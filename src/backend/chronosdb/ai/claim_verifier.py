"""Verify every narrative claim against the engine output it cites.

A claim is only ``VERIFIED`` when the figures it states can be found in the impact,
simulation, optimisation or evidence output it points at. A claim that cites nothing,
cites an unknown source, or states a value absent from that source is ``REJECTED``.
When there is nothing to check the result is ``UNVERIFIED`` — never ``VERIFIED``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

VERIFIED = "VERIFIED"
UNVERIFIED = "UNVERIFIED"
REJECTED = "REJECTED"

KNOWN_SOURCES = ("IMPACT", "SIMULATION", "OPTIMIZATION", "EVIDENCE", "CONSTRAINT")

_NUMBER = re.compile(r"\d+(?:[.,]\d+)*")


@dataclass
class Claim:
    """One statement produced by the narration layer."""

    text: str
    source: str = ""


@dataclass
class VerificationResult:
    status: str
    verified_claims: list[Claim] = field(default_factory=list)
    rejected_claims: list[Claim] = field(default_factory=list)
    unverified_claims: list[Claim] = field(default_factory=list)


def _normalise_number(token: str) -> str:
    cleaned = token.replace(",", "")
    try:
        return str(int(float(cleaned)))
    except ValueError:
        return cleaned


def _collect(value: Any, numbers: set[str], texts: list[str], depth: int = 0) -> None:
    """Walk an engine result and gather every number and string it contains."""

    if depth > 8:
        return
    if isinstance(value, bool):
        texts.append(str(value).lower())
    elif isinstance(value, (int, float)):
        numbers.add(_normalise_number(str(value)))
    elif isinstance(value, str):
        texts.append(value.lower())
        for token in _NUMBER.findall(value):
            numbers.add(_normalise_number(token))
    elif isinstance(value, dict):
        for key, item in value.items():
            texts.append(str(key).lower())
            _collect(item, numbers, texts, depth + 1)
    elif isinstance(value, (list, tuple, set)):
        for item in value:
            _collect(item, numbers, texts, depth + 1)
    elif value is not None and hasattr(value, "__dict__"):
        _collect(vars(value), numbers, texts, depth + 1)


def _sources(impact: Any, simulation: Any, optimization: Any, evidence: Any) -> dict[str, Any]:
    return {
        "IMPACT": impact,
        "SIMULATION": simulation,
        "OPTIMIZATION": optimization,
        "EVIDENCE": evidence,
        "CONSTRAINT": optimization,
    }


class ClaimVerifier:
    """Checks narrative claims against the engine output that produced them."""

    def verify(
        self,
        narration: Any,
        optimization: Any = None,
        impact: Any = None,
        simulation: Any = None,
        evidence: Any = None,
    ) -> VerificationResult:
        claims: list[Claim] = list(getattr(narration, "claims", None) or [])
        if not claims:
            return VerificationResult(status=UNVERIFIED)

        outputs = _sources(impact, simulation, optimization, evidence)

        verified: list[Claim] = []
        rejected: list[Claim] = []
        unverified: list[Claim] = []

        for claim in claims:
            if not isinstance(claim, Claim) or not claim.text.strip():
                rejected.append(claim) if isinstance(claim, Claim) else None
                continue

            source = (claim.source or "").upper()
            if source not in KNOWN_SOURCES or outputs.get(source) is None:
                unverified.append(claim)
                continue

            numbers: set[str] = set()
            texts: list[str] = []
            _collect(outputs[source], numbers, texts)

            stated = {_normalise_number(token) for token in _NUMBER.findall(claim.text)}

            if stated and stated.issubset(numbers):
                verified.append(claim)
                continue

            haystack = " ".join(texts)
            if not stated and claim.text.strip().lower() in haystack:
                verified.append(claim)
                continue

            rejected.append(claim)

        if rejected:
            status = REJECTED
        elif unverified:
            status = UNVERIFIED
        elif verified:
            status = VERIFIED
        else:
            status = UNVERIFIED

        return VerificationResult(
            status=status,
            verified_claims=verified,
            rejected_claims=rejected,
            unverified_claims=unverified,
        )


__all__ = [
    "Claim",
    "ClaimVerifier",
    "REJECTED",
    "UNVERIFIED",
    "VERIFIED",
    "VerificationResult",
]
