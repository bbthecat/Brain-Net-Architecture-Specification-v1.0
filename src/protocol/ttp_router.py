"""
ttp_router.py — Thought Transfer Protocol Router
Sprint 1–2 | Owner: เจม (Network Architect)

Routes TTPPackets from source to destination node.
Implements UDP-like drop (no retransmit) to prevent Neural Dissonance.
"""

import time
import queue
import threading
from typing import Callable, Optional

from src.protocol.ttp_packet import TTPPacket

LATENCY_BUDGET_MS = 50.0   # Hard limit — drop packets older than this


class TTPRouter:
    """
    Routes TTPPackets between nodes.

    - Drops packets that exceed the 50ms latency budget
    - Prioritizes High-Arousal (emergency) packets
    - Integrates with BrainFirewall and ConsensualHandshake (Sprint 2)
    """

    def __init__(self, node_id: str, max_queue: int = 128):
        self.node_id   = node_id
        self._queue    = queue.PriorityQueue(maxsize=max_queue)
        self._handlers: dict[str, Callable] = {}   # dest_id → callback
        self._firewall = None
        self._handshake = None
        self._running  = False
        self._lock     = threading.Lock()
        self._stats    = {"routed": 0, "dropped_latency": 0, "dropped_firewall": 0}

    # ── Wiring ──────────────────────────────────────────────────────────────

    def attach_firewall(self, firewall):
        """Attach a BrainFirewall instance (Sprint 2 integration)."""
        self._firewall = firewall

    def attach_handshake(self, handshake):
        """Attach ConsensualHandshake instance (Sprint 2)."""
        self._handshake = handshake

    def register_handler(self, dest_id: str, callback: Callable[[TTPPacket], None]):
        """Register a receive callback for a destination node."""
        self._handlers[dest_id] = callback

    # ── Routing ─────────────────────────────────────────────────────────────

    def send(self, packet: TTPPacket) -> bool:
        """
        Queue a packet for routing.
        High-arousal packets get priority (lower number = higher priority).
        """
        # Drop stale packets immediately
        if packet.header.age_ms > LATENCY_BUDGET_MS:
            self._stats["dropped_latency"] += 1
            return False

        priority = 0 if packet.arousal > 0.7 else 1
        try:
            self._queue.put_nowait((priority, time.time(), packet))
            return True
        except queue.Full:
            self._stats["dropped_latency"] += 1
            return False

    def route_thought(self, packet: TTPPacket) -> Optional[TTPPacket]:
        """
        Synchronous routing: validate → firewall → deliver.
        Returns routed packet or None if dropped.
        """
        # Latency check
        if packet.header.age_ms > LATENCY_BUDGET_MS:
            self._stats["dropped_latency"] += 1
            return None

        # Handshake check (Sprint 2)
        if self._handshake:
            session_ok = self._handshake.is_session_active(
                packet.header.source_id, packet.header.dest_id
            )
            if not session_ok:
                return None

        # Firewall check (Sprint 2)
        if self._firewall:
            decision = self._firewall.evaluate(packet)
            if not decision.allow:
                self._stats["dropped_firewall"] += 1
                return None

        # Deliver
        dest = packet.header.dest_id
        if dest in self._handlers:
            self._handlers[dest](packet)

        self._stats["routed"] += 1
        return packet

    # ── Async processing ────────────────────────────────────────────────────

    def start(self):
        """Start background routing thread."""
        self._running = True
        t = threading.Thread(target=self._process_loop, daemon=True)
        t.start()

    def stop(self):
        self._running = False

    def _process_loop(self):
        while self._running:
            try:
                _, _, packet = self._queue.get(timeout=0.01)
                self.route_thought(packet)
            except queue.Empty:
                continue

    # ── Stats ────────────────────────────────────────────────────────────────

    @property
    def stats(self) -> dict:
        return dict(self._stats)
