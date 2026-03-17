"""
context_frame.py — Contextual Framing Layer (Data Link Layer)
Sprint 1 | Owner: เจม (Network Architect)

แนบ Emotion Vectors (Valence/Arousal) เข้ากับ Neural Symbol
ก่อนส่งเข้า TTP Transport Layer
"""

import time
from dataclasses import dataclass


@dataclass
class ContextFrame:
    """
    Contextual Frame (32 bytes) — Data Link Layer payload.

    Encapsulates a neural symbol with its emotional/contextual metadata.
    """
    neural_symbol_id: int     # From Neural Dictionary
    valence:          float   # -1.0 (negative) to +1.0 (positive)
    arousal:          float   # 0.0 (calm) to 1.0 (excited)
    intensity:        float   # Signal strength 0.0–1.0
    timestamp_us:     int     # Microsecond timestamp
    cognitive_anchor: str     # Subject ID (sender)

    def assemble_with_ttp(self, source_id: str, dest_id: str,
                          consent_score: float, domain: str = "neuro"):
        """
        Assemble this frame into a TTPPacket.
        Assembly must complete in < 5ms (Sprint 1 AC for BNET-202).
        """
        from src.protocol.ttp_packet import TTPHeader, TTPPacket

        t0 = time.perf_counter()
        header = TTPHeader(
            source_id=source_id,
            dest_id=dest_id,
            symbol_id=self.neural_symbol_id,
        )
        packet = TTPPacket(
            header=header,
            symbol=_symbol_id_to_name(self.neural_symbol_id),
            valence=self.valence,
            arousal=self.arousal,
            intensity=self.intensity,
            consent_score=consent_score,
            domain=domain,
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000
        assert elapsed_ms < 5.0, f"Assembly too slow: {elapsed_ms:.2f}ms (limit 5ms)"
        return packet


SYMBOL_MAP = {0: "focus", 1: "relax", 2: "reject", 3: "neutral"}


def _symbol_id_to_name(symbol_id: int) -> str:
    return SYMBOL_MAP.get(symbol_id, f"unknown_{symbol_id}")
