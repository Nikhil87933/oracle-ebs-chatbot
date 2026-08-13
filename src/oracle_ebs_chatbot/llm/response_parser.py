"""Parse LLM responses into controlled tool calls."""

from typing import Any

from oracle_ebs_chatbot.orchestrator.schemas import ToolCall


class LlmResponseParser:
    """Convert a raw Ollama response into a validated ToolCall."""

    def parse(self, response: dict[str, Any]) -> ToolCall:
        """Parse an Ollama tool-calling response."""

        message = response.get("message")

        if not isinstance(message, dict):
            raise ValueError("LLM response is missing message")

        tool_calls = message.get("tool_calls")

        if not isinstance(tool_calls, list) or not tool_calls:
            raise ValueError("LLM response is missing tool_calls")

        first_call = tool_calls[0]

        if not isinstance(first_call, dict):
            raise ValueError("LLM tool call must be an object")

        function = first_call.get("function")

        if not isinstance(function, dict):
            raise ValueError("LLM tool call is missing function")

        tool_name = function.get("name")
        parameters = function.get("arguments", {})

        if not isinstance(tool_name, str):
            raise ValueError("LLM tool name must be a string")

        if not isinstance(parameters, dict):
            raise ValueError("LLM tool arguments must be an object")

        return ToolCall(
            tool=tool_name,
            parameters=parameters,
        )
