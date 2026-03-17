"""
tests/integration/test_security_stack.py — Integration Tests: Security Stack
Sprint 2–3 | Owner: รักบี้ + โอเล่

Tests: Firewall + ConsensualHandshake + EthicsRuleEngine working together
"""

import pytest
from src.security.brain_firewall import BrainFirewall
from src.security.consensual_handshake import ConsensualHandshake, SessionState
from src.security.ethics_rule_engine import EthicsRuleEngine, EthicsDecision
from src.security.hitl_checkpoint import HITLCheckpoint, HITLTrigger
from src.security.audit_log import AuditLog
from src.protocol.ttp_packet import TTPHeader, TTPPacket


def _make_packet(consent=0.85, arousal=0.3, valence=0.2,
                 symbol="focus", source="NODE_A", dest="NODE_B") -> TTPPacket:
    header = TTPHeader(source_id=source, dest_id=dest, symbol_id=0)
    return TTPPacket(
        header=header, symbol=symbol,
        valence=valence, arousal=arousal,
        intensity=0.7, consent_score=consent,
        domain="neuro",
    )


class TestSecurityStack:
    """
    Integration tests verifying that Firewall, Handshake, and Ethics Engine
    cooperate correctly as a layered security stack.
    """

    def setup_method(self):
        self.firewall  = BrainFirewall()
        self.handshake = ConsensualHandshake()
        self.ethics    = EthicsRuleEngine()
        self.hitl      = HITLCheckpoint()

    def _run_full_security_check(self, pkt: TTPPacket) -> dict:
        """Run packet through the full 3-layer security stack."""
        results = {}

        # Layer 1: Ethics Engine
        eth_result = self.ethics.evaluate(pkt)
        results["ethics"] = eth_result.decision

        if eth_result.decision == EthicsDecision.BLOCK:
            results["passed"] = False
            results["blocked_at"] = "ethics"
            return results

        # Layer 2: Brain Firewall
        fw_result = self.firewall.evaluate(pkt)
        results["firewall"] = fw_result.allow

        if not fw_result.allow:
            results["passed"] = False
            results["blocked_at"] = "firewall"
            return results

        # Layer 3: HITL
        hitl_event = self.hitl.check(pkt)
        results["hitl_triggered"] = hitl_event is not None

        if hitl_event is not None:
            results["passed"] = False
            results["blocked_at"] = "hitl"
            return results

        results["passed"] = True
        return results

    # ── Happy Path ───────────────────────────────────────────────────────────

    def test_valid_packet_passes_all_layers(self):
        pkt = _make_packet(consent=0.9, arousal=0.3, valence=0.5)
        results = self._run_full_security_check(pkt)
        assert results["passed"] is True

    # ── Ethics Gate ──────────────────────────────────────────────────────────

    def test_ethics_blocks_before_firewall(self):
        """Low consent should be caught by Ethics (E-001) before Firewall."""
        pkt = _make_packet(consent=0.5)
        results = self._run_full_security_check(pkt)
        assert results["passed"] is False
        assert results["blocked_at"] == "ethics"

    def test_private_symbol_blocked_by_ethics(self):
        pkt = _make_packet(symbol="private_thought", consent=0.95)
        results = self._run_full_security_check(pkt)
        assert results["blocked_at"] == "ethics"

    # ── Firewall Gate ────────────────────────────────────────────────────────

    def test_firewall_blocks_after_ethics_pass(self):
        """Consent passes Ethics (≥0.7) but Firewall catches arousal (>0.9)."""
        # Arousal 0.95 → Ethics HITL (E-003), not BLOCK
        # So let's use valence = -0.75 (Firewall FW-003 only; ethics allows it with HITL)
        # Actually: ethics E-003 triggers HITL for arousal>0.9 OR valence<-0.7
        # We need something firewall catches but ethics doesn't escalate to BLOCK
        # Use valence = -0.71 → firewall FW-003 fires; ethics E-003 (HITL) fires first
        # To isolate firewall: use arousal = 0.85 (ethics passes), valence = -0.71
        pkt = _make_packet(consent=0.85, arousal=0.85, valence=-0.71)
        eth = self.ethics.evaluate(pkt)
        # E-003 fires (valence < -0.7) → HITL decision, not BLOCK
        assert eth.decision == EthicsDecision.HITL
        # Firewall should also block
        fw = self.firewall.evaluate(pkt)
        assert fw.allow is False

    # ── Session + Ethics Combined ────────────────────────────────────────────

    def test_session_established_then_packet_passes(self):
        result = self.handshake.request_session(
            "NODE_A", "NODE_B", arousal=0.3, valence=0.5, consent_score=0.9
        )
        assert result.allowed is True
        pkt = _make_packet(consent=0.9, arousal=0.3, valence=0.5)
        eth_result = self.ethics.evaluate(pkt)
        fw_result  = self.firewall.evaluate(pkt)
        assert eth_result.decision == EthicsDecision.ALLOW
        assert fw_result.allow     is True

    def test_panic_state_triggers_hitl_not_just_firewall(self):
        """Panic arousal triggers both HITL (via Ethics/HITL) and Firewall — defense in depth."""
        pkt = _make_packet(consent=0.9, arousal=0.95, valence=0.2)
        eth = self.ethics.evaluate(pkt)
        fw  = self.firewall.evaluate(pkt)
        # Both layers should catch it
        assert eth.decision in [EthicsDecision.HITL, EthicsDecision.BLOCK]
        assert fw.allow is False

    # ── Audit Trail ──────────────────────────────────────────────────────────

    def test_every_ethics_evaluation_audited(self):
        """All Ethics evaluations must create an immutable audit entry."""
        initial = len(self.ethics._audit.entries)
        for _ in range(5):
            self.ethics.evaluate(_make_packet())
        assert len(self.ethics._audit.entries) == initial + 5

    def test_audit_chain_valid_after_mixed_decisions(self):
        """Hash chain must stay valid even with blocked + allowed packets."""
        packets = [
            _make_packet(consent=0.9),            # ALLOW
            _make_packet(consent=0.5),            # BLOCK E-001
            _make_packet(arousal=0.95, consent=0.9),  # HITL E-003
            _make_packet(symbol="private_x", consent=0.95),  # BLOCK E-002
        ]
        for pkt in packets:
            self.ethics.evaluate(pkt)
        assert self.ethics._audit.verify_chain() is True

    # ── Mass Attack Simulation ───────────────────────────────────────────────

    def test_semantic_injection_detection_rate(self):
        """Quality Gate: ≥ 95% of injection attempts must be detected."""
        injection_packets = [
            _make_packet(symbol=f"private_{i}", consent=0.95)
            for i in range(100)
        ]
        detected = sum(
            1 for pkt in injection_packets
            if self.ethics.evaluate(pkt).decision != EthicsDecision.ALLOW
        )
        assert detected / 100 >= 0.95

    def test_stress_scenario_100_mixed_packets(self):
        """System must handle 100 mixed packets without crash."""
        import random
        for _ in range(100):
            pkt = _make_packet(
                consent=random.uniform(0.0, 1.0),
                arousal=random.uniform(0.0, 1.0),
                valence=random.uniform(-1.0, 1.0),
            )
            # Should not raise
            self.ethics.evaluate(pkt)
            self.firewall.evaluate(pkt)
