import pytest

from oracle_ebs_chatbot.core.errors import AuthorizationError
from oracle_ebs_chatbot.security.authorization import AuthorizationService
from oracle_ebs_chatbot.security.user_context import UserContext


def test_authorized_user_can_invoke_capability() -> None:
    user = UserContext(username="SYSADMIN")

    authorization = AuthorizationService(
        allowed_capabilities={"entity_lookup"},
    )

    assert authorization.can_invoke(user, "entity_lookup") is True


def test_user_cannot_invoke_unapproved_capability() -> None:
    user = UserContext(username="SYSADMIN")

    authorization = AuthorizationService(
        allowed_capabilities={"entity_lookup"},
    )

    assert authorization.can_invoke(user, "aggregate_query") is False


def test_authorize_allows_approved_capability() -> None:
    user = UserContext(username="SYSADMIN")

    authorization = AuthorizationService(
        allowed_capabilities={"entity_lookup"},
    )

    authorization.authorize(user, "entity_lookup")


def test_authorize_raises_for_denied_capability() -> None:
    user = UserContext(username="SYSADMIN")

    authorization = AuthorizationService(
        allowed_capabilities={"entity_lookup"},
    )

    with pytest.raises(
        AuthorizationError,
        match="not authorized",
    ):
        authorization.authorize(user, "aggregate_query")


def test_empty_username_is_denied() -> None:
    user = UserContext(username="")

    authorization = AuthorizationService(
        allowed_capabilities={"entity_lookup"},
    )

    assert authorization.can_invoke(user, "entity_lookup") is False
