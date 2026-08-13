"""Input validation for chatbot requests."""

from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    """Validated chatbot request."""

    message: str = Field(..., min_length=1, max_length=4000)

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        """Reject messages containing only whitespace."""
        value = value.strip()

        if not value:
            raise ValueError("message must not be empty")

        return value


def validate_chat_request(message: str) -> ChatRequest:
    """Validate and normalize a raw chatbot message."""
    return ChatRequest(message=message)
