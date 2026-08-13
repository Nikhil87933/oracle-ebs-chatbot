"""Application-level chatbot service."""

from typing import Any

from oracle_ebs_chatbot.llm.service import LlmService
from oracle_ebs_chatbot.orchestrator.loop import OrchestratorLoop
from oracle_ebs_chatbot.security.boundary import SecurityBoundary
from oracle_ebs_chatbot.tools.base import ToolResult


class ChatService:
    """Coordinate security, LLM tool selection, and tool execution."""

    def __init__(
        self,
        llm_service: LlmService,
        orchestrator: OrchestratorLoop,
        security_boundary: SecurityBoundary,
    ) -> None:
        self.llm_service = llm_service
        self.orchestrator = orchestrator
        self.security_boundary = security_boundary

    def handle_message(
        self,
        message: str,
        identity: dict[str, Any],
    ) -> ToolResult:
        """Process a user message through the secured chatbot flow."""

        _, validated_message = self.security_boundary.authenticate_and_validate(
            identity=identity,
            message=message,
            capability="chat",
        )

        messages: list[dict[str, Any]] = [
            {
                "role": "user",
                "content": validated_message,
            }
        ]

        tool_call = self.llm_service.create_tool_call(messages)

        return self.orchestrator.execute_tool(tool_call)
