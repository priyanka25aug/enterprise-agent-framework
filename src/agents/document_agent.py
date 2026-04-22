from .base_agent import BaseAgent, AgentInput, AgentOutput

DOCUMENT_PATTERNS = {
    "earnings_call": ["revenue", "earnings", "guidance", "quarterly", "eps", "beat", "miss", "outlook"],
    "risk_disclosure": ["risk factor", "material adverse", "forward-looking", "uncertainty", "litigation"],
    "trade_confirmation": ["trade date", "settlement", "cusip", "isin", "notional", "counterparty", "execution"],
}


class DocumentAgent(BaseAgent):
    def __init__(self, mock_mode: bool = True):
        super().__init__("DocumentAgent", mock_mode)

    def _process(self, agent_input: AgentInput) -> AgentOutput:
        content_lower = agent_input.content.lower()
        scores = {}
        for doc_type, keywords in DOCUMENT_PATTERNS.items():
            matched = sum(1 for kw in keywords if kw in content_lower)
            scores[doc_type] = self._score_confidence(matched, len(keywords))

        best_type = max(scores, key=scores.get)
        confidence = scores[best_type]

        return AgentOutput(
            result=f"Document classified as: {best_type.replace('_', ' ').title()}",
            confidence=confidence,
            agent_name=self.name,
            reasoning=f"Keyword match scores: {scores}",
            metadata={"document_type": best_type, "all_scores": scores},
        )
