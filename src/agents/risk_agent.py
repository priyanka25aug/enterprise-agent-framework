from .base_agent import BaseAgent, AgentInput, AgentOutput

RISK_CATEGORIES = {
    "market_risk": ["volatility", "vix", "beta", "drawdown", "var", "mark-to-market"],
    "credit_risk": ["default", "counterparty", "downgrade", "credit spread", "cds", "collateral"],
    "operational_risk": ["system failure", "fraud", "human error", "process breakdown", "outage"],
    "regulatory_risk": ["sec", "finra", "compliance", "violation", "enforcement", "breach", "limit exceeded"],
}

ESCALATION_TRIGGERS = {"breach", "limit exceeded", "default", "fraud", "enforcement", "violation"}


class RiskAgent(BaseAgent):
    def __init__(self, mock_mode: bool = True):
        super().__init__("RiskAgent", mock_mode)

    def _process(self, agent_input: AgentInput) -> AgentOutput:
        content_lower = agent_input.content.lower()
        scores = {}
        for category, keywords in RISK_CATEGORIES.items():
            matched = sum(1 for kw in keywords if kw in content_lower)
            scores[category] = self._score_confidence(matched, len(keywords))

        best_category = max(scores, key=scores.get)
        confidence = scores[best_category]
        should_escalate = any(trigger in content_lower for trigger in ESCALATION_TRIGGERS)

        return AgentOutput(
            result=f"Risk category: {best_category.replace('_', ' ').title()}",
            confidence=confidence,
            agent_name=self.name,
            reasoning=f"Risk scores: {scores}. Auto-escalated: {should_escalate}",
            metadata={"risk_category": best_category, "all_scores": scores},
            escalate=should_escalate,
        )
