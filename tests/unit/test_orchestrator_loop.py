from oracle_ebs_chatbot.clients.ords_client import OrdsClient
from oracle_ebs_chatbot.domain.registry import DomainRegistry
from oracle_ebs_chatbot.orchestrator.loop import OrchestratorLoop
from oracle_ebs_chatbot.orchestrator.schemas import ToolCall
from oracle_ebs_chatbot.orchestrator.tool_catalog import ToolCatalog


def create_loop() -> OrchestratorLoop:
    """Create an orchestrator with test dependencies."""
    catalog = ToolCatalog(
        ords_client=OrdsClient("http://mock-ords"),
        domain_registry=DomainRegistry(),
    )

    return OrchestratorLoop(catalog)


def test_unknown_tool_is_rejected() -> None:
    loop = create_loop()

    result = loop.execute_tool(
        ToolCall(
            tool="delete_database",
            parameters={},
        )
    )

    assert result.success is False
    assert result.error == "Unknown tool: delete_database"


def test_known_tool_validation_failure_returns_tool_result() -> None:
    loop = create_loop()

    result = loop.execute_tool(
        ToolCall(
            tool="entity_lookup",
            parameters={},
        )
    )

    assert result.success is False
    assert result.error == "entity is required"


def test_known_tool_is_resolved_from_catalog() -> None:
    loop = create_loop()

    result = loop.execute_tool(
        ToolCall(
            tool="entity_lookup",
            parameters={
                "entity": "purchase_order",
                "identifier": "PO-1001",
            },
        )
    )

    assert result.success is False
    assert result.error is not None
