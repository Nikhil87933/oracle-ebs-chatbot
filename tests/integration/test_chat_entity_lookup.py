from unittest.mock import Mock

import httpx
import pytest

from oracle_ebs_chatbot.chat.service import ChatService
from oracle_ebs_chatbot.clients.ords_client import OrdsClient
from oracle_ebs_chatbot.domain.default_registry import create_default_registry
from oracle_ebs_chatbot.llm.ollama_client import OllamaClient
from oracle_ebs_chatbot.llm.response_parser import LlmResponseParser
from oracle_ebs_chatbot.llm.service import LlmService
from oracle_ebs_chatbot.orchestrator.loop import OrchestratorLoop
from oracle_ebs_chatbot.orchestrator.tool_catalog import ToolCatalog
from oracle_ebs_chatbot.security.auth import AuthenticationService
from oracle_ebs_chatbot.security.authorization import AuthorizationService
from oracle_ebs_chatbot.security.boundary import SecurityBoundary


def test_chat_entity_lookup_end_to_end() -> None:
    def ords_handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert str(request.url) == ("http://fake-ords/purchase_order/PO-1001")

        return httpx.Response(
            200,
            json={
                "po_number": "PO-1001",
                "status": "APPROVED",
                "supplier": "ABC Supplies",
                "amount": 125000,
            },
        )

    transport = httpx.MockTransport(ords_handler)
    http_client = httpx.Client(transport=transport)

    ords_client = OrdsClient(
        base_url="http://fake-ords",
        http_client=http_client,
    )

    registry = create_default_registry()

    tool_catalog = ToolCatalog(
        ords_client=ords_client,
        domain_registry=registry,
    )

    orchestrator = OrchestratorLoop(tool_catalog)

    llm_client = Mock(spec=OllamaClient)
    llm_client.chat.return_value = {
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

    llm_service = LlmService(
        client=llm_client,
        parser=LlmResponseParser(),
        domain_registry=registry,
    )

    security_boundary = SecurityBoundary(
        authentication=AuthenticationService(),
        authorization=AuthorizationService(
            allowed_capabilities={"chat"},
        ),
    )

    service = ChatService(
        llm_service=llm_service,
        orchestrator=orchestrator,
        security_boundary=security_boundary,
    )

    result = service.handle_message(
        message="Show me PO-1001.",
        identity={"username": "POC_USER"},
    )

    assert result.success is True
    assert result.data == {
        "po_number": "PO-1001",
        "status": "APPROVED",
        "supplier": "ABC Supplies",
        "amount": 125000,
    }

    llm_client.chat.assert_called_once()

    http_client.close()


def test_chat_rejects_unauthorized_user() -> None:
    llm_client = Mock(spec=OllamaClient)

    registry = create_default_registry()

    llm_service = LlmService(
        client=llm_client,
        parser=LlmResponseParser(),
        domain_registry=registry,
    )

    ords_client = Mock(spec=OrdsClient)

    tool_catalog = ToolCatalog(
        ords_client=ords_client,
        domain_registry=registry,
    )

    orchestrator = OrchestratorLoop(tool_catalog)

    security_boundary = SecurityBoundary(
        authentication=AuthenticationService(),
        authorization=AuthorizationService(
            allowed_capabilities=set(),
        ),
    )

    service = ChatService(
        llm_service=llm_service,
        orchestrator=orchestrator,
        security_boundary=security_boundary,
    )

    with pytest.raises(Exception, match="not authorized"):
        service.handle_message(
            message="Show me PO-1001.",
            identity={"username": "POC_USER"},
        )

    llm_client.chat.assert_not_called()
    ords_client.get_entity.assert_not_called()
