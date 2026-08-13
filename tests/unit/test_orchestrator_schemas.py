import pytest
from pydantic import ValidationError

from oracle_ebs_chatbot.orchestrator.schemas import ToolCall


def test_tool_call_accepts_valid_request() -> None:
    request = ToolCall(
        tool="aggregate_query",
        parameters={
            "metric": "po_amount",
            "dimensions": ["supplier"],
            "filters": {},
        },
    )

    assert request.tool == "aggregate_query"
    assert request.parameters["metric"] == "po_amount"


def test_tool_call_defaults_parameters_to_empty_dict() -> None:
    request = ToolCall(tool="entity_lookup")

    assert request.parameters == {}


def test_tool_call_rejects_empty_tool_name() -> None:
    with pytest.raises(ValidationError):
        ToolCall(tool="")


def test_tool_call_rejects_missing_tool_name() -> None:
    with pytest.raises(ValidationError):
        ToolCall.model_validate({})
