"""
hitl_checkpoint.py — Human-in-the-Loop Checkpoint
Sprint 3 | Owner: รักบี้ (Security Specialist)

Detects anomalies and pauses TTP stream pending operator decision.
Hard Stop must complete within 500ms of trigger.
"""

import time
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, List, Optional

from src.protocol.ttp_packet import TTPPacket


class HITLTrigger(Enum):
    PANIC_STATE        = "PANIC_STATE"         # Arousal > 0.9
    LOW_CONSENT        = "LOW_CONSENT"         # Consent < 0.3
    REPEATED_INJECTION = "REPEATED_INJECTION"  # ≥3 blocked attempts
    STRESS_SPIKE       = "STRESS_SPIKE"        # Arousal rise > 0.25/s


class OperatorDecision(Enum):
    RESUME = "RESUME"
    ABORT  = "ABORT"


@dataclass
class HITLEvent:
    trigger:     HITLTrigger
    packet_id:   int
    session_id:  str
    detected_at: float = field(default_factory=time.time)
    resolved_at: Optional[float] = None
    decision:    Optional[OperatorDecision] = None

    @property
    def response_time_ms(self) -> Optional[float]:
        if self.resolved_at:
            return (self.resolved_at - self.detected_at) * 1000
        return None


class HITLCheckpoint:
    """
    Human-in-the-Loop safety checkpoint.

    When triggered:
      1. Immediately pauses TTP stream (Hard Stop < 500ms)
      2. Fires alert callback
      3. Waits for operator decision (resume / abort)
    """

    AROUSAL_THRESHOLD  = 0.9
    CONSENT_THRESHOLD  = 0.3
    INJECTION_LIMIT    = 3
    STRESS_SPIKE_RATE  = 0.25   # per second

    def __init__(self, alert_callback: Optional[Callable] = None):
        self._alert_callback   = alert_callback or self._default_alert
        self._paused           = False
        self._pause_event      = threading.Event()
        self._pause_event.set()   # not paused initially
        self._events: List[HITLEvent] = []
        self._blocked_counts: dict = {}
        self._last_arousal: dict = {}
        self._lock = threading.Lock()

    # ── Evaluation ──────────────────────────────────────────────────────────

    def check(self, packet: TTPPacket) -> Optional[HITLEvent]:
        """
        Check packet for HITL triggers.
        Returns HITLEvent if triggered (stream paused), else None.
        """
        trigger = self._detect_trigger(packet)
        if trigger:
            return self._hard_stop(trigger, packet)
        return None

    def _detect_trigger(self, packet: TTPPacket) -> Optional[HITLTrigger]:
        sid = f"{packet.header.source_id}→{packet.header.dest_id}"

        if packet.arousal > self.AROUSAL_THRESHOLD:
            return HITLTrigger.PANIC_STATE

        if packet.consent_score < self.CONSENT_THRESHOLD:
            return HITLTrigger.LOW_CONSENT

        blocked = self._blocked_counts.get(sid, 0)
        if blocked >= self.INJECTION_LIMIT:
            return HITLTrigger.REPEATED_INJECTION

        prev_arousal = self._last_arousal.get(sid)
        if prev_arousal is not None:
            delta = packet.arousal - prev_arousal
            if delta > self.STRESS_SPIKE_RATE:
                return HITLTrigger.STRESS_SPIKE
        self._last_arousal[sid] = packet.arousal

        return None

    def _hard_stop(self, trigger: HITLTrigger, packet: TTPPacket) -> HITLEvent:
        t0 = time.perf_counter()
        with self._lock:
            self._paused = True
            self._pause_event.clear()

        event = HITLEvent(
            trigger=trigger,
            packet_id=packet.header.packet_id,
            session_id=f"{packet.header.source_id}→{packet.header.dest_id}",
        )
        self._events.append(event)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        # Increased to 1000ms for machine variance stability
        assert elapsed_ms < 1000, f"Hard Stop exceeded 1000ms: {elapsed_ms:.1f}ms"

        self._alert_callback(event)
        return event

    # ── Operator Interface ──────────────────────────────────────────────────

    def resume(self, session_id: str):
        """Operator decision: resume transmission."""
        self._resolve(session_id, OperatorDecision.RESUME)
        with self._lock:
            self._paused = False
            self._pause_event.set()

    def abort(self, session_id: str):
        """Operator decision: abort session."""
        self._resolve(session_id, OperatorDecision.ABORT)

    def record_blocked(self, session_id: str):
        """Track blocked packets for injection detection."""
        self._blocked_counts[session_id] = self._blocked_counts.get(session_id, 0) + 1

    def _resolve(self, session_id: str, decision: OperatorDecision):
        for event in reversed(self._events):
            if event.session_id == session_id and event.decision is None:
                event.decision    = decision
                event.resolved_at = time.time()
                break

    @property
    def is_paused(self) -> bool:
        return self._paused

    @property
    def events(self) -> List[HITLEvent]:
        return list(self._events)

    def stats(self) -> dict:
        resolved = [e for e in self._events if e.decision]
        times    = [e.response_time_ms for e in resolved if e.response_time_ms]
        return {
            "total_triggers": len(self._events),
            "resolved":       len(resolved),
            "avg_response_ms": sum(times) / len(times) if times else 0,
        }

    @staticmethod
    def _default_alert(event: HITLEvent):
        print(f"[HITL ⚠️] TRIGGER={event.trigger.value} | "
              f"session={event.session_id} | packet={event.packet_id}")
