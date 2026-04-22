import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from src.router.intent_router import IntentRouter
from src.agents import DocumentAgent, RiskAgent, QueryAgent, AgentInput
from src.reconciler.reconciler import Reconciler


@pytest.fixture
def router():
    return IntentRouter()


def test_routes_earnings_to_document(router):
    decision = router.route("Q3 earnings call transcript with revenue guidance")
    assert decision.agent_type == "document"


def test_routes_breach_to_risk(router):
    decision = router.route("Counterparty limit exceeded, breach detected in trading system")
    assert decision.agent_type == "risk"


def test_routes_generic_to_query(router):
    decision = router.route("Hello, how are you today?")
    assert decision.agent_type == "query"


def test_explain_routing_returns_string(router):
    explanation = router.explain_routing("earnings call revenue beat")
    assert isinstance(explanation, str)
    assert "document" in explanation


def test_document_agent_classifies_earnings():
    agent = DocumentAgent(mock_mode=True)
    output = agent.run(AgentInput(content="quarterly earnings revenue EPS guidance beat"))
    assert output.confidence > 0.5
    assert "earnings" in output.result.lower() or output.metadata["document_type"] == "earnings_call"


def test_risk_agent_escalates_on_breach():
    agent = RiskAgent(mock_mode=True)
    output = agent.run(AgentInput(content="limit exceeded on counterparty credit exposure"))
    assert output.escalate is True


def test_reconciler_escalates_low_confidence():
    agent = QueryAgent(mock_mode=True)
    output = agent.run(AgentInput(content="hi"))
    output.confidence = 0.4
    reconciler = Reconciler(threshold=0.75)
    result = reconciler.reconcile(output)
    assert result.human_escalation_required is True
    assert result.audit_id is not None


def test_reconciler_passes_high_confidence():
    agent = DocumentAgent(mock_mode=True)
    output = agent.run(AgentInput(content="earnings revenue quarterly guidance EPS beat outlook"))
    reconciler = Reconciler(threshold=0.75)
    result = reconciler.reconcile(output)
    assert result.audit_id is not None
