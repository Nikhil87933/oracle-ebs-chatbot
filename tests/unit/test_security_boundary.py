import pytest

from oracle_ebs_chatbot.core.errors import AuthorizationError
from oracle_ebs_chatbot.security.auth import AuthenticationService
from oracle_ebs_chatbot.security.authorization import AuthorizationService


def test_authenticated_user_can_be_authorized() -> None:
    authentication = AuthenticationService()
    authorization = AuthorizationService(
        allowed_capabilities={"entity_lookup"},
    )

    user = authentication.authenticate(
        {
            "username": "SYSADMIN",
            "responsibility": "System Administrator",
            "role": "APPLICATION_ADMIN",
            "organization": "Vision Operations",
        }
    )

    authorization.authorize(user, "entity_lookup")


def test_authenticated_user_can_be_denied() -> None:
    authentication = AuthenticationService()
    authorization = AuthorizationService(
        allowed_capabilities={"entity_lookup"},
    )

    user = authentication.authenticate(
        {
            "username": "SYSADMIN",
            "responsibility": "System Administrator",
        }
    )

    with pytest.raises(AuthorizationError, match="not authorized"):
        authorization.authorize(user, "aggregate_query")


def test_invalid_identity_never_reaches_authorization() -> None:
    authentication = AuthenticationService()
    authorization = AuthorizationService(
        allowed_capabilities={"entity_lookup"},
    )

    with pytest.raises(ValueError):
        user = authentication.authenticate({})

        authorization.authorize(user, "entity_lookup")
