from oracle_ebs_chatbot.security.user_context import UserContext


def test_user_context_contains_ebs_identity() -> None:
    context = UserContext(
        username="SYSADMIN",
        responsibility="System Administrator",
        role="APPLICATION_ADMIN",
        organization="Vision Operations",
    )

    assert context.username == "SYSADMIN"
    assert context.responsibility == "System Administrator"
    assert context.role == "APPLICATION_ADMIN"
    assert context.organization == "Vision Operations"


def test_optional_security_context_defaults_to_none() -> None:
    context = UserContext(username="SYSADMIN")

    assert context.username == "SYSADMIN"
    assert context.responsibility is None
    assert context.role is None
    assert context.organization is None
