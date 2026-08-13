from unittest.mock import patch

import httpx

from oracle_ebs_chatbot.llm.ollama_client import OllamaClient


def test_ollama_client_sends_chat_request() -> None:
    client = OllamaClient(
        host="http://ollama:11434",
        model="qwen",
    )

    request = httpx.Request(
        "POST",
        "http://ollama:11434/api/chat",
    )

    mock_response = httpx.Response(
        200,
        request=request,
        json={
            "message": {
                "role": "assistant",
                "content": "Hello",
            }
        },
    )

    with patch(
        "oracle_ebs_chatbot.llm.ollama_client.httpx.post",
        return_value=mock_response,
    ) as mock_post:
        result = client.chat([{"role": "user", "content": "Hello"}])

    mock_post.assert_called_once_with(
        "http://ollama:11434/api/chat",
        json={
            "model": "qwen",
            "messages": [
                {"role": "user", "content": "Hello"},
            ],
            "stream": False,
        },
        timeout=60.0,
    )

    assert result["message"]["content"] == "Hello"


def test_ollama_client_raises_for_http_error() -> None:
    client = OllamaClient(
        host="http://ollama:11434",
        model="qwen",
    )

    request = httpx.Request(
        "POST",
        "http://ollama:11434/api/chat",
    )

    mock_response = httpx.Response(
        500,
        request=request,
        json={"error": "server error"},
    )

    with patch(
        "oracle_ebs_chatbot.llm.ollama_client.httpx.post",
        return_value=mock_response,
    ):
        try:
            client.chat([{"role": "user", "content": "Hello"}])
        except httpx.HTTPStatusError as exc:
            assert exc.response.status_code == 500
        else:
            raise AssertionError("Expected HTTPStatusError")
