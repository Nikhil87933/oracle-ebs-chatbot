from unittest.mock import patch

from fastapi.testclient import TestClient

from oracle_ebs_chatbot.main import app
from oracle_ebs_chatbot.tools.base import ToolResult

client = TestClient(app)


def test_chat_endpoint_returns_tool_result() -> None:
    with patch(
        "oracle_ebs_chatbot.api.routes_chat.ChatService.handle_message",
        return_value=ToolResult(
            success=True,
            data={"id": "PO-1001"},
        ),
    ):
        response = client.post(
            "/chat",
            json={"message": "Show me PO-1001."},
        )

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": {"id": "PO-1001"},
        "error": None,
    }
