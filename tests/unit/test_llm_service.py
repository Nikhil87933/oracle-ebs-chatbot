from unittest.mock import Mock

import pytest

from oracle_ebs_chatbot.domain.default_registry import create_default_registry
from oracle_ebs_chatbot.llm.ollama_client import OllamaClient
from oracle_ebs_chatbot.llm.response_parser import LlmResponseParser
from oracle_ebs_chatbot.llm.service import LlmService
from oracle_ebs_chatbot.llm.tool_schemas import get_tool_schemas


def test_llm_service_returns_parsed_tool_call() -> None:
    client = Mock(spec=OllamaClient)
    parser = LlmResponseParser()

    client.chat.return_value = {
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

    service = LlmService(
        client=client,
        parser=parser,
        domain_registry=create_default_registry(),
    )

    messages = [
        {
            "role": "user",
            "content": "Show me PO-1001.",
        }
    ]

    result = service.create_tool_call(messages)

    assert result.tool == "entity_lookup"
    assert result.parameters == {
        "entity": "purchase_order",
        "identifier": "PO-1001",
    }

    client.chat.assert_called_once_with(
        messages,
        tools=get_tool_schemas(create_default_registry()),
    )


def test_llm_service_propagates_parser_failure() -> None:
    client = Mock(spec=OllamaClient)
    parser = LlmResponseParser()

    client.chat.return_value = {
        "message": {},
    }

    service = LlmService(
        client=client,
        parser=parser,
        domain_registry=create_default_registry(),
    )

    with pytest.raises(
        ValueError,
        match="LLM response is missing tool_call",
    ):
        service.create_tool_call(
            [
                {
                    "role": "user",
                    "content": "Show me PO-1001.",
                }
            ]
        )
