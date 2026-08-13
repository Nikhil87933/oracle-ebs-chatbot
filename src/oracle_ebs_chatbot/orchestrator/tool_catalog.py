"""Registry of chatbot tools available to the orchestrator."""

from oracle_ebs_chatbot.clients.ords_client import OrdsClient
from oracle_ebs_chatbot.domain.registry import DomainRegistry
from oracle_ebs_chatbot.tools.aggregate_query import AggregateQueryTool
from oracle_ebs_chatbot.tools.base import BaseTool
from oracle_ebs_chatbot.tools.entity_lookup import EntityLookupTool


class ToolCatalog:
    """Provide the controlled set of tools available to the chatbot."""

    def __init__(
        self,
        ords_client: OrdsClient,
        domain_registry: DomainRegistry,
    ) -> None:
        self._tools: dict[str, BaseTool] = {
            EntityLookupTool.name: EntityLookupTool(ords_client),
            AggregateQueryTool.name: AggregateQueryTool(
                ords_client,
                domain_registry,
            ),
        }

    def get(self, name: str) -> BaseTool | None:
        """Return a tool by its registered name."""
        return self._tools.get(name)

    def list_tools(self) -> list[BaseTool]:
        """Return all registered tools."""
        return list(self._tools.values())
