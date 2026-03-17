"""
tests/unit/test_ttp_packet.py — Unit Tests: TTPHeader & TTPPacket
Sprint 1 | Owner: เจม

Tests: serialization, clamping, safety checks, age tracking
"""

import time
import pytest
from src.protocol.ttp_packet import TTPHeader, TTPPacket


# ── TTPHeader Tests ──────────────────────────────────────────────────────────

class TestTTPHeader:

    def test_pack_unpack_roundtrip(self):
        """Header serializes and deserializes correctly."""
        h = TTPHeader(source_id="NODE_A", dest_id="NODE_B", symbol_id=0)
        raw = h.pack()
        assert len(raw) == 32
        restored = TTPHeader.unpack(raw)
        assert restored.source_id == "NODE_A"
        assert restored.dest_id   == "NODE_B"
        assert restored.symbol_id == 0
        assert restored.packet_id == h.packet_id

    def test_pack_truncates_long_ids(self):
        """Node IDs longer than 8 chars are truncated silently."""
        h = TTPHeader(source_id="VERY_LONG_NODE_ID", dest_id="ALSO_LONG", symbol_id=1)
        raw = h.pack()
        assert len(raw) == 32

    def test_age_ms_recent(self):
        """Freshly created packet should have age < 5ms."""
        h = TTPHeader(source_id="A", dest_id="B", symbol_id=0)
        assert h.age_ms < 5.0

    def test_packet_id_unique(self):
        """Two headers should have different packet IDs."""
        h1 = TTPHeader(source_id="A", dest_id="B", symbol_id=0)
        h2 = TTPHeader(source_id="A", dest_id="B", symbol_id=0)
        assert h1.packet_id != h2.packet_id

    def test_unpack_too_short_raises(self):
        with pytest.raises(AssertionError):
            TTPHeader.unpack(b"\x00" * 16)


# ── TTPPacket Tests ──────────────────────────────────────────────────────────

class TestTTPPacket:

    def _make_packet(self, **kwargs) -> TTPPacket:
        header = TTPHeader(source_id="NODE_A", dest_id="NODE_B", symbol_id=0)
        defaults = dict(
            header=header, symbol="focus",
            valence=0.5, arousal=0.3,
            intensity=0.7, consent_score=0.85,
            domain="neuro"
        )
        defaults.update(kwargs)
        return TTPPacket(**defaults)

    def test_pack_unpack_roundtrip(self):
        pkt = self._make_packet()
        raw = pkt.pack()
        restored = TTPPacket.unpack(raw)
        assert restored.symbol        == "focus"
        assert abs(restored.valence   - 0.5)  < 0.001
        assert abs(restored.arousal   - 0.3)  < 0.001
        assert abs(restored.consent_score - 0.85) < 0.001
        assert restored.domain        == "neuro"

    def test_clamp_valence_above_1(self):
        pkt = self._make_packet(valence=2.5)
        assert pkt.valence == 1.0

    def test_clamp_valence_below_minus1(self):
        pkt = self._make_packet(valence=-5.0)
        assert pkt.valence == -1.0

    def test_clamp_arousal_above_1(self):
        pkt = self._make_packet(arousal=1.5)
        assert pkt.arousal == 1.0

    def test_clamp_arousal_below_0(self):
        pkt = self._make_packet(arousal=-0.5)
        assert pkt.arousal == 0.0

    def test_clamp_consent_score(self):
        pkt = self._make_packet(consent_score=1.9)
        assert pkt.consent_score == 1.0

    def test_is_safe_to_transmit_true(self):
        pkt = self._make_packet(consent_score=0.9, arousal=0.4)
        assert pkt.is_safe_to_transmit is True

    def test_is_safe_to_transmit_low_consent(self):
        pkt = self._make_packet(consent_score=0.4)
        assert pkt.is_safe_to_transmit is False

    def test_is_safe_to_transmit_high_arousal(self):
        pkt = self._make_packet(arousal=0.95)
        assert pkt.is_safe_to_transmit is False

    def test_summary_string(self):
        pkt = self._make_packet()
        s = pkt.summary()
        assert "focus" in s
        assert "neuro" in s

    def test_all_domains_roundtrip(self):
        for domain in ["bio", "phy", "neuro", "quantum"]:
            pkt = self._make_packet(domain=domain)
            raw = pkt.pack()
            restored = TTPPacket.unpack(raw)
            assert restored.domain == domain
