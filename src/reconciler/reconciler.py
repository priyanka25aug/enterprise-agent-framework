from dataclasses import dataclass
from typing import Optional
from ..agents.base_agent import AgentOutput
from ..utils.audit_logger import AuditLogger

CONFIDENCE_THRESHOLD = 0.75


@dataclass
class ReconcilerResult:
    final_output: AgentOutput
    human_escalation_required: bool
    escalation_reason: Optional[str]
    audit_id: str


class Reconciler:
    def __init__(self, threshold: float = CONFIDENCE_THRESHOLD):
        self.threshold = threshold
        self.logger = AuditLogger()

    def reconcile(self, output: AgentOutput, session_id: str = "") -> ReconcilerResult:
        escalate = False
        reason = None

        if output.confidence < self.threshold:
            escalate = True
            reason = f"Confidence {output.confidence:.2f} below threshold {self.threshold}"

        if output.escalate:
            escalate = True
            reason = (reason or "") + " | Agent-triggered escalation (breach/limit exceeded detected)"

        audit_id = self.logger.log({
            "session_id": session_id,
            "agent": output.agent_name,
            "result": output.result,
            "confidence": output.confidence,
            "escalated": escalate,
            "escalation_reason": reason,
            "reasoning": output.reasoning,
        })

        return ReconcilerResult(
            final_output=output,
            human_escalation_required=escalate,
            escalation_reason=reason,
            audit_id=audit_id,
        )
