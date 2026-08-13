import pytest

from oracle_ebs_chatbot.security.auth import AuthenticationService


def test_authenticate_builds_user_context() -> None:
    service = AuthenticationService()

    context = service.authenticate(
        {
            "username": " SYSADMIN ",
            "responsibility": " System Administrator ",
            "role": " APPLICATION_ADMIN ",
            "organization": " Vision Operations ",
        }
    )

    assert context.username == "SYSADMIN"
    assert context.responsibility == "System Administrator"
    assert context.role == "APPLICATION_ADMIN"
    assert context.organization == "Vision Operations"


def test_authenticate_allows_optional_context() -> None:
    service = AuthenticationService()

    context = service.authenticate(
        {
            "username": "SYSADMIN",
        }
    )

    assert context.username == "SYSADMIN"
    assert context.responsibility is None
    assert context.role is None
    assert context.organization is None


def test_authenticate_rejects_missing_username() -> None:
    service = AuthenticationService()

    with pytest.raises(
        ValueError,
        match="authenticated identity must contain a username",
    ):
        service.authenticate({})


def test_authenticate_rejects_empty_username() -> None:
    service = AuthenticationService()

    with pytest.raises(
        ValueError,
        match="authenticated identity must contain a username",
    ):
        service.authenticate({"username": "   "})


def test_authenticate_rejects_non_string_context_value() -> None:
    service = AuthenticationService()

    with pytest.raises(
        ValueError,
        match="identity context values must be strings",
    ):
        service.authenticate(
            {
                "username": "SYSADMIN",
                "role": 123,
            }
        )
