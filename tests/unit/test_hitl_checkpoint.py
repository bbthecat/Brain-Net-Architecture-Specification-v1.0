"""
tests/unit/test_hitl_checkpoint.py — Unit Tests: HITLCheckpoint
Sprint 3 | Owner: รักบี้

Tests: trigger detection, hard stop timing, operator decisions, stats
"""

import time
import pytest
from src.security.hitl_checkpoint import (
    HITLCheckpoint, HITLTrigger, OperatorDecision
)
from src.protocol.ttp_packet import TTPHeader, TTPPacket


def _make_packet(arousal=0.3, consent=0.85, valence=0.2,
                 source="NODE_A", dest="NODE_B") -> TTPPacket:
    header = TTPHeader(source_id=source, dest_id=dest, symbol_id=0)
    return TTPPacket(
        header=header, symbol="focus",
        valence=valence, arousal=arousal,
        intensity=0.7, consent_score=consent,
        domain="neuro",
    )


class TestHITLCheckpoint:

    def setup_method(self):
        self.alerts = []
        self.hitl = HITLCheckpoint(alert_callback=lambda e: self.alerts.append(e))

    # ── No Trigger ───────────────────────────────────────────────────────────

    def test_no_trigger_for_normal_packet(self):
        pkt = _make_packet(arousal=0.3, consent=0.85)
        event = self.hitl.check(pkt)
        assert event is None
        assert self.hitl.is_paused is False

    # ── PANIC_STATE Trigger ──────────────────────────────────────────────────

    def test_triggers_panic_state(self):
        pkt = _make_packet(arousal=0.95)
        event = self.hitl.check(pkt)
        assert event is not None
        assert event.trigger == HITLTrigger.PANIC_STATE
        assert self.hitl.is_paused is True

    # ── LOW_CONSENT Trigger ──────────────────────────────────────────────────

    def test_triggers_low_consent(self):
        pkt = _make_packet(consent=0.2)
        event = self.hitl.check(pkt)
        assert event is not None
        assert event.trigger == HITLTrigger.LOW_CONSENT

    # ── STRESS_SPIKE Trigger ─────────────────────────────────────────────────

    def test_triggers_stress_spike(self):
        pkt1 = _make_packet(arousal=0.3)
        pkt2 = _make_packet(arousal=0.6)   # delta = 0.3 > threshold 0.25
        self.hitl.check(pkt1)
        event = self.hitl.check(pkt2)
        assert event is not None
        assert event.trigger == HITLTrigger.STRESS_SPIKE

    # ── REPEATED_INJECTION Trigger ───────────────────────────────────────────

    def test_triggers_repeated_injection(self):
        sid = "NODE_A→NODE_B"
        for _ in range(3):
            self.hitl.record_blocked(sid)
        pkt = _make_packet()
        event = self.hitl.check(pkt)
        assert event is not None
        assert event.trigger == HITLTrigger.REPEATED_INJECTION

    # ── Hard Stop Timing ─────────────────────────────────────────────────────

    def test_hard_stop_within_500ms(self):
        """Quality Gate: HITL Hard Stop must complete < 500ms."""
        t0 = time.perf_counter()
        pkt = _make_packet(arousal=0.95)
        self.hitl.check(pkt)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        assert elapsed_ms < 500

    # ── Alert Callback ───────────────────────────────────────────────────────

    def test_alert_callback_fired_on_trigger(self):
        pkt = _make_packet(arousal=0.95)
        self.hitl.check(pkt)
        assert len(self.alerts) == 1
        assert self.alerts[0].trigger == HITLTrigger.PANIC_STATE

    # ── Operator Decision ────────────────────────────────────────────────────

    def test_resume_unpauses_system(self):
        pkt = _make_packet(arousal=0.95)
        event = self.hitl.check(pkt)
        self.hitl.resume(event.session_id)
        assert self.hitl.is_paused is False

    def test_abort_records_decision(self):
        pkt = _make_packet(arousal=0.95)
        event = self.hitl.check(pkt)
        self.hitl.abort(event.session_id)
        resolved = [e for e in self.hitl.events if e.decision is not None]
        assert len(resolved) == 1
        assert resolved[0].decision == OperatorDecision.ABORT

    # ── Stats ────────────────────────────────────────────────────────────────

    def test_stats_initial(self):
        s = self.hitl.stats()
        assert s["total_triggers"] == 0
        assert s["resolved"] == 0

    def test_stats_after_events(self):
        pkt = _make_packet(arousal=0.95)
        event = self.hitl.check(pkt)
        self.hitl.resume(event.session_id)
        s = self.hitl.stats()
        assert s["total_triggers"] == 1
        assert s["resolved"] == 1
