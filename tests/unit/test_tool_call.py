import pytest
from pydantic import ValidationError

from oracle_ebs_chatbot.orchestrator.schemas import ToolCall


def test_tool_call_contains_tool_and_parameters() -> None:
    tool_call = ToolCall(
        tool="entity_lookup",
        parameters={
            "entity": "purchase_order",
            "identifier": "PO-1001",
        },
    )

    assert tool_call.tool == "entity_lookup"
    assert tool_call.parameters == {
        "entity": "purchase_order",
        "identifier": "PO-1001",
    }


def test_tool_call_allows_empty_parameters() -> None:
    tool_call = ToolCall(tool="example")

    assert tool_call.parameters == {}


def test_tool_call_requires_tool_name() -> None:
    with pytest.raises(ValidationError):
        ToolCall(tool="", parameters={})
