from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import time


@dataclass
class AgentInput:
    content: str
    context: Dict[str, Any] = field(default_factory=dict)
    session_id: str = ""
    user_id: str = ""


@dataclass
class AgentOutput:
    result: str
    confidence: float
    agent_name: str
    reasoning: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    escalate: bool = False
    latency_ms: float = 0.0


class BaseAgent(ABC):
    def __init__(self, name: str, mock_mode: bool = True):
        self.name = name
        self.mock_mode = mock_mode

    def run(self, agent_input: AgentInput) -> AgentOutput:
        start = time.time()
        output = self._process(agent_input)
        output.latency_ms = (time.time() - start) * 1000
        output.agent_name = self.name
        return output

    @abstractmethod
    def _process(self, agent_input: AgentInput) -> AgentOutput:
        pass

    def _score_confidence(self, matched_keywords: int, total_keywords: int) -> float:
        if total_keywords == 0:
            return 0.5
        return min(0.5 + 0.5 * (matched_keywords / total_keywords), 0.99)
