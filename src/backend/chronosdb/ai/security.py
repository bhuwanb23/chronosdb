"""Prompt-injection defence for the narration surface.

The narrative layer is allowed to explain engine output, never to change policy or
results. Anything that looks like an override attempt is rejected before it reaches
narration, and the caller is told why.

Principles encoded here:

* documents cannot create policy,
* users cannot override constraints,
* prompts cannot modify computed results.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

MAX_QUERY_LENGTH = 2000

_OVERRIDE_PATTERNS = (
    re.compile(
        r"ignore\s+(?:all\s+|every\s+|any\s+|the\s+)*(?:previous|prior|above|earlier)?\s*"
        r"(?:instructions?|prompts?|polic(?:y|ies)|rules?|constraints?)",
        re.IGNORECASE,
    ),
    re.compile(r"disregard\s+.{0,40}(?:instruction|policy|rule|constraint)", re.IGNORECASE),
    re.compile(r"(?:forget|override|bypass)\s+.{0,20}(?:instruction|policy|rule|constraint)", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+", re.IGNORECASE),
    re.compile(r"act\s+as\s+(?:an?\s+)?(?:admin|administrator|system|root|developer)", re.IGNORECASE),
    re.compile(r"(?:approve|authori[sz]e|whitelist)\s+(?:any|all|every)\s+supplier", re.IGNORECASE),
    re.compile(
        r"(?:change|set|increase|reduce|edit)\s+(?:the\s+)?(?:revenue|sla|cost|budget|result|hash)",
        re.IGNORECASE,
    ),
    re.compile(r"(?:reveal|print|show|output)\s+.{0,25}(?:system\s+prompt|instructions|api\s*key|secret)", re.IGNORECASE),
    re.compile(r"<\|[^>]{0,40}\|>"),
    re.compile(r"\{\{.{0,80}\}\}"),
    re.compile(r"```\s*(?:system|assistant)"),
)

_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


@dataclass(frozen=True)
class SecurityResult:
    """Outcome of a guardrail check."""

    status: str
    reason: str = ""

    @property
    def blocked(self) -> bool:
        return self.status != "ALLOWED"


class PromptRejectedError(ValueError):
    """Raised when a query fails the guardrail."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class PromptSecurityLayer:
    """Rejects queries that try to rewrite policy, constraints or results."""

    def check_prompt(self, user_query: str) -> SecurityResult:
        if not isinstance(user_query, str) or not user_query.strip():
            return SecurityResult("BLOCKED", "Query is empty")

        if len(user_query) > MAX_QUERY_LENGTH:
            return SecurityResult("BLOCKED", f"Query exceeds {MAX_QUERY_LENGTH} characters")

        if _CONTROL_CHARS.search(user_query):
            return SecurityResult("BLOCKED", "Query contains control characters")

        for pattern in _OVERRIDE_PATTERNS:
            if pattern.search(user_query):
                return SecurityResult("BLOCKED", "Policy or constraint override attempt detected")

        return SecurityResult("ALLOWED")


__all__ = ["PromptRejectedError", "PromptSecurityLayer", "SecurityResult"]
