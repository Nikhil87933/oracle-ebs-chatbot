"""User context for authenticated EBS users."""

from pydantic import BaseModel


class UserContext(BaseModel):
    """Identity and EBS security context for the current user."""

    username: str
    responsibility: str | None = None
    role: str | None = None
    organization: str | None = None
