"""Controlled orchestration loop for chatbot tool execution."""

from oracle_ebs_chatbot.orchestrator.schemas import ToolCall
from oracle_ebs_chatbot.orchestrator.tool_catalog import ToolCatalog
from oracle_ebs_chatbot.tools.base import ToolResult


class OrchestratorLoop:
    """Execute only tools registered in the tool catalog."""

    def __init__(self, tool_catalog: ToolCatalog) -> None:
        self.tool_catalog = tool_catalog

    def execute_tool(self, tool_call: ToolCall) -> ToolResult:
        """Resolve and execute a validated tool request."""

        tool = self.tool_catalog.get(tool_call.tool)

        if tool is None:
            return ToolResult(
                success=False,
                error=f"Unknown tool: {tool_call.tool}",
            )

        try:
            return tool.execute(tool_call.parameters)
        except ValueError as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )
