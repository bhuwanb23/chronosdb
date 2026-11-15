"""API authentication and authorization.

Every business route requires an API key presented as ``X-API-Key``. Keys are
compared in constant time and map to a fixed scope set, so the routes declare the
scope they need instead of trusting the caller.

Credentials come from settings (``CHRONOSDB_API_KEY`` for operators,
``CHRONOSDB_AUDIT_KEY`` for auditors). When neither is configured, the API fails
closed and every protected route answers 401.
"""

from __future__ import annotations

import hmac
from dataclasses import dataclass
from typing import Callable

from fastapi import Depends, Header, HTTPException, status

from chronosdb.config import Settings, get_settings

READ = "read"
WRITE = "write"
AUDIT = "audit"

_OPERATOR_SCOPES = frozenset({READ, WRITE})
_AUDITOR_SCOPES = frozenset({READ, AUDIT})


@dataclass(frozen=True)
class Principal:
    """The authenticated caller and the scopes it is allowed to use."""

    role: str
    scopes: frozenset[str]

    def allows(self, scope: str) -> bool:
        return scope in self.scopes


def _matches(candidate: str | None, expected: str) -> bool:
    """Compare two secrets without leaking length or content through timing."""

    if not candidate or not expected:
        return False
    return hmac.compare_digest(candidate.strip().encode("utf-8"), expected.strip().encode("utf-8"))


def authenticate(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    settings: Settings = Depends(get_settings),
) -> Principal:
    """Resolve the caller from the API key header, or reject the request."""

    if _matches(x_api_key, settings.audit_api_key):
        return Principal(role="auditor", scopes=_AUDITOR_SCOPES)
    if _matches(x_api_key, settings.api_key):
        return Principal(role="operator", scopes=_OPERATOR_SCOPES)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="A valid X-API-Key header is required",
        headers={"WWW-Authenticate": "ApiKey"},
    )


def require_scope(scope: str) -> Callable[..., Principal]:
    """Build a dependency that requires one scope on top of authentication."""

    def dependency(principal: Principal = Depends(authenticate)) -> Principal:
        if not principal.allows(scope):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"The {principal.role} role cannot perform a {scope} operation",
            )
        return principal

    return dependency


__all__ = ["Principal", "READ", "WRITE", "AUDIT", "authenticate", "require_scope"]
