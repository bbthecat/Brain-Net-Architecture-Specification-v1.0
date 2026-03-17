"""
tests/integration/test_daft_pipeline.py — Integration Tests: DAFT Layer + TTP Pipeline
Sprint 3 | Owner: เจม + บี

Tests: Domain mapping → DAFT validation → TTP packet assembly → encryption
"""

import numpy as np
import pytest
from src.daft.domain_interface import Domain, DomainInterface
from src.daft.daft_validator import DAFTValidator
from src.protocol.ttp_packet import TTPHeader, TTPPacket
from src.security.brain_firewall import BrainFirewall
from src.security.ethics_rule_engine import EthicsRuleEngine, EthicsDecision
from src.crypto.mock_qkd_aes import MockQKD


def _name_to_id(name: str) -> int:
    return {"focus": 0, "relax": 1, "reject": 2, "neutral": 3}.get(name, 3)


class TestDAFTPipeline:
    """
    Integration tests: full flow from raw domain input → encrypted TTP packet
    """

    def setup_method(self):
        self.di       = DomainInterface()
        self.validator = DAFTValidator()
        self.firewall = BrainFirewall()
        self.ethics   = EthicsRuleEngine()
        self.qkd      = MockQKD(reuse_key=True)

    def _domain_to_packet(self, domain: Domain, raw_input,
                          consent: float = 0.9) -> TTPPacket:
        """Helper: map → validate → assemble TTP packet."""
        sym = self.di.map(domain, raw_input, consent_score=consent)
        val = self.validator.validate(sym)
        assert val.status == "PASS", f"Validation failed: {val.message}"

        header = TTPHeader(
            source_id="NODE_A", dest_id="NODE_B",
            symbol_id=_name_to_id(sym.symbol_name)
        )
        return TTPPacket(
            header=header, symbol=sym.symbol_name,
            valence=0.2, arousal=0.3,
            intensity=float(sym.confidence),
            consent_score=consent,
            domain=domain.value,
        )

    # ── Neuro Domain ─────────────────────────────────────────────────────────

    def test_neuro_focus_full_pipeline(self):
        pkt = self._domain_to_packet(Domain.NEURO, "focus")
        assert pkt.symbol == "focus"
        assert pkt.consent_score == 0.9

    def test_neuro_all_symbols_through_ethics(self):
        for state in ["focus", "relax", "reject", "neutral"]:
            pkt = self._domain_to_packet(Domain.NEURO, state)
            result = self.ethics.evaluate(pkt)
            assert result.decision == EthicsDecision.ALLOW

    # ── Bio Domain ───────────────────────────────────────────────────────────

    def test_bio_domain_full_pipeline(self):
        firing_rates = np.random.rand(64)
        pkt = self._domain_to_packet(Domain.BIO, firing_rates)
        assert pkt.domain == "bio"
        fw = self.firewall.evaluate(pkt)
        assert fw.allow is True

    # ── Physical Domain ──────────────────────────────────────────────────────

    def test_phy_domain_full_pipeline(self):
        eeg_matrix = np.random.rand(14, 32)
        pkt = self._domain_to_packet(Domain.PHY, eeg_matrix)
        assert pkt.domain == "phy"

    # ── Quantum Domain ───────────────────────────────────────────────────────

    def test_quantum_domain_full_pipeline(self):
        state = np.random.randn(8) + 1j * np.random.randn(8)
        state /= np.linalg.norm(state)
        pkt = self._domain_to_packet(Domain.QUANTUM, state)
        assert pkt.domain == "quantum"

    # ── All 4 Domains Through Encryption ────────────────────────────────────

    def test_all_domains_encrypt_decrypt(self):
        """All 4 domain packets must survive QKD encrypt/decrypt roundtrip."""
        test_cases = [
            (Domain.NEURO,   "focus"),
            (Domain.BIO,     np.random.rand(64)),
            (Domain.PHY,     np.random.rand(14, 32)),
            (Domain.QUANTUM, (np.random.randn(8) + 1j*np.random.randn(8))),
        ]
        for domain, raw in test_cases:
            pkt = self._domain_to_packet(domain, raw)
            raw_bytes = pkt.pack()
            encrypted = self.qkd.encrypt_packet(raw_bytes)
            decrypted = self.qkd.decrypt_packet(encrypted)
            restored  = TTPPacket.unpack(decrypted)
            assert restored.domain == domain.value, \
                f"Domain mismatch after encrypt/decrypt: {domain}"
            assert abs(restored.consent_score - 0.9) < 0.001

    # ── DAFT Validation Gates ────────────────────────────────────────────────

    def test_daft_rejects_low_consent(self):
        sym = self.di.map(Domain.NEURO, "focus", consent_score=0.4)
        result = self.validator.validate(sym)
        assert result.status == "FAIL"

    def test_daft_rejects_nan_vector(self):
        sym = self.di.map(Domain.NEURO, "focus", consent_score=0.9)
        sym.vector[0] = float('nan')
        result = self.validator.validate(sym)
        assert result.status == "FAIL"

    def test_daft_pass_rate_100_inputs(self):
        """Integration: 100 valid inputs across all domains → ≥95% DAFT pass."""
        passes = 0
        for i in range(100):
            domain = [Domain.NEURO, Domain.BIO, Domain.PHY, Domain.QUANTUM][i % 4]
            if domain == Domain.NEURO:
                raw = "focus"
            elif domain == Domain.BIO:
                raw = np.random.rand(64)
            elif domain == Domain.PHY:
                raw = np.random.rand(14, 32)
            else:
                v = np.random.randn(8) + 1j * np.random.randn(8)
                raw = v / np.linalg.norm(v)
            sym = self.di.map(domain, raw, consent_score=0.9)
            if self.validator.validate(sym).status == "PASS":
                passes += 1
        assert passes / 100 >= 0.95

    # ── Timing Constraints ───────────────────────────────────────────────────

    def test_daft_validation_under_5ms(self):
        """Quality Gate: DAFT validation < 5ms."""
        import time
        sym = self.di.map(Domain.NEURO, "focus", consent_score=0.9)
        t0 = time.perf_counter()
        self.validator.validate(sym)
        elapsed = (time.perf_counter() - t0) * 1000
        assert elapsed < 5.0, f"DAFT took {elapsed:.2f}ms (limit 5ms)"
