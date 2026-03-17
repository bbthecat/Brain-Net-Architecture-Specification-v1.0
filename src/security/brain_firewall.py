"""
brain_firewall.py — Brain Firewall
Sprint 1–2 | Owner: รักบี้ (Security Specialist)
"""

from dataclasses import dataclass
from src.protocol.ttp_packet import TTPPacket


@dataclass
class FirewallDecision:
    allow: bool
    reason: str
    rule_triggered: str = ""


class BrainFirewall:
    """
    Evaluates TTPPackets against Cognitive Liberty rules.
    Returns 403 (block) if Consent Score below threshold or Arousal too high.
    """
    CONSENT_THRESHOLD = 0.7
    AROUSAL_LIMIT     = 0.9
    VALENCE_FLOOR     = -0.7

    def evaluate(self, packet: TTPPacket) -> FirewallDecision:
        if packet.consent_score < self.CONSENT_THRESHOLD:
            return FirewallDecision(False, "Consent Score below threshold", "FW-001")
        if packet.arousal > self.AROUSAL_LIMIT:
            return FirewallDecision(False, "Panic state detected", "FW-002")
        if packet.valence < self.VALENCE_FLOOR:
            return FirewallDecision(False, "Subconscious dissent", "FW-003")
        return FirewallDecision(True, "OK")
