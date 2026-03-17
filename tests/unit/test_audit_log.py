"""
tests/unit/test_audit_log.py — Unit Tests: AuditLog (Immutable Hash Chain)
Sprint 3 | Owner: โอเล่

Tests: append, hash chain integrity, tamper detection, JSON export, privacy
"""

import json
import os
import tempfile
import pytest
from unittest.mock import MagicMock
from src.security.audit_log import AuditLog, AuditEntry
from src.security.ethics_rule_engine import EthicsDecision


def _mock_packet(consent=0.85, arousal=0.3, domain="neuro",
                 source="NODE_A", dest="NODE_B"):
    pkt = MagicMock()
    pkt.header.source_id = source
    pkt.header.dest_id   = dest
    pkt.consent_score    = consent
    pkt.arousal          = arousal
    pkt.domain           = domain
    return pkt


def _mock_result(decision="ALLOW", rule_id="PASS"):
    r = MagicMock()
    r.rule_id  = rule_id
    r.decision = decision
    return r


class TestAuditLog:

    def setup_method(self):
        self.log = AuditLog()

    # ── Appending ────────────────────────────────────────────────────────────

    def test_empty_log_verifies(self):
        assert self.log.verify_chain() is True

    def test_single_entry_appended(self):
        pkt = _mock_packet()
        res = _mock_result()
        entry = self.log.log(pkt, res)
        assert isinstance(entry, AuditEntry)
        assert len(self.log.entries) == 1

    def test_multiple_entries_appended(self):
        for i in range(10):
            self.log.log(_mock_packet(), _mock_result())
        assert len(self.log.entries) == 10

    # ── Hash Chain ───────────────────────────────────────────────────────────

    def test_chain_valid_after_multiple_entries(self):
        for _ in range(5):
            self.log.log(_mock_packet(), _mock_result())
        assert self.log.verify_chain() is True

    def test_tamper_detection_breaks_chain(self):
        for _ in range(3):
            self.log.log(_mock_packet(), _mock_result())
        # Tamper with middle entry
        self.log._entries[1].decision = "TAMPERED"
        assert self.log.verify_chain() is False

    def test_each_entry_has_unique_hash(self):
        for _ in range(5):
            self.log.log(_mock_packet(), _mock_result())
        hashes = [e.this_hash for e in self.log.entries]
        assert len(set(hashes)) == 5   # all unique

    def test_hash_chain_links_prev_to_next(self):
        for _ in range(3):
            self.log.log(_mock_packet(), _mock_result())
        entries = self.log.entries
        assert entries[1].previous_hash == entries[0].this_hash
        assert entries[2].previous_hash == entries[1].this_hash

    # ── Privacy: No Neural Payload in Log ───────────────────────────────────

    def test_no_raw_neural_payload_in_entries(self):
        """GDPR requirement: log must never store neural payload."""
        pkt = _mock_packet()
        pkt.neural_payload = "SECRET_THOUGHT_CONTENT"
        self.log.log(pkt, _mock_result())
        entry = self.log.entries[0]
        entry_dict = vars(entry)
        for key, val in entry_dict.items():
            assert "SECRET_THOUGHT_CONTENT" not in str(val), \
                f"Neural payload leaked in field: {key}"

    def test_session_id_is_hashed_not_plaintext(self):
        """Session IDs must be hashed in the audit log."""
        pkt = _mock_packet(source="REAL_USER_ID")
        self.log.log(pkt, _mock_result())
        entry = self.log.entries[0]
        assert "REAL_USER_ID" not in entry.session_hash

    # ── Export ───────────────────────────────────────────────────────────────

    def test_export_json(self):
        for _ in range(3):
            self.log.log(_mock_packet(), _mock_result())
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "audit", "log.json")
            self.log.export_json(path)
            assert os.path.exists(path)
            with open(path) as f:
                data = json.load(f)
            assert len(data) == 3
            # Verify no raw payload fields
            for entry in data:
                assert "neural_payload" not in entry
                assert "raw_eeg" not in entry
                assert "thought_content" not in entry
