"""Schemas used by the orchestration layer."""

from typing import Any

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """Structured instruction produced by the LLM."""

    tool: str = Field(min_length=1)
    parameters: dict[str, Any] = Field(default_factory=dict)
