"""
ethics_rule_engine.py — Automated Ethics Rule Engine
Sprint 3 | Owner: โอเล่ (Neuroethics Lead) + รักบี้ (Security)
"""

from dataclasses import dataclass
from enum import Enum
from src.protocol.ttp_packet import TTPPacket
from src.security.audit_log import AuditLog


class EthicsDecision(Enum):
    ALLOW      = "ALLOW"
    BLOCK      = "BLOCK"
    QUARANTINE = "QUARANTINE"
    HITL       = "HITL"


@dataclass
class EthicsResult:
    decision:   EthicsDecision
    rule_id:    str
    message:    str
    packet_id:  int = 0


class EthicsRuleEngine:
    """
    Evaluates packets against all Ethics Rules (E-001 to E-005).
    Integrates with AuditLog and BrainFirewall.
    """

    def __init__(self):
        self._audit = AuditLog()
        self.rules = ["E-001", "E-002", "E-003", "E-004", "E-005"]

    def evaluate(self, packet: TTPPacket) -> EthicsResult:
        result = self._check_all(packet)
        self._audit.log(packet, result)
        return result

    def _check_all(self, packet: TTPPacket) -> EthicsResult:
        # E-001: Consent
        if packet.consent_score < 0.7:
            return EthicsResult(EthicsDecision.BLOCK, "E-001",
                                "Consent Score below minimum", packet.header.packet_id)
        # E-002: Private Thought Boundary
        if self._in_private_boundary(packet):
            return EthicsResult(EthicsDecision.BLOCK, "E-002",
                                "Private thought boundary violation", packet.header.packet_id)
        # E-003: Coercion
        if packet.arousal > 0.9 or packet.valence < -0.7:
            return EthicsResult(EthicsDecision.HITL, "E-003",
                                "Coercion indicator detected", packet.header.packet_id)
        # E-004 & E-005 handled by AuditLog and Session teardown
        return EthicsResult(EthicsDecision.ALLOW, "PASS", "OK", packet.header.packet_id)

    def _in_private_boundary(self, packet: TTPPacket) -> bool:
        """Symbols explicitly marked as private cannot be transmitted."""
        return packet.symbol.startswith("private_")
