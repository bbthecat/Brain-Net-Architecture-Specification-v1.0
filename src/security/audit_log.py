"""
audit_log.py — Immutable Ethics Audit Log with Hash Chain
Sprint 3 | Owner: โอเล่ + โยรุ

GDPR-compliant: stores NO neural payload, only metadata + decision.
"""

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import List


@dataclass
class AuditEntry:
    timestamp:    float
    session_hash: str
    user_hash:    str
    rule_id:      str
    decision:     str
    domain:       str
    consent_score: float
    arousal_level: float
    previous_hash: str
    this_hash:    str = field(init=False)

    def __post_init__(self):
        content = (f"{self.timestamp}{self.session_hash}{self.rule_id}"
                   f"{self.decision}{self.consent_score}{self.previous_hash}")
        self.this_hash = hashlib.sha256(content.encode()).hexdigest()


class AuditLog:
    """
    Append-only audit log using SHA-256 hash chain.
    Tamper-detection: any modification breaks the chain.
    """

    def __init__(self):
        self._entries: List[AuditEntry] = []
        self._genesis_hash = hashlib.sha256(b"BRAIN_NET_GENESIS").hexdigest()

    def log(self, packet, result) -> AuditEntry:
        """Append a new entry. Never stores neural payload."""
        prev_hash = (self._entries[-1].this_hash
                     if self._entries else self._genesis_hash)
        entry = AuditEntry(
            timestamp=time.time(),
            session_hash=hashlib.sha256(
                packet.header.source_id.encode()).hexdigest()[:16],
            user_hash=hashlib.sha256(
                packet.header.dest_id.encode()).hexdigest()[:16],
            rule_id=result.rule_id,
            decision=result.decision.value if hasattr(result.decision, "value") else str(result.decision),
            domain=packet.domain,
            consent_score=packet.consent_score,
            arousal_level=packet.arousal,
            previous_hash=prev_hash,
        )
        self._entries.append(entry)
        return entry

    def verify_chain(self) -> bool:
        """Verify hash chain integrity. Returns False if tampered."""
        prev = self._genesis_hash
        for entry in self._entries:
            content = (f"{entry.timestamp}{entry.session_hash}{entry.rule_id}"
                       f"{entry.decision}{entry.consent_score}{prev}")
            expected = hashlib.sha256(content.encode()).hexdigest()
            if expected != entry.this_hash:
                return False
            prev = entry.this_hash
        return True

    def export_json(self, path: str):
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = [{"timestamp": e.timestamp, "rule_id": e.rule_id,
                 "decision": e.decision, "domain": e.domain,
                 "consent_score": e.consent_score, "hash": e.this_hash}
                for e in self._entries]
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    @property
    def entries(self) -> List[AuditEntry]:
        return list(self._entries)
