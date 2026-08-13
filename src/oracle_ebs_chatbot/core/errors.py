"""Application-level error types and API error models."""

from pydantic import BaseModel


class ChatbotError(Exception):
    """Base exception for expected application-level failures."""

    code = "CHATBOT_ERROR"
    status_code = 500

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ValidationError(ChatbotError):
    """Raised when an application request fails validation."""

    code = "VALIDATION_ERROR"
    status_code = 400


class AuthorizationError(ChatbotError):
    """Raised when a user is not authorized for an operation."""

    code = "AUTHORIZATION_DENIED"
    status_code = 403


class ToolError(ChatbotError):
    """Raised when a chatbot capability cannot execute successfully."""

    code = "TOOL_ERROR"
    status_code = 500


class ExternalServiceError(ChatbotError):
    """Raised when an external dependency such as ORDS fails."""

    code = "EXTERNAL_SERVICE_ERROR"
    status_code = 502


class ErrorDetail(BaseModel):
    """Standard API error payload."""

    code: str
    message: str


class ErrorResponse(BaseModel):
    """Standard API error response."""

    error: ErrorDetail
