"""Application service for LLM-driven tool selection."""

from typing import Any

from oracle_ebs_chatbot.domain.registry import DomainRegistry
from oracle_ebs_chatbot.llm.ollama_client import OllamaClient
from oracle_ebs_chatbot.llm.response_parser import LlmResponseParser
from oracle_ebs_chatbot.llm.tool_schemas import get_tool_schemas
from oracle_ebs_chatbot.orchestrator.schemas import ToolCall


class LlmService:
    """Coordinate LLM communication and response parsing."""

    def __init__(
        self,
        client: OllamaClient,
        parser: LlmResponseParser,
        domain_registry: DomainRegistry,
    ) -> None:
        self.client = client
        self.parser = parser
        self.domain_registry = domain_registry

    def create_tool_call(
        self,
        messages: list[dict[str, Any]],
    ) -> ToolCall:
        """Ask the LLM for the next tool call and validate it."""

        tools = get_tool_schemas(self.domain_registry)

        response = self.client.chat(
            messages,
            tools=tools,
        )

        return self.parser.parse(response)
