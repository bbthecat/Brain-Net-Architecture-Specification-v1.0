"""
tests/unit/test_daft.py — Unit Tests: DAFTValidator + DomainInterface
Sprint 3 | Owner: เจม + บี

Tests: all 4 domains, range checks, dimension checks, consent checks, timing
"""

import time
import numpy as np
import pytest
from src.daft.domain_interface import Domain, DomainInterface, MathSymbol
from src.daft.daft_validator import DAFTValidator, ValidationResult


# ── DomainInterface Tests ────────────────────────────────────────────────────

class TestDomainInterface:

    def setup_method(self):
        self.di = DomainInterface()

    # ── Neuro Domain ─────────────────────────────────────────────────────────

    def test_neuro_focus(self):
        sym = self.di.map(Domain.NEURO, "focus", consent_score=0.9)
        assert sym.symbol_name == "focus"
        assert sym.symbol_id   == 0
        assert sym.domain      == Domain.NEURO
        assert len(sym.vector) == 4
        assert sym.vector[0]   == 1.0   # one-hot

    def test_neuro_relax(self):
        sym = self.di.map(Domain.NEURO, "relax")
        assert sym.symbol_name == "relax"
        assert sym.vector[1]   == 1.0

    def test_neuro_reject(self):
        sym = self.di.map(Domain.NEURO, "reject")
        assert sym.symbol_name == "reject"
        assert sym.vector[2]   == 1.0

    def test_neuro_unknown_defaults_to_neutral(self):
        sym = self.di.map(Domain.NEURO, "unknown_state")
        assert sym.symbol_name == "neutral"
        assert sym.symbol_id   == 3

    # ── Bio Domain ───────────────────────────────────────────────────────────

    def test_bio_produces_valid_symbol(self):
        firing_rates = np.random.rand(64)
        sym = self.di.map(Domain.BIO, firing_rates, consent_score=0.85)
        assert sym.domain  == Domain.BIO
        assert len(sym.vector) == 64
        assert 0 <= sym.confidence <= 1.0

    def test_bio_vector_normalized(self):
        firing_rates = np.array([10.0, 20.0, 5.0, 1.0])
        sym = self.di.map(Domain.BIO, firing_rates)
        assert np.all(sym.vector <= 1.0)
        assert np.all(sym.vector >= 0.0)

    # ── Physical Domain ──────────────────────────────────────────────────────

    def test_phy_produces_valid_symbol(self):
        eeg = np.random.rand(14, 32)
        sym = self.di.map(Domain.PHY, eeg, consent_score=0.8)
        assert sym.domain == Domain.PHY
        assert len(sym.vector) <= 32

    def test_phy_vector_in_0_to_1(self):
        eeg = np.random.rand(14, 32) * 100
        sym = self.di.map(Domain.PHY, eeg)
        # After normalization, vector should be in [0,1]
        assert np.all(sym.vector >= 0.0)
        assert np.all(sym.vector <= 1.0)

    # ── Quantum Domain ───────────────────────────────────────────────────────

    def test_quantum_produces_valid_symbol(self):
        state = np.random.randn(8) + 1j * np.random.randn(8)
        state /= np.linalg.norm(state)
        sym = self.di.map(Domain.QUANTUM, state, consent_score=0.9)
        assert sym.domain == Domain.QUANTUM
        assert abs(sym.vector.sum() - 1.0) < 1e-5   # probabilities sum to 1

    # ── Timing Constraint ────────────────────────────────────────────────────

    def test_mapping_under_5ms(self):
        """DAFT mapping must complete < 5ms (BNET-301 AC)."""
        for domain, raw in [
            (Domain.NEURO, "focus"),
            (Domain.BIO, np.random.rand(64)),
            (Domain.PHY, np.random.rand(14, 32)),
            (Domain.QUANTUM, (np.random.randn(8) + 1j*np.random.randn(8))),
        ]:
            t0 = time.perf_counter()
            self.di.map(domain, raw)
            elapsed = (time.perf_counter() - t0) * 1000
            assert elapsed < 5.0, f"{domain} mapping took {elapsed:.2f}ms"

    # ── MathSymbol Validity ──────────────────────────────────────────────────

    def test_symbol_is_valid(self):
        sym = self.di.map(Domain.NEURO, "focus", consent_score=0.9)
        assert sym.is_valid() is True

    def test_invalid_symbol_with_nan(self):
        sym = MathSymbol(
            domain=Domain.NEURO, symbol_id=0, symbol_name="focus",
            vector=np.array([1.0, np.nan, 0.0, 0.0]),
            consent_score=0.9, confidence=1.0
        )
        assert sym.is_valid() is False


# ── DAFTValidator Tests ──────────────────────────────────────────────────────

class TestDAFTValidator:

    def setup_method(self):
        self.di  = DomainInterface()
        self.val = DAFTValidator()

    def _neuro_sym(self, consent=0.85) -> MathSymbol:
        return self.di.map(Domain.NEURO, "focus", consent_score=consent)

    def test_valid_neuro_passes(self):
        sym = self._neuro_sym()
        result = self.val.validate(sym)
        assert result.status == "PASS"

    def test_valid_bio_passes(self):
        sym = self.di.map(Domain.BIO, np.random.rand(64), consent_score=0.85)
        result = self.val.validate(sym)
        assert result.status == "PASS"

    def test_valid_quantum_passes(self):
        state = np.random.randn(8) + 1j*np.random.randn(8)
        state /= np.linalg.norm(state)
        sym = self.di.map(Domain.QUANTUM, state, consent_score=0.9)
        result = self.val.validate(sym)
        assert result.status == "PASS"

    def test_fails_low_consent(self):
        sym = self._neuro_sym(consent=0.4)
        result = self.val.validate(sym)
        assert result.status == "FAIL"
        assert "Consent" in result.message

    def test_fails_nan_vector(self):
        sym = MathSymbol(
            domain=Domain.NEURO, symbol_id=0, symbol_name="focus",
            vector=np.array([1.0, np.nan, 0.0, 0.0]),
            consent_score=0.9, confidence=1.0
        )
        result = self.val.validate(sym)
        assert result.status == "FAIL"

    def test_fails_out_of_range_values(self):
        sym = MathSymbol(
            domain=Domain.BIO, symbol_id=0, symbol_name="focus",
            vector=np.array([1e8, 2e8]),   # way outside range
            consent_score=0.9, confidence=1.0
        )
        result = self.val.validate(sym)
        assert result.status == "FAIL"

    def test_daft_pass_rate_target(self):
        """Quality gate: DAFT Pass Rate ≥ 95% for normal inputs."""
        passes = 0
        total  = 100
        for _ in range(total):
            sym = self._neuro_sym(consent=0.9)
            if self.val.validate(sym).status == "PASS":
                passes += 1
        assert passes / total >= 0.95
