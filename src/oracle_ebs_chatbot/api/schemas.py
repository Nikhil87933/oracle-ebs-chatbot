"""API request and response models."""

from typing import Any

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """User chat request."""

    message: str


class ChatResponse(BaseModel):
    """Chat execution response."""

    success: bool
    data: Any = None
    error: str | None = None
