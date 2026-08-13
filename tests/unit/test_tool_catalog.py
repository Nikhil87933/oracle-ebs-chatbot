from oracle_ebs_chatbot.clients.ords_client import OrdsClient
from oracle_ebs_chatbot.domain.registry import DomainRegistry
from oracle_ebs_chatbot.orchestrator.tool_catalog import ToolCatalog
from oracle_ebs_chatbot.tools.aggregate_query import AggregateQueryTool
from oracle_ebs_chatbot.tools.entity_lookup import EntityLookupTool


def test_catalog_registers_entity_lookup() -> None:
    catalog = ToolCatalog(
        ords_client=OrdsClient("http://mock-ords"),
        domain_registry=DomainRegistry(),
    )

    tool = catalog.get("entity_lookup")

    assert isinstance(tool, EntityLookupTool)


def test_catalog_registers_aggregate_query() -> None:
    catalog = ToolCatalog(
        ords_client=OrdsClient("http://mock-ords"),
        domain_registry=DomainRegistry(),
    )

    tool = catalog.get("aggregate_query")

    assert isinstance(tool, AggregateQueryTool)


def test_catalog_returns_none_for_unknown_tool() -> None:
    catalog = ToolCatalog(
        ords_client=OrdsClient("http://mock-ords"),
        domain_registry=DomainRegistry(),
    )

    assert catalog.get("does_not_exist") is None


def test_catalog_lists_registered_tools() -> None:
    catalog = ToolCatalog(
        ords_client=OrdsClient("http://mock-ords"),
        domain_registry=DomainRegistry(),
    )

    tools = catalog.list_tools()
    names = {tool.name for tool in tools}

    assert names == {
        "entity_lookup",
        "aggregate_query",
    }
