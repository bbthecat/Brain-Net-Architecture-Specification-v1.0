"""
daft_validator.py — DAFT Validation Engine
Sprint 3 | Owner: เจม (Network Architect)

Validates MathSymbol before entering TTP pipeline.
Checks: Range, Dimension, Consent Score.
"""

from dataclasses import dataclass
from src.daft.domain_interface import MathSymbol, Domain


@dataclass
class ValidationResult:
    status:   str    # PASS | FAIL
    score:    float  # 0.0 – 1.0
    domain:   str
    message:  str


DIMENSION_MAP = {
    Domain.BIO:     (1, 256),    # 1D vector, up to 256 elements
    Domain.PHY:     (1, 1024),   # Flattened tensor up to 1024
    Domain.NEURO:   (4, 4),      # Exactly 4 elements (one-hot)
    Domain.QUANTUM: (1, 512),    # Probability amplitudes
}


class DAFTValidator:
    """
    Domain Adaptive Formalization & Translation Validator.
    Ensures mathematical consistency before TTP entry.
    """

    def validate(self, symbol: MathSymbol) -> ValidationResult:
        checks = [
            self._range_check(symbol),
            self._dimension_check(symbol),
            self._consent_check(symbol),
        ]
        failures = [c for c in checks if c is not None]
        if failures:
            return ValidationResult("FAIL", 0.0, symbol.domain.value, failures[0])

        score = (symbol.consent_score + symbol.confidence) / 2
        return ValidationResult("PASS", score, symbol.domain.value, "OK")

    def _range_check(self, symbol: MathSymbol):
        import numpy as np
        if np.any(symbol.vector < -1e6) or np.any(symbol.vector > 1e6):
            return "Vector values out of acceptable range"
        if not symbol.is_valid():
            return "Symbol contains NaN or invalid values"
        return None

    def _dimension_check(self, symbol: MathSymbol):
        min_d, max_d = DIMENSION_MAP.get(symbol.domain, (1, 9999))
        n = len(symbol.vector)
        if not (min_d <= n <= max_d):
            return f"Dimension {n} out of range [{min_d}, {max_d}] for {symbol.domain.value}"
        return None

    def _consent_check(self, symbol: MathSymbol):
        if symbol.consent_score < 0.5:
            return f"Consent Score {symbol.consent_score:.2f} too low (min 0.5)"
        return None
