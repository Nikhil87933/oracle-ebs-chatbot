import pytest
from pydantic import ValidationError as PydanticValidationError

from oracle_ebs_chatbot.security.input_validation import (
    ChatRequest,
    validate_chat_request,
)


def test_valid_chat_request() -> None:
    request = ChatRequest(message="Show me purchase order 12345")

    assert request.message == "Show me purchase order 12345"


def test_message_is_trimmed() -> None:
    request = ChatRequest(message="  Show me suppliers  ")

    assert request.message == "Show me suppliers"


def test_empty_message_is_rejected() -> None:
    with pytest.raises(PydanticValidationError):
        ChatRequest(message="")


def test_whitespace_message_is_rejected() -> None:
    with pytest.raises(PydanticValidationError):
        ChatRequest(message="   ")


def test_message_over_maximum_length_is_rejected() -> None:
    with pytest.raises(PydanticValidationError):
        ChatRequest(message="x" * 4001)


def test_validate_chat_request() -> None:
    request = validate_chat_request("  Show me invoices  ")

    assert request.message == "Show me invoices"
