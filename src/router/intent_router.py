from dataclasses import dataclass
from typing import Tuple

ROUTING_RULES = {
    "document": ["earnings", "filing", "trade confirm", "settlement", "disclosure", "prospectus", "cusip"],
    "risk": ["risk", "exposure", "breach", "limit exceeded", "default", "volatility", "var", "compliance"],
    "query": [],
}


@dataclass
class RoutingDecision:
    agent_type: str
    matched_keywords: list
    rule_applied: str
    confidence: float


class IntentRouter:
    def route(self, content: str) -> RoutingDecision:
        content_lower = content.lower()
        scores = {}
        matched = {}
        for agent_type, keywords in ROUTING_RULES.items():
            hits = [kw for kw in keywords if kw in content_lower]
            scores[agent_type] = len(hits)
            matched[agent_type] = hits

        if scores["document"] >= scores["risk"] and scores["document"] > 0:
            chosen = "document"
        elif scores["risk"] > 0:
            chosen = "risk"
        else:
            chosen = "query"

        total = max(sum(scores.values()), 1)
        confidence = min(0.5 + 0.1 * scores[chosen], 0.95)

        return RoutingDecision(
            agent_type=chosen,
            matched_keywords=matched[chosen],
            rule_applied=f"keyword_match:{chosen}",
            confidence=confidence,
        )

    def explain_routing(self, content: str) -> str:
        decision = self.route(content)
        return (
            f"Route: {decision.agent_type} | "
            f"Keywords matched: {decision.matched_keywords} | "
            f"Rule: {decision.rule_applied} | "
            f"Confidence: {decision.confidence:.2f}"
        )
