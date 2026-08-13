"""Structured audit logging."""

import logging
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class AuditEvent(BaseModel):
    """Structured record of a chatbot operation."""

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    request_id: str
    user: str | None = None
    tool: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)
    result: str


class AuditLogger:
    """Application audit logger."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger("oracle_ebs_chatbot.audit")

    def log(self, event: AuditEvent) -> None:
        """Write an audit event as structured JSON."""
        self._logger.info(event.model_dump_json())
