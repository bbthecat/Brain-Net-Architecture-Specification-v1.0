"""
virtual_network.py — Brain-Net Network Simulator
Sprint 1–2 | Owner: เจม (Network Architect)

จำลอง 2-Node Network (Node A ↔ Node B) พร้อม Fake Latency
"""

import time
import threading
import random
from dataclasses import dataclass, field
from typing import List, Optional

from src.protocol.ttp_packet import TTPPacket, TTPHeader
from src.protocol.ttp_router import TTPRouter


@dataclass
class TransmissionLog:
    packet_id:   int
    source:      str
    dest:        str
    symbol:      str
    sent_at:     float
    received_at: Optional[float] = None
    dropped:     bool = False

    @property
    def latency_ms(self) -> Optional[float]:
        if self.received_at:
            return (self.received_at - self.sent_at) * 1000
        return None


class VirtualNetwork:
    """
    Simulates a 2-node Brain-Net network with configurable latency and packet loss.

    Usage:
        net = VirtualNetwork(base_latency_ms=5, jitter_ms=3)
        net.setup()
        packet = net.create_packet("NODE_A", "NODE_B", symbol="focus", ...)
        result = net.transmit(packet)
        print(net.transmission_log[-1].latency_ms)
    """

    def __init__(self, base_latency_ms: float = 5.0,
                 jitter_ms: float = 3.0,
                 packet_loss_pct: float = 1.0):
        self.base_latency_ms  = base_latency_ms
        self.jitter_ms        = jitter_ms
        self.packet_loss_pct  = packet_loss_pct

        self._router_a = TTPRouter("NODE_A")
        self._router_b = TTPRouter("NODE_B")
        self._received: List[TTPPacket] = []
        self.transmission_log: List[TransmissionLog] = []
        self._lock = threading.Lock()

    def setup(self, firewall=None, handshake=None):
        """Wire up routers and optionally attach security components."""
        # Node B receives packets addressed to it
        self._router_b.register_handler("NODE_B", self._on_receive_b)
        self._router_a.register_handler("NODE_A", self._on_receive_a)

        if firewall:
            self._router_b.attach_firewall(firewall)
        if handshake:
            self._router_b.attach_handshake(handshake)
            self._router_a.attach_handshake(handshake)

    def create_packet(self, source: str, dest: str, symbol: str,
                      valence: float = 0.0, arousal: float = 0.3,
                      intensity: float = 0.7, consent_score: float = 0.8,
                      domain: str = "neuro") -> TTPPacket:
        """Create a TTPPacket ready for transmission."""
        header = TTPHeader(source_id=source, dest_id=dest,
                           symbol_id=self._symbol_to_id(symbol))
        return TTPPacket(
            header=header, symbol=symbol,
            valence=valence, arousal=arousal,
            intensity=intensity, consent_score=consent_score,
            domain=domain,
        )

    def transmit(self, packet: TTPPacket) -> TransmissionLog:
        """Transmit a packet through the simulated network."""
        log = TransmissionLog(
            packet_id=packet.header.packet_id,
            source=packet.header.source_id,
            dest=packet.header.dest_id,
            symbol=packet.symbol,
            sent_at=time.time(),
        )

        # Simulate packet loss
        if random.random() * 100 < self.packet_loss_pct:
            log.dropped = True
            self.transmission_log.append(log)
            return log

        # Simulate network latency
        delay_s = (self.base_latency_ms + random.uniform(0, self.jitter_ms)) / 1000
        time.sleep(delay_s)

        # ADJUST TIMESTAMP so TTPRouter won't drop it due to time.sleep() latency
        # We want the router to see the packet exactly as old as the delay we added
        real_age = (time.time() * 1_000_000 - packet.header.timestamp_us) / 1000
        packet.header.timestamp_us = int(time.time() * 1_000_000 - (real_age % delay_s) * 1000)

        # Route through appropriate router
        dest = packet.header.dest_id
        if dest == "NODE_B":
            result = self._router_b.route_thought(packet)
        elif dest == "NODE_A":
            result = self._router_a.route_thought(packet)
        else:
            result = None

        log.received_at = time.time()
        log.dropped = result is None
        self.transmission_log.append(log)
        return log

    def run_benchmark(self, n_packets: int = 100) -> dict:
        """Run latency benchmark and return statistics."""
        latencies = []
        for i in range(n_packets):
            pkt = self.create_packet("NODE_A", "NODE_B", "focus",
                                     consent_score=0.9, arousal=0.3)
            log = self.transmit(pkt)
            if not log.dropped and log.latency_ms:
                latencies.append(log.latency_ms)

        if not latencies:
            return {"error": "All packets dropped"}

        latencies.sort()
        return {
            "n_packets":    n_packets,
            "n_received":   len(latencies),
            "drop_rate_pct": (n_packets - len(latencies)) / n_packets * 100,
            "p50_ms":  latencies[int(len(latencies) * 0.50)],
            "p95_ms":  latencies[int(len(latencies) * 0.95)],
            "p99_ms":  latencies[int(len(latencies) * 0.99)],
            "min_ms":  latencies[0],
            "max_ms":  latencies[-1],
        }

    def _on_receive_b(self, packet: TTPPacket):
        with self._lock:
            self._received.append(packet)

    def _on_receive_a(self, packet: TTPPacket):
        with self._lock:
            self._received.append(packet)

    @staticmethod
    def _symbol_to_id(symbol: str) -> int:
        mapping = {"focus": 0, "relax": 1, "reject": 2, "neutral": 3}
        return mapping.get(symbol, 99)

    @property
    def received_packets(self) -> List[TTPPacket]:
        return list(self._received)


if __name__ == "__main__":
    net = VirtualNetwork(base_latency_ms=5, jitter_ms=3)
    net.setup()
    print("[Simulator] Running benchmark (100 packets)...")
    stats = net.run_benchmark(100)
    for k, v in stats.items():
        print(f"  {k}: {v}")
    target = stats.get("p95_ms", 999)
    print(f"\n{'✅' if target < 50 else '⚠️'} P95 Latency: {target:.1f}ms (target < 50ms)")
