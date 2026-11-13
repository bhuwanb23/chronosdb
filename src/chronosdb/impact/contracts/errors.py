from __future__ import annotations


class ImpactError(Exception):
    """Base error for deterministic impact calculations."""


class ContractError(ImpactError):
    """The request or rule contract is invalid."""


class StateReconstructionError(ImpactError):
    """The requested operational state cannot be reconstructed safely."""


class DisruptionValidationError(ImpactError):
    """The disruption is invalid or outside the supported scope."""
