"""Authentication boundary for EBS user identity."""

from typing import Any

from oracle_ebs_chatbot.security.user_context import UserContext


class AuthenticationService:
    """Convert an external identity artifact into UserContext."""

    def authenticate(self, identity: dict[str, Any]) -> UserContext:
        """Build a user context from an authenticated identity artifact."""
        username = identity.get("username")

        if not isinstance(username, str) or not username.strip():
            raise ValueError("authenticated identity must contain a username")

        return UserContext(
            username=username.strip(),
            responsibility=self._optional_string(identity.get("responsibility")),
            role=self._optional_string(identity.get("role")),
            organization=self._optional_string(identity.get("organization")),
        )

    @staticmethod
    def _optional_string(value: Any) -> str | None:
        """Return a normalized optional string."""
        if value is None:
            return None

        if not isinstance(value, str):
            raise ValueError("identity context values must be strings")

        value = value.strip()

        return value or None
