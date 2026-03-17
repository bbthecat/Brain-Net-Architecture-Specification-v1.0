"""
consensual_handshake.py — Consensual Handshake Protocol
Sprint 2 | Owner: รักบี้ (Security Specialist)

Subconscious-level session authorization.
Rules C-001 to C-004 from Architecture Specification.
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Tuple


class SessionState(Enum):
    PENDING   = "pending"
    ACTIVE    = "active"
    REJECTED  = "rejected"
    CLOSED    = "closed"


@dataclass
class HandshakeResult:
    allowed: bool
    state:   SessionState
    rule:    str
    message: str


@dataclass
class Session:
    source_id:  str
    dest_id:    str
    state:      SessionState = SessionState.PENDING
    created_at: float = field(default_factory=time.time)
    closed_at:  float = 0.0

    @property
    def key(self) -> Tuple[str, str]:
        return (self.source_id, self.dest_id)


class ConsensualHandshake:
    """
    Manages consent-based session establishment.

    Rules:
      C-001: Auto-Reject if Panic State (Arousal > 0.9)
      C-002: Terminate if Subconscious Dissent (Valence < -0.7)
      C-003: Block & Log if Coercion Marker detected
      C-004: Establish Session on Mutual Resonance
    """

    TEARDOWN_WARNING_S = 3.0
    CLEAR_TIMEOUT_MS   = 10.0

    def __init__(self):
        self._sessions: Dict[Tuple, Session] = {}

    def request_session(self, source_id: str, dest_id: str,
                        arousal: float, valence: float,
                        consent_score: float) -> HandshakeResult:
        """Attempt to open a new session."""
        # C-001
        if arousal > 0.9:
            return HandshakeResult(False, SessionState.REJECTED, "C-001",
                                   "Auto-reject: Panic state detected")
        # C-002
        if valence < -0.7:
            return HandshakeResult(False, SessionState.REJECTED, "C-002",
                                   "Terminate: Subconscious dissent")
        # C-003
        if self._coercion_detected(source_id):
            return HandshakeResult(False, SessionState.REJECTED, "C-003",
                                   "Block: Coercion marker detected")
        # C-004
        if consent_score >= 0.7:
            session = Session(source_id=source_id, dest_id=dest_id,
                              state=SessionState.ACTIVE)
            self._sessions[session.key] = session
            return HandshakeResult(True, SessionState.ACTIVE, "C-004",
                                   "Session established: Mutual resonance")

        return HandshakeResult(False, SessionState.PENDING, "NONE",
                               "Insufficient consent score")

    def is_session_active(self, source_id: str, dest_id: str) -> bool:
        session = self._sessions.get((source_id, dest_id))
        return session is not None and session.state == SessionState.ACTIVE

    def close_session(self, source_id: str, dest_id: str):
        """Soft-disconnect: warn then clear within 10ms."""
        key = (source_id, dest_id)
        if key in self._sessions:
            time.sleep(self.TEARDOWN_WARNING_S)
            t0 = time.perf_counter()
            self._sessions[key].state = SessionState.CLOSED
            self._sessions[key].closed_at = time.time()
            elapsed_ms = (time.perf_counter() - t0) * 1000
            assert elapsed_ms < self.CLEAR_TIMEOUT_MS, \
                f"Teardown exceeded 10ms: {elapsed_ms:.2f}ms"

    def _coercion_detected(self, source_id: str) -> bool:
        """Detect repeated rejection attempts (≥3 in 10s)."""
        now = time.time()
        recent = [s for s in self._sessions.values()
                  if s.source_id == source_id
                  and s.state == SessionState.REJECTED
                  and (now - s.created_at) < 10]
        return len(recent) >= 3
