from typing import Any

import pytest

from oracle_ebs_chatbot.clients.ords_client import OrdsClient
from oracle_ebs_chatbot.tools.base import BaseTool, ToolResult
from oracle_ebs_chatbot.tools.entity_lookup import EntityLookupTool


class ExampleTool(BaseTool):
    """Test implementation of the base tool contract."""

    name = "example"
    description = "Example tool."

    def validate(self, parameters: dict[str, Any]) -> None:
        """Validate example parameters."""
        if "value" not in parameters:
            raise ValueError("value is required")

    def execute(self, parameters: dict[str, Any]) -> ToolResult:
        """Execute example tool."""
        self.validate(parameters)
        return ToolResult(
            success=True,
            data=parameters["value"],
        )


class MockOrdsClient(OrdsClient):
    """Fake ORDS client used by unit tests."""

    def __init__(self) -> None:
        super().__init__(base_url="http://mock-ords")

    def get_entity(
        self,
        entity: str,
        identifier: str,
    ) -> dict[str, Any]:
        """Return a deterministic fake entity."""
        return {
            "entity": entity,
            "identifier": identifier,
            "name": "Test Purchase Order",
        }

    def aggregate(
        self,
        metric: str,
        dimensions: list[str],
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Return deterministic aggregate data."""
        return [
            {
                "metric": metric,
                "dimensions": dimensions,
                "filters": filters,
            }
        ]


def test_tool_result_success() -> None:
    result = ToolResult(
        success=True,
        data={"id": 123},
    )

    assert result.success is True
    assert result.data == {"id": 123}
    assert result.error is None


def test_tool_result_error() -> None:
    result = ToolResult(
        success=False,
        error="Something went wrong.",
    )

    assert result.success is False
    assert result.error == "Something went wrong."


def test_base_tool_requires_validate_and_execute() -> None:
    tool = ExampleTool()

    assert tool.name == "example"
    assert tool.description == "Example tool."

    result = tool.execute({"value": "test"})

    assert result.success is True
    assert result.data == "test"


def test_base_tool_validation_happens_before_execution() -> None:
    tool = ExampleTool()

    with pytest.raises(ValueError, match="value is required"):
        tool.execute({})


def test_entity_lookup_returns_ords_data() -> None:
    tool = EntityLookupTool(MockOrdsClient())

    result = tool.execute(
        {
            "entity": "purchase_order",
            "identifier": "PO-1001",
        }
    )

    assert result.success is True
    assert result.data == {
        "entity": "purchase_order",
        "identifier": "PO-1001",
        "name": "Test Purchase Order",
    }


def test_entity_lookup_requires_entity() -> None:
    tool = EntityLookupTool(MockOrdsClient())

    with pytest.raises(ValueError, match="entity is required"):
        tool.execute({"identifier": "PO-1001"})


def test_entity_lookup_requires_identifier() -> None:
    tool = EntityLookupTool(MockOrdsClient())

    with pytest.raises(ValueError, match="identifier is required"):
        tool.execute({"entity": "purchase_order"})


def test_entity_lookup_rejects_blank_entity() -> None:
    tool = EntityLookupTool(MockOrdsClient())

    with pytest.raises(ValueError, match="entity is required"):
        tool.execute(
            {
                "entity": "   ",
                "identifier": "PO-1001",
            }
        )


def test_entity_lookup_rejects_blank_identifier() -> None:
    tool = EntityLookupTool(MockOrdsClient())

    with pytest.raises(ValueError, match="identifier is required"):
        tool.execute(
            {
                "entity": "purchase_order",
                "identifier": "   ",
            }
        )


class FailingOrdsClient(MockOrdsClient):
    """Fake ORDS client that simulates backend failures."""

    def get_entity(
        self,
        entity: str,
        identifier: str,
    ) -> dict[str, Any]:
        """Simulate an ORDS entity lookup failure."""
        raise RuntimeError("ORDS unavailable")

    def aggregate(
        self,
        metric: str,
        dimensions: list[str],
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Simulate an ORDS aggregate failure."""
        raise RuntimeError("ORDS unavailable")


def test_entity_lookup_returns_failed_tool_result_on_ords_error() -> None:
    tool = EntityLookupTool(FailingOrdsClient())

    result = tool.execute(
        {
            "entity": "purchase_order",
            "identifier": "PO-1001",
        }
    )

    assert result.success is False
    assert result.error == "ORDS unavailable"


def test_aggregate_query_returns_failed_tool_result_on_ords_error() -> None:
    from oracle_ebs_chatbot.domain.registry import (
        ApprovedCombination,
        Dimension,
        DomainRegistry,
        Entity,
        Metric,
    )
    from oracle_ebs_chatbot.tools.aggregate_query import AggregateQueryTool

    entity = Entity(
        name="purchase_order",
        description="A purchase order.",
    )
    metric = Metric(
        name="po_amount",
        description="Total purchase order amount.",
        entity="purchase_order",
    )
    dimension = Dimension(
        name="supplier",
        description="Supplier.",
        entity="purchase_order",
    )

    registry = DomainRegistry(
        entities={"purchase_order": entity},
        metrics={"po_amount": metric},
        dimensions={"supplier": dimension},
        approved_combinations=[
            ApprovedCombination(
                metric="po_amount",
                dimensions=frozenset({"supplier"}),
            )
        ],
    )

    tool = AggregateQueryTool(
        FailingOrdsClient(),
        registry,
    )

    result = tool.execute(
        {
            "metric": "po_amount",
            "dimensions": ["supplier"],
            "filters": {},
        }
    )

    assert result.success is False
    assert result.error == "ORDS unavailable"
