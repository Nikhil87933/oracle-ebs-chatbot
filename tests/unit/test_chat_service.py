from unittest.mock import Mock

from oracle_ebs_chatbot.chat.service import ChatService
from oracle_ebs_chatbot.llm.service import LlmService
from oracle_ebs_chatbot.orchestrator.loop import OrchestratorLoop
from oracle_ebs_chatbot.orchestrator.schemas import ToolCall
from oracle_ebs_chatbot.security.boundary import SecurityBoundary
from oracle_ebs_chatbot.tools.base import ToolResult


def create_service() -> ChatService:
    """Create a chat service with mocked dependencies."""
    llm_service = Mock(spec=LlmService)
    orchestrator = Mock(spec=OrchestratorLoop)
    security_boundary = Mock(spec=SecurityBoundary)

    security_boundary.authenticate_and_validate.return_value = (
        Mock(username="NIKHIL"),
        "Show me PO-1001.",
    )

    llm_service.create_tool_call.return_value = ToolCall(
        tool="entity_lookup",
        parameters={
            "entity": "purchase_order",
            "identifier": "PO-1001",
        },
    )

    orchestrator.execute_tool.return_value = ToolResult(
        success=True,
        data={"id": "PO-1001"},
    )

    return ChatService(
        llm_service=llm_service,
        orchestrator=orchestrator,
        security_boundary=security_boundary,
    )


def test_chat_service_uses_security_boundary() -> None:
    service = create_service()

    result = service.handle_message(
        message="Show me PO-1001.",
        identity={"username": "NIKHIL"},
    )

    assert result.success is True
    assert result.data == {"id": "PO-1001"}


def test_chat_service_sends_validated_message_to_llm() -> None:
    service = create_service()

    service.handle_message(
        message="Show me PO-1001.",
        identity={"username": "NIKHIL"},
    )

    service.llm_service.create_tool_call.assert_called_once_with(
        [
            {
                "role": "user",
                "content": "Show me PO-1001.",
            }
        ]
    )


def test_chat_service_sends_tool_call_to_orchestrator() -> None:
    service = create_service()

    service.handle_message(
        message="Show me PO-1001.",
        identity={"username": "NIKHIL"},
    )

    tool_call = service.llm_service.create_tool_call.return_value

    service.orchestrator.execute_tool.assert_called_once_with(tool_call)
