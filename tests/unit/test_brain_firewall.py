"""
tests/unit/test_brain_firewall.py — Unit Tests: BrainFirewall
Sprint 1–2 | Owner: รักบี้

Tests: consent threshold, arousal limit, valence floor, happy path
"""

import pytest
from src.security.brain_firewall import BrainFirewall
from src.protocol.ttp_packet import TTPHeader, TTPPacket


def _make_packet(consent=0.85, arousal=0.3, valence=0.2) -> TTPPacket:
    header = TTPHeader(source_id="NODE_A", dest_id="NODE_B", symbol_id=0)
    return TTPPacket(
        header=header, symbol="focus",
        valence=valence, arousal=arousal,
        intensity=0.7, consent_score=consent,
        domain="neuro"
    )


class TestBrainFirewall:

    def setup_method(self):
        self.fw = BrainFirewall()

    # ── Happy Path ──────────────────────────────────────────────────────────

    def test_allows_valid_packet(self):
        pkt = _make_packet(consent=0.9, arousal=0.3, valence=0.5)
        result = self.fw.evaluate(pkt)
        assert result.allow is True
        assert result.reason == "OK"

    def test_allows_minimum_consent(self):
        pkt = _make_packet(consent=0.7)
        result = self.fw.evaluate(pkt)
        assert result.allow is True

    # ── Consent Threshold ───────────────────────────────────────────────────

    def test_blocks_below_consent_threshold(self):
        pkt = _make_packet(consent=0.69)
        result = self.fw.evaluate(pkt)
        assert result.allow is False
        assert result.rule_triggered == "FW-001"

    def test_blocks_zero_consent(self):
        pkt = _make_packet(consent=0.0)
        result = self.fw.evaluate(pkt)
        assert result.allow is False

    # ── Arousal Limit ───────────────────────────────────────────────────────

    def test_blocks_panic_state(self):
        pkt = _make_packet(arousal=0.91)
        result = self.fw.evaluate(pkt)
        assert result.allow is False
        assert result.rule_triggered == "FW-002"

    def test_allows_arousal_at_limit(self):
        pkt = _make_packet(arousal=0.9)
        result = self.fw.evaluate(pkt)
        # exactly at 0.9 should pass (> 0.9 triggers block)
        assert result.allow is True

    # ── Valence Floor ───────────────────────────────────────────────────────

    def test_blocks_subconscious_dissent(self):
        pkt = _make_packet(valence=-0.71)
        result = self.fw.evaluate(pkt)
        assert result.allow is False
        assert result.rule_triggered == "FW-003"

    def test_allows_valence_at_floor(self):
        pkt = _make_packet(valence=-0.7)
        result = self.fw.evaluate(pkt)
        assert result.allow is True

    # ── Priority Order ──────────────────────────────────────────────────────

    def test_consent_checked_before_arousal(self):
        """Low consent should trigger FW-001 even if arousal is also high."""
        pkt = _make_packet(consent=0.5, arousal=0.95)
        result = self.fw.evaluate(pkt)
        assert result.rule_triggered == "FW-001"

    def test_block_accuracy_across_100_malicious_packets(self):
        """Firewall must block ≥ 99% of malicious packets (Quality Gate)."""
        blocked = 0
        for _ in range(100):
            pkt = _make_packet(consent=0.3, arousal=0.95, valence=-0.8)
            if not self.fw.evaluate(pkt).allow:
                blocked += 1
        assert blocked / 100 >= 0.99
