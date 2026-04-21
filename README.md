# enterprise-agent-framework

A production-grade multi-agent orchestration framework built for regulated enterprise environments — financial services, healthcare, legal.

Designed from real deployments at Tier-1 financial institutions. Not a toy. Not a tutorial. Built to handle the things that break in production.

---

## Architecture

The framework uses a three-layer agent pattern:

```
User Request
     │
     ▼
┌─────────────┐
│   Router    │  ← Classifies intent, selects specialist agent
└─────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│           Specialist Agents             │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │ Document │ │  Risk    │ │ Query   │ │
│  │ Agent    │ │  Agent   │ │ Agent   │ │
│  └──────────┘ └──────────┘ └─────────┘ │
└─────────────────────────────────────────┘
     │
     ▼
┌─────────────┐
│ Reconciler  │  ← Validates output, checks confidence, routes to human if needed
└─────────────┘
     │
     ▼
Final Output (with audit trail)
```

**Why three layers?**

Giving one agent too much to decide at once is the most common failure pattern in enterprise AI. A single overloaded agent produces inconsistent outputs, fails silently on edge cases, and is impossible to debug in production.

The router keeps intent classification separate from execution. Specialist agents do one thing well. The reconciler acts as the safety net — catching low-confidence outputs before they reach a human.

---

## Features

- **Intent routing** — classifies incoming requests and dispatches to the right specialist
- **Specialist sub-agents** — modular, independently testable agents per domain
- **Reconciliation layer** — confidence scoring, output validation, human-in-the-loop escalation
- **Full audit trail** — every decision logged with input, output, agent used, confidence score, and timestamp
- **Pluggable LLM backend** — works with OpenAI, Anthropic, Google Vertex AI, or local models
- **Regulated-environment ready** — explainability outputs, confidence thresholds, escalation paths

---

## Quickstart

```bash
pip install -r requirements.txt
cp .env.example .env  # add your LLM API key
python examples/run_basic.py
```

---

## Project Structure

```
enterprise-agent-framework/
├── src/
│   ├── router/
│   │   ├── __init__.py
│   │   └── intent_router.py       # Classifies request → selects agent
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py          # Abstract base class for all agents
│   │   ├── document_agent.py      # Document classification & extraction
│   │   ├── risk_agent.py          # Risk assessment & flagging
│   │   └── query_agent.py         # General Q&A over structured data
│   ├── reconciler/
│   │   ├── __init__.py
│   │   └── reconciler.py          # Output validation, confidence gating
│   └── utils/
│       ├── __init__.py
│       ├── audit_logger.py        # Structured audit trail
│       └── llm_client.py          # Unified LLM interface
├── tests/
│   ├── test_router.py
│   ├── test_agents.py
│   └── test_reconciler.py
├── examples/
│   └── run_basic.py
├── .env.example
├── requirements.txt
└── README.md
```

---

## Configuration

```python
from src.router import IntentRouter
from src.agents import DocumentAgent, RiskAgent, QueryAgent
from src.reconciler import Reconciler

# Register your specialist agents
router = IntentRouter()
router.register("document", DocumentAgent())
router.register("risk", RiskAgent())
router.register("query", QueryAgent())

# Set up reconciler with confidence threshold
reconciler = Reconciler(confidence_threshold=0.75)

# Run
result = reconciler.process(
    router.route("Classify this earnings call document and flag any risk disclosures")
)

print(result.output)
print(result.audit_trail)
```

---

## Reconciler behaviour

The reconciler does three things before returning any output:

1. **Confidence check** — if the agent's confidence score is below the threshold, the output is flagged for human review rather than returned directly
2. **Consistency validation** — checks the output format matches the expected schema for that agent type
3. **Audit logging** — records the full decision path regardless of outcome

In regulated environments, "I don't know" is a valid and important output. The reconciler surfaces that honestly rather than returning a confident but wrong answer.

---

## Why this exists

Built from experience deploying AI agents in investment banking environments where:
- A wrong output has regulatory consequences
- Every decision needs to be explainable to Risk and Legal
- Human-in-the-loop isn't optional — it's a design requirement
- Models that work in demos fail in production on edge cases

---

## Requirements

- Python 3.10+
- An LLM API key (OpenAI, Anthropic, or Google Vertex AI)

---

## License

MIT
