"""
tests/unit/test_consensual_handshake.py — Unit Tests: ConsensualHandshake
Sprint 2 | Owner: รักบี้

Tests: C-001 to C-004 rules, session lifecycle, coercion detection
"""

import time
import pytest
from src.security.consensual_handshake import (
    ConsensualHandshake, SessionState
)


class TestConsensualHandshake:

    def setup_method(self):
        self.hs = ConsensualHandshake()

    # ── C-001: Panic State ──────────────────────────────────────────────────

    def test_c001_rejects_panic_state(self):
        result = self.hs.request_session(
            "A", "B", arousal=0.95, valence=0.2, consent_score=0.8
        )
        assert result.allowed is False
        assert result.rule == "C-001"
        assert result.state == SessionState.REJECTED

    def test_c001_allows_arousal_at_boundary(self):
        result = self.hs.request_session(
            "A", "B", arousal=0.9, valence=0.2, consent_score=0.8
        )
        assert result.allowed is True

    # ── C-002: Subconscious Dissent ─────────────────────────────────────────

    def test_c002_rejects_negative_valence(self):
        result = self.hs.request_session(
            "A", "B", arousal=0.3, valence=-0.8, consent_score=0.8
        )
        assert result.allowed is False
        assert result.rule == "C-002"

    def test_c002_allows_valence_at_floor(self):
        result = self.hs.request_session(
            "A", "B", arousal=0.3, valence=-0.7, consent_score=0.8
        )
        assert result.allowed is True

    # ── C-004: Mutual Resonance ─────────────────────────────────────────────

    def test_c004_establishes_session(self):
        result = self.hs.request_session(
            "A", "B", arousal=0.3, valence=0.5, consent_score=0.85
        )
        assert result.allowed is True
        assert result.rule == "C-004"
        assert result.state == SessionState.ACTIVE

    def test_session_is_active_after_establishment(self):
        self.hs.request_session(
            "A", "B", arousal=0.3, valence=0.2, consent_score=0.85
        )
        assert self.hs.is_session_active("A", "B") is True

    def test_session_not_active_when_rejected(self):
        self.hs.request_session(
            "A", "B", arousal=0.95, valence=0.2, consent_score=0.8
        )
        assert self.hs.is_session_active("A", "B") is False

    # ── Insufficient Consent ────────────────────────────────────────────────

    def test_pending_when_consent_insufficient(self):
        result = self.hs.request_session(
            "A", "B", arousal=0.3, valence=0.2, consent_score=0.6
        )
        assert result.allowed is False
        assert result.state == SessionState.PENDING

    # ── C-003: Coercion Detection ───────────────────────────────────────────

    def test_c003_blocks_after_3_rejections(self):
        """Three rejections within 10s should trigger coercion block."""
        for _ in range(3):
            # Force rejections by submitting low-valence (C-002 rejection)
            self.hs.request_session(
                "COERCE", "B", arousal=0.3, valence=-0.8, consent_score=0.8
            )
        # Now try a legitimate request — should be blocked as coercion
        result = self.hs.request_session(
            "COERCE", "B", arousal=0.3, valence=0.5, consent_score=0.9
        )
        assert result.allowed is False
        assert result.rule == "C-003"
