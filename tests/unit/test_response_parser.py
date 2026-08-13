import pytest

from oracle_ebs_chatbot.llm.response_parser import LlmResponseParser


def test_parser_creates_tool_call() -> None:
    parser = LlmResponseParser()

    result = parser.parse(
        {
            "message": {
                "tool_calls": [
                    {
                        "function": {
                            "name": "entity_lookup",
                            "arguments": {
                                "entity": "purchase_order",
                                "identifier": "PO-1001",
                            },
                        }
                    }
                ]
            }
        }
    )

    assert result.tool == "entity_lookup"
    assert result.parameters == {
        "entity": "purchase_order",
        "identifier": "PO-1001",
    }


def test_parser_allows_missing_arguments() -> None:
    parser = LlmResponseParser()

    result = parser.parse(
        {
            "message": {
                "tool_calls": [
                    {
                        "function": {
                            "name": "entity_lookup",
                        }
                    }
                ]
            }
        }
    )

    assert result.parameters == {}


def test_parser_rejects_missing_message() -> None:
    parser = LlmResponseParser()

    with pytest.raises(ValueError, match="missing message"):
        parser.parse({})


def test_parser_rejects_missing_tool_calls() -> None:
    parser = LlmResponseParser()

    with pytest.raises(ValueError, match="missing tool_calls"):
        parser.parse({"message": {}})


def test_parser_rejects_invalid_tool_name() -> None:
    parser = LlmResponseParser()

    with pytest.raises(ValueError, match="tool name must be a string"):
        parser.parse(
            {
                "message": {
                    "tool_calls": [
                        {
                            "function": {
                                "name": 123,
                            }
                        }
                    ]
                }
            }
        )


def test_parser_rejects_invalid_arguments() -> None:
    parser = LlmResponseParser()

    with pytest.raises(ValueError, match="arguments must be an object"):
        parser.parse(
            {
                "message": {
                    "tool_calls": [
                        {
                            "function": {
                                "name": "entity_lookup",
                                "arguments": "invalid",
                            }
                        }
                    ]
                }
            }
        )


def test_parser_rejects_invalid_tool_call() -> None:
    parser = LlmResponseParser()

    with pytest.raises(ValueError, match="tool call must be an object"):
        parser.parse(
            {
                "message": {
                    "tool_calls": ["invalid"],
                }
            }
        )


def test_parser_rejects_missing_function() -> None:
    parser = LlmResponseParser()

    with pytest.raises(ValueError, match="missing function"):
        parser.parse(
            {
                "message": {
                    "tool_calls": [{}],
                }
            }
        )
