"""
tests/unit/test_mock_qkd.py — Unit Tests: MockQKD (AES-256-GCM)
Sprint 1–2 | Owner: โยรุ

Tests: encrypt/decrypt roundtrip, nonce uniqueness, overhead timing, tamper detection
"""

import os
import time
import pytest
from src.crypto.mock_qkd_aes import MockQKD


class TestMockQKD:

    def setup_method(self):
        self.qkd = MockQKD(reuse_key=True)

    # ── Encrypt / Decrypt Roundtrip ──────────────────────────────────────────

    def test_encrypt_decrypt_roundtrip(self):
        data = b"Brain-Net test payload"
        ciphertext, nonce = self.qkd.encrypt(data)
        plaintext = self.qkd.decrypt(ciphertext, nonce)
        assert plaintext == data

    def test_encrypt_packet_roundtrip(self):
        packet_bytes = os.urandom(72)   # typical TTP packet size
        encrypted = self.qkd.encrypt_packet(packet_bytes)
        decrypted = self.qkd.decrypt_packet(encrypted)
        assert decrypted == packet_bytes

    def test_encrypt_returns_different_bytes(self):
        data = b"same data"
        c1, n1 = self.qkd.encrypt(data)
        c2, n2 = self.qkd.encrypt(data)
        # Nonces should be different (random)
        assert n1 != n2

    def test_encrypt_packet_prepends_12_byte_nonce(self):
        data = os.urandom(64)
        encrypted = self.qkd.encrypt_packet(data)
        # Ciphertext should be nonce(12) + data(64) + tag(16) = 92 bytes
        assert len(encrypted) == 12 + 64 + 16

    # ── Key Management ───────────────────────────────────────────────────────

    def test_key_is_256_bits(self):
        assert len(self.qkd._session_key) == 32

    def test_rotate_key_changes_key(self):
        old_key = self.qkd._session_key
        self.qkd.rotate_key()
        assert self.qkd._session_key != old_key

    # ── Tamper Detection ─────────────────────────────────────────────────────

    def test_tampered_ciphertext_raises(self):
        data = b"sensitive data"
        encrypted = self.qkd.encrypt_packet(data)
        # Flip a byte in the ciphertext portion
        tampered = bytearray(encrypted)
        tampered[20] ^= 0xFF
        from cryptography.exceptions import InvalidTag
        with pytest.raises((InvalidTag, Exception)):
            self.qkd.decrypt_packet(bytes(tampered))

    # ── Overhead Timing ──────────────────────────────────────────────────────

    def test_single_enc_dec_under_15ms(self):
        """Quality Gate: encryption overhead < 15ms (Mock QKD)."""
        data = os.urandom(128)
        t0 = time.perf_counter()
        enc, nonce = self.qkd.encrypt(data)
        self.qkd.decrypt(enc, nonce)
        elapsed = (time.perf_counter() - t0) * 1000
        assert elapsed < 15.0, f"Overhead {elapsed:.2f}ms exceeds 15ms target"

    def test_benchmark_passes_15ms_target(self):
        results = self.qkd.benchmark(n=50)
        assert results["passes_15ms"] is True

    def test_benchmark_returns_expected_keys(self):
        results = self.qkd.benchmark(n=10)
        for key in ["avg_enc_ms", "avg_dec_ms", "avg_total_ms", "max_total_ms", "passes_15ms"]:
            assert key in results
