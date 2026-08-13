"""Authorization checks for chatbot capabilities."""

from oracle_ebs_chatbot.security.user_context import UserContext


class AuthorizationService:
    """Determine whether a user can invoke a chatbot capability."""

    def __init__(self, allowed_capabilities: set[str] | None = None) -> None:
        self._allowed_capabilities = allowed_capabilities or set()

    def can_invoke(
        self,
        user: UserContext,
        capability: str,
    ) -> bool:
        """Return whether the user can invoke the requested capability."""
        if not user.username:
            return False

        return capability in self._allowed_capabilities

    def authorize(
        self,
        user: UserContext,
        capability: str,
    ) -> None:
        """Raise an error when the user cannot invoke a capability."""
        from oracle_ebs_chatbot.core.errors import AuthorizationError

        if not self.can_invoke(user, capability):
            raise AuthorizationError(
                f"User '{user.username}' is not authorized "
                f"to invoke '{capability}'."
            )
