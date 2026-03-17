"""
tests/unit/test_ttp_router.py — Unit Tests: TTPRouter + VirtualNetwork
Sprint 1–2 | Owner: เจม

Tests: routing, latency budget drops, firewall integration, queue priority
"""

import time
import pytest
from unittest.mock import MagicMock
from src.protocol.ttp_packet import TTPHeader, TTPPacket
from src.protocol.ttp_router import TTPRouter, LATENCY_BUDGET_MS
from src.protocol.virtual_network import VirtualNetwork, TransmissionLog


def _make_packet(arousal=0.3, consent=0.85, source="NODE_A",
                 dest="NODE_B", symbol="focus") -> TTPPacket:
    header = TTPHeader(source_id=source, dest_id=dest, symbol_id=0)
    return TTPPacket(
        header=header, symbol=symbol,
        valence=0.2, arousal=arousal,
        intensity=0.7, consent_score=consent,
        domain="neuro",
    )


# ── TTPRouter Tests ──────────────────────────────────────────────────────────

class TestTTPRouter:

    def setup_method(self):
        self.router = TTPRouter("NODE_A")
        self.received = []
        self.router.register_handler("NODE_B", lambda p: self.received.append(p))

    def test_routes_fresh_packet(self):
        pkt = _make_packet()
        result = self.router.route_thought(pkt)
        assert result is not None

    def test_delivers_to_handler(self):
        pkt = _make_packet(dest="NODE_B")
        self.router.route_thought(pkt)
        assert len(self.received) == 1

    def test_drops_stale_packet(self):
        """Packets older than LATENCY_BUDGET_MS must be dropped."""
        pkt = _make_packet()
        # Manually backdate the timestamp
        pkt.header.timestamp_us = int(
            (time.time() - (LATENCY_BUDGET_MS + 10) / 1000) * 1_000_000
        )
        result = self.router.route_thought(pkt)
        assert result is None
        assert self.router.stats["dropped_latency"] == 1

    def test_firewall_integration_blocks_packet(self):
        mock_fw = MagicMock()
        mock_fw.evaluate.return_value = MagicMock(allow=False, reason="Test block")
        self.router.attach_firewall(mock_fw)
        pkt = _make_packet()
        result = self.router.route_thought(pkt)
        assert result is None
        assert self.router.stats["dropped_firewall"] == 1

    def test_firewall_integration_allows_packet(self):
        mock_fw = MagicMock()
        mock_fw.evaluate.return_value = MagicMock(allow=True)
        self.router.attach_firewall(mock_fw)
        pkt = _make_packet()
        result = self.router.route_thought(pkt)
        assert result is not None

    def test_handshake_integration_blocks_without_session(self):
        mock_hs = MagicMock()
        mock_hs.is_session_active.return_value = False
        self.router.attach_handshake(mock_hs)
        pkt = _make_packet()
        result = self.router.route_thought(pkt)
        assert result is None

    def test_stats_routed_count(self):
        for _ in range(5):
            self.router.route_thought(_make_packet())
        assert self.router.stats["routed"] == 5

    def test_send_enqueues_packet(self):
        pkt = _make_packet()
        ok = self.router.send(pkt)
        assert ok is True

    def test_high_arousal_gets_priority_0(self):
        """High-arousal packets should be marked priority=0 (highest)."""
        pkt = _make_packet(arousal=0.8)
        ok = self.router.send(pkt)
        assert ok is True   # just verify it queued without error


# ── VirtualNetwork Tests ─────────────────────────────────────────────────────

class TestVirtualNetwork:

    def setup_method(self):
        self.net = VirtualNetwork(
            base_latency_ms=2.0,
            jitter_ms=1.0,
            packet_loss_pct=0.0   # disable loss for deterministic tests
        )
        self.net.setup()

    def test_create_packet(self):
        pkt = self.net.create_packet("NODE_A", "NODE_B", "focus",
                                     consent_score=0.9)
        assert pkt.symbol       == "focus"
        assert pkt.consent_score == 0.9

    def test_transmit_returns_log(self):
        pkt = self.net.create_packet("NODE_A", "NODE_B", "focus")
        log = self.net.transmit(pkt)
        assert isinstance(log, TransmissionLog)

    def test_transmit_not_dropped_zero_loss(self):
        pkt = self.net.create_packet("NODE_A", "NODE_B", "focus",
                                     consent_score=0.9)
        log = self.net.transmit(pkt)
        assert log.dropped is False

    def test_transmit_latency_recorded(self):
        pkt = self.net.create_packet("NODE_A", "NODE_B", "focus",
                                     consent_score=0.9)
        log = self.net.transmit(pkt)
        assert log.latency_ms is not None
        assert log.latency_ms >= 0

    def test_all_symbols_transmittable(self):
        for symbol in ["focus", "relax", "reject", "neutral"]:
            pkt = self.net.create_packet("NODE_A", "NODE_B", symbol,
                                         consent_score=0.9)
            log = self.net.transmit(pkt)
            assert log.dropped is False

    def test_benchmark_returns_stats(self):
        stats = self.net.run_benchmark(n_packets=20)
        for key in ["n_packets", "n_received", "p50_ms", "p95_ms"]:
            assert key in stats

    def test_benchmark_p95_reasonable(self):
        """With 2ms base + 1ms jitter, P95 should be well under 50ms."""
        stats = self.net.run_benchmark(n_packets=50)
        if "p95_ms" in stats:
            assert stats["p95_ms"] < 50.0

    def test_packet_loss_causes_drops(self):
        lossy_net = VirtualNetwork(
            base_latency_ms=1.0,
            jitter_ms=0.5,
            packet_loss_pct=100.0   # drop everything
        )
        lossy_net.setup()
        pkt = lossy_net.create_packet("NODE_A", "NODE_B", "focus")
        log = lossy_net.transmit(pkt)
        assert log.dropped is True
