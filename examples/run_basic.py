#!/usr/bin/env python3
"""Working demo — runs entirely in mock mode, no LLM API key required."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.agents import DocumentAgent, RiskAgent, QueryAgent, AgentInput
from src.router.intent_router import IntentRouter
from src.reconciler.reconciler import Reconciler

AGENT_MAP = {
    "document": DocumentAgent(mock_mode=True),
    "risk": RiskAgent(mock_mode=True),
    "query": QueryAgent(mock_mode=True),
}

router = IntentRouter()
reconciler = Reconciler(threshold=0.75)

TEST_INPUTS = [
    "Q3 earnings call transcript: revenue beat expectations, EPS guidance raised for FY2024.",
    "Credit risk alert: counterparty limit exceeded on EUR/USD forward trade, breach reported.",
    "Risk disclosure filing: material adverse factors include litigation and regulatory uncertainty.",
    "What is the capital adequacy ratio formula?",
    "Trade confirmation: CUSIP 123456789, settlement T+2, notional $5M, counterparty Goldman Sachs.",
]

print("=" * 70)
print("Enterprise Agent Framework — Demo Run")
print("=" * 70)

for i, text in enumerate(TEST_INPUTS, 1):
    print(f"\n[{i}] Input: {text[:75]}...")
    routing = router.route(text)
    print(f"     Router → {routing.agent_type} (keywords: {routing.matched_keywords})")

    agent = AGENT_MAP[routing.agent_type]
    output = agent.run(AgentInput(content=text, session_id=f"demo-{i}"))
    result = reconciler.reconcile(output, session_id=f"demo-{i}")

    print(f"     Result: {output.result}")
    print(f"     Confidence: {output.confidence:.2f} | Escalate: {result.human_escalation_required}")
    if result.escalation_reason:
        print(f"     Escalation reason: {result.escalation_reason}")
    print(f"     Audit ID: {result.audit_id}")

print("\n" + "=" * 70)
print("Audit trail written to audit_trail.jsonl")
print("All agents ran successfully in mock mode.")
