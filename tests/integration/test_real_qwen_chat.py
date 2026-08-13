from oracle_ebs_chatbot.domain.default_registry import create_default_registry
from oracle_ebs_chatbot.llm.ollama_client import OllamaClient
from oracle_ebs_chatbot.llm.response_parser import LlmResponseParser
from oracle_ebs_chatbot.llm.service import LlmService


def test_real_qwen_selects_entity_lookup() -> None:
    registry = create_default_registry()

    client = OllamaClient(
        host="http://localhost:11434",
        model="qwen2.5:7b",
    )

    service = LlmService(
        client=client,
        parser=LlmResponseParser(),
        domain_registry=registry,
    )

    tool_call = service.create_tool_call(
        [
            {
                "role": "user",
                "content": "Look up purchase order PO-1001.",
            }
        ]
    )

    assert tool_call.tool == "entity_lookup"
    assert tool_call.parameters["entity"] == "purchase_order"
    assert tool_call.parameters["identifier"] == "PO-1001"
