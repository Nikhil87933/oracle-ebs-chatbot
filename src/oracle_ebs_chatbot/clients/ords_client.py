"""HTTP client for communicating with Oracle REST Data Services (ORDS)."""

from typing import Any

import httpx

from oracle_ebs_chatbot.config.settings import Settings, get_settings


class OrdsClient:
    """HTTP client for the ORDS backend."""

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float | None = None,
        headers: dict[str, str] | None = None,
        settings: Settings | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        runtime_settings = settings or get_settings()

        self.base_url = (
            base_url if base_url is not None else runtime_settings.ords_base_url
        ).rstrip("/")

        self.timeout = (
            timeout if timeout is not None else runtime_settings.ords_timeout_seconds
        )

        self.headers = headers or {}
        self.http_client = http_client or httpx.Client()

    def get_entity(
        self,
        entity: str,
        identifier: str,
    ) -> dict[str, Any]:
        """Fetch a single entity from ORDS."""

        response = self.http_client.get(
            f"{self.base_url}/{entity}/{identifier}",
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()

        data = response.json()

        if not isinstance(data, dict):
            raise ValueError("ORDS entity response must be an object")

        return data

    def aggregate(
        self,
        metric: str,
        dimensions: list[str],
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Execute an aggregate request through ORDS."""

        response = self.http_client.post(
            f"{self.base_url}/aggregate",
            headers=self.headers,
            json={
                "metric": metric,
                "dimensions": dimensions,
                "filters": filters,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()

        data = response.json()

        if not isinstance(data, list):
            raise ValueError("ORDS aggregate response must be a list")

        return data
