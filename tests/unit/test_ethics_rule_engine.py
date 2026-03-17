"""
tests/unit/test_ethics_rule_engine.py — Unit Tests: EthicsRuleEngine
Sprint 3 | Owner: โอเล่

Tests: E-001 to E-005 rules, EthicsDecision outcomes, audit log integration
"""

import pytest
from unittest.mock import MagicMock, patch
from src.security.ethics_rule_engine import EthicsRuleEngine, EthicsDecision
from src.protocol.ttp_packet import TTPHeader, TTPPacket


def _make_packet(consent=0.85, arousal=0.3, valence=0.2,
                 symbol="focus", domain="neuro") -> TTPPacket:
    header = TTPHeader(source_id="NODE_A", dest_id="NODE_B", symbol_id=0)
    return TTPPacket(
        header=header, symbol=symbol,
        valence=valence, arousal=arousal,
        intensity=0.7, consent_score=consent,
        domain=domain,
    )


class TestEthicsRuleEngine:

    def setup_method(self):
        self.engine = EthicsRuleEngine()

    # ── E-001: Consent Score ─────────────────────────────────────────────────

    def test_e001_allows_sufficient_consent(self):
        pkt = _make_packet(consent=0.75)
        result = self.engine.evaluate(pkt)
        assert result.decision == EthicsDecision.ALLOW

    def test_e001_blocks_low_consent(self):
        pkt = _make_packet(consent=0.65)
        result = self.engine.evaluate(pkt)
        assert result.decision == EthicsDecision.BLOCK
        assert result.rule_id == "E-001"

    def test_e001_blocks_zero_consent(self):
        pkt = _make_packet(consent=0.0)
        result = self.engine.evaluate(pkt)
        assert result.decision == EthicsDecision.BLOCK

    # ── E-002: Private Thought Boundary ─────────────────────────────────────

    def test_e002_blocks_private_symbol(self):
        pkt = _make_packet(symbol="private_memory_recall", consent=0.9)
        result = self.engine.evaluate(pkt)
        assert result.decision == EthicsDecision.BLOCK
        assert result.rule_id == "E-002"

    def test_e002_allows_normal_symbol(self):
        pkt = _make_packet(symbol="focus", consent=0.9)
        result = self.engine.evaluate(pkt)
        assert result.decision == EthicsDecision.ALLOW

    # ── E-003: Coercion ──────────────────────────────────────────────────────

    def test_e003_hitl_on_panic_arousal(self):
        pkt = _make_packet(arousal=0.95, consent=0.85)
        result = self.engine.evaluate(pkt)
        assert result.decision == EthicsDecision.HITL
        assert result.rule_id == "E-003"

    def test_e003_hitl_on_extreme_negative_valence(self):
        pkt = _make_packet(valence=-0.75, consent=0.85)
        result = self.engine.evaluate(pkt)
        assert result.decision == EthicsDecision.HITL

    def test_e003_allows_acceptable_state(self):
        pkt = _make_packet(arousal=0.5, valence=0.0, consent=0.85)
        result = self.engine.evaluate(pkt)
        assert result.decision == EthicsDecision.ALLOW

    # ── Rule Set Completeness ────────────────────────────────────────────────

    def test_engine_loads_5_rules(self):
        assert len(self.engine.rules) == 5

    def test_all_rule_ids_present(self):
        for rule_id in ["E-001", "E-002", "E-003", "E-004", "E-005"]:
            assert rule_id in self.engine.rules

    # ── Audit Log Integration ────────────────────────────────────────────────

    def test_every_evaluation_creates_audit_entry(self):
        pkt = _make_packet()
        self.engine.evaluate(pkt)
        self.engine.evaluate(pkt)
        assert len(self.engine._audit.entries) == 2

    def test_audit_chain_valid_after_evaluations(self):
        for _ in range(10):
            pkt = _make_packet()
            self.engine.evaluate(pkt)
        assert self.engine._audit.verify_chain() is True

    # ── Ethics Compliance Rate ───────────────────────────────────────────────

    def test_ethics_compliance_rate_all_pass(self):
        """100 valid packets → 100% compliance (MVP gate)."""
        passes = 0
        for _ in range(100):
            pkt = _make_packet(consent=0.9, arousal=0.3, valence=0.2)
            result = self.engine.evaluate(pkt)
            if result.decision == EthicsDecision.ALLOW:
                passes += 1
        assert passes / 100 >= 0.99
