from oracle_ebs_chatbot.core.errors import (
    AuthorizationError,
    ChatbotError,
    ErrorDetail,
    ErrorResponse,
    ExternalServiceError,
    ToolError,
    ValidationError,
)


def test_chatbot_error_contains_message() -> None:
    error = ChatbotError("Something went wrong.")

    assert str(error) == "Something went wrong."
    assert error.message == "Something went wrong."
    assert error.code == "CHATBOT_ERROR"
    assert error.status_code == 500


def test_validation_error() -> None:
    error = ValidationError("Invalid request.")

    assert error.code == "VALIDATION_ERROR"
    assert error.status_code == 400
    assert error.message == "Invalid request."


def test_authorization_error() -> None:
    error = AuthorizationError("Access denied.")

    assert error.code == "AUTHORIZATION_DENIED"
    assert error.status_code == 403
    assert error.message == "Access denied."


def test_tool_error() -> None:
    error = ToolError("Tool execution failed.")

    assert error.code == "TOOL_ERROR"
    assert error.status_code == 500
    assert error.message == "Tool execution failed."


def test_external_service_error() -> None:
    error = ExternalServiceError("ORDS unavailable.")

    assert error.code == "EXTERNAL_SERVICE_ERROR"
    assert error.status_code == 502
    assert error.message == "ORDS unavailable."


def test_error_response_model() -> None:
    response = ErrorResponse(
        error=ErrorDetail(
            code="VALIDATION_ERROR",
            message="Invalid request.",
        )
    )

    assert response.error.code == "VALIDATION_ERROR"
    assert response.error.message == "Invalid request."
