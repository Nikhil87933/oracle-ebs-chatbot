"""Shared interfaces for chatbot tools."""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class ToolResult(BaseModel):
    """Standard result returned by a chatbot tool."""

    success: bool
    data: Any = None
    error: str | None = None


class BaseTool(ABC):
    """Common interface for all chatbot tools."""

    name: str
    description: str

    @abstractmethod
    def validate(self, parameters: dict[str, Any]) -> None:
        """Validate tool parameters before execution."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, parameters: dict[str, Any]) -> ToolResult:
        """Validate and execute the tool."""
        raise NotImplementedError
