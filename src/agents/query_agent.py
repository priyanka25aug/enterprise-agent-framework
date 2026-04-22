from .base_agent import BaseAgent, AgentInput, AgentOutput


class QueryAgent(BaseAgent):
    def __init__(self, mock_mode: bool = True):
        super().__init__("QueryAgent", mock_mode)

    def _process(self, agent_input: AgentInput) -> AgentOutput:
        word_count = len(agent_input.content.split())
        confidence = min(0.6 + 0.01 * min(word_count, 30), 0.85)
        return AgentOutput(
            result=f"General query processed: '{agent_input.content[:80]}...' (mock response)",
            confidence=confidence,
            agent_name=self.name,
            reasoning="Fallback general Q&A agent — no domain-specific keywords matched router rules",
            metadata={"word_count": word_count},
        )
