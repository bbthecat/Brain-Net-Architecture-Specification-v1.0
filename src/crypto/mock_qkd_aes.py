"""
mock_qkd_aes.py — Mock Quantum Key Distribution using AES-256
Sprint 1–2 | Owner: โยรุ (Quantum Specialist)

Classical fallback for QKD. Overhead target: < 15ms.
"""

import os
import time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class MockQKD:
    """
    AES-256-GCM encryption simulating future QKD pipeline.
    Key is regenerated per session (simulates QKD key exchange).
    """

    def __init__(self, reuse_key: bool = True):
        """
        Args:
            reuse_key: Cache session key to reduce overhead (Sprint 2 optimization).
        """
        self._reuse_key = reuse_key
        self._session_key: bytes = self._generate_key()
        self._aesgcm = AESGCM(self._session_key)

    # ── Key Management ───────────────────────────────────────────────────────

    def _generate_key(self) -> bytes:
        return os.urandom(32)   # 256-bit key

    def rotate_key(self):
        """Simulate QKD key rotation (new entanglement session)."""
        self._session_key = self._generate_key()
        self._aesgcm = AESGCM(self._session_key)

    # ── Encryption / Decryption ──────────────────────────────────────────────

    def encrypt(self, data: bytes) -> tuple[bytes, bytes]:
        """
        Encrypt data. Returns (ciphertext, nonce).
        Overhead target: < 15ms total for enc+dec.
        """
        nonce = os.urandom(12)
        ciphertext = self._aesgcm.encrypt(nonce, data, None)
        return ciphertext, nonce

    def decrypt(self, ciphertext: bytes, nonce: bytes) -> bytes:
        """Decrypt data. Raises InvalidTag if tampered."""
        return self._aesgcm.decrypt(nonce, ciphertext, None)

    def encrypt_packet(self, packet_bytes: bytes) -> bytes:
        """Encrypt a TTP packet payload and prepend nonce."""
        ciphertext, nonce = self.encrypt(packet_bytes)
        return nonce + ciphertext   # 12B nonce + encrypted data

    def decrypt_packet(self, encrypted: bytes) -> bytes:
        """Decrypt a packet encrypted with encrypt_packet()."""
        nonce      = encrypted[:12]
        ciphertext = encrypted[12:]
        return self.decrypt(ciphertext, nonce)

    def benchmark(self, n: int = 100, data_size: int = 128) -> dict:
        """Measure encryption overhead."""
        data = os.urandom(data_size)
        enc_times, dec_times = [], []

        for _ in range(n):
            t0 = time.perf_counter()
            enc, nonce = self.encrypt(data)
            enc_times.append((time.perf_counter() - t0) * 1000)

            t0 = time.perf_counter()
            self.decrypt(enc, nonce)
            dec_times.append((time.perf_counter() - t0) * 1000)

        total = [e + d for e, d in zip(enc_times, dec_times)]
        return {
            "avg_enc_ms":   sum(enc_times) / n,
            "avg_dec_ms":   sum(dec_times) / n,
            "avg_total_ms": sum(total) / n,
            "max_total_ms": max(total),
            "passes_15ms":  max(total) < 15,
        }


if __name__ == "__main__":
    qkd = MockQKD(reuse_key=True)
    results = qkd.benchmark(n=100)
    for k, v in results.items():
        print(f"  {k}: {v}")
    status = "✅" if results["passes_15ms"] else "⚠️"
    print(f"\n{status} Max overhead: {results['max_total_ms']:.2f}ms (target < 15ms)")
