"""Security boundary for chatbot requests."""

from typing import Any

from oracle_ebs_chatbot.security.auth import AuthenticationService
from oracle_ebs_chatbot.security.authorization import AuthorizationService
from oracle_ebs_chatbot.security.input_validation import validate_chat_request
from oracle_ebs_chatbot.security.prompt_injection import validate_prompt
from oracle_ebs_chatbot.security.user_context import UserContext


class SecurityBoundary:
    """Validate identity, input, and capability access before chat execution."""

    def __init__(
        self,
        authentication: AuthenticationService,
        authorization: AuthorizationService,
    ) -> None:
        self.authentication = authentication
        self.authorization = authorization

    def authenticate_and_validate(
        self,
        identity: dict[str, Any],
        message: str,
        capability: str,
    ) -> tuple[UserContext, str]:
        """Authenticate the user and validate the requested operation."""

        user = self.authentication.authenticate(identity)

        request = validate_chat_request(message)

        validated_message = validate_prompt(request.message)

        self.authorization.authorize(
            user,
            capability,
        )

        return user, validated_message
