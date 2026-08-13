"""Heuristic prompt-injection detection for chatbot messages."""

import re

INJECTION_PATTERNS = (
    r"\bignore\s+(all\s+)?previous\s+instructions\b",
    r"\bignore\s+(all\s+)?prior\s+instructions\b",
    r"\bdisregard\s+(all\s+)?previous\s+instructions\b",
    r"\bdisregard\s+(all\s+)?prior\s+instructions\b",
    r"\bforget\s+(all\s+)?previous\s+instructions\b",
    r"\bforget\s+(all\s+)?prior\s+instructions\b",
    r"\breveal\s+(the\s+)?system\s+prompt\b",
    r"\bshow\s+(me\s+)?(the\s+)?system\s+prompt\b",
    r"\bprint\s+(the\s+)?system\s+prompt\b",
    r"\breveal\s+(your\s+)?instructions\b",
    r"\bshow\s+(me\s+)?(your\s+)?instructions\b",
)

_COMPILED_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE) for pattern in INJECTION_PATTERNS
)


def contains_prompt_injection(message: str) -> bool:
    """Return True when a message matches a known injection pattern."""
    return any(pattern.search(message) for pattern in _COMPILED_PATTERNS)


def validate_prompt(message: str) -> str:
    """Reject messages that match known prompt-injection patterns."""
    if contains_prompt_injection(message):
        raise ValueError("potential prompt injection detected")

    return message
