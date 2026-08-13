"""Client for communicating with Ollama."""

from typing import Any, cast

import httpx


class OllamaClient:
    """HTTP client for the Ollama API."""

    def __init__(
        self,
        host: str,
        model: str,
        timeout: float = 60.0,
    ) -> None:
        self.host = host.rstrip("/")
        self.model = model
        self.timeout = timeout

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Send a chat request to Ollama."""
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }

        if tools:
            payload["tools"] = tools

        response = httpx.post(
            f"{self.host}/api/chat",
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()

        return cast(dict[str, Any], response.json())
