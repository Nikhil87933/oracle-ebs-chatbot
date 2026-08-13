"""Generic entity lookup capability."""

from typing import Any

from oracle_ebs_chatbot.clients.ords_client import OrdsClient
from oracle_ebs_chatbot.tools.base import BaseTool, ToolResult


class EntityLookupTool(BaseTool):
    """Fetch a single business entity by identifier."""

    name = "entity_lookup"
    description = "Fetch a single business entity by its identifier."

    def __init__(self, ords_client: OrdsClient) -> None:
        self.ords_client = ords_client

    def validate(self, parameters: dict[str, Any]) -> None:
        """Validate entity lookup parameters."""

        entity = parameters.get("entity")
        identifier = parameters.get("identifier")

        if not isinstance(entity, str) or not entity.strip():
            raise ValueError("entity is required")

        if not isinstance(identifier, str) or not identifier.strip():
            raise ValueError("identifier is required")

    def execute(self, parameters: dict[str, Any]) -> ToolResult:
        """Validate parameters and fetch the requested entity."""

        self.validate(parameters)

        entity = str(parameters["entity"])
        identifier = str(parameters["identifier"])

        try:
            data = self.ords_client.get_entity(
                entity=entity,
                identifier=identifier,
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )

        return ToolResult(
            success=True,
            data=data,
        )
