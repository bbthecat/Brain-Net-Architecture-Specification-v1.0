"""
ttp_packet.py — Thought Transfer Protocol: Packet & Header
Sprint 1 | Owner: เจม (Network Architect)

TTPHeader:  32-byte header for routing symbolic neural data
TTPPacket:  Full packet = header + contextual frame payload
"""

import struct
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


# ── TTP Header (32 bytes) ────────────────────────────────────────────────────

@dataclass
class TTPHeader:
    """
    Thought Transfer Protocol Header.

    Format (32 bytes total):
      source_id     : 8B  — sender node identifier (hashed)
      dest_id       : 8B  — receiver node identifier (hashed)
      packet_id     : 4B  — unique packet sequence number
      symbol_id     : 4B  — Neural Dictionary Symbol ID
      timestamp_us  : 8B  — microsecond timestamp
    """
    source_id:    str
    dest_id:      str
    symbol_id:    int
    packet_id:    int = field(default_factory=lambda: int(uuid.uuid4()) & 0xFFFFFFFF)
    timestamp_us: int = field(default_factory=lambda: int(time.time() * 1_000_000))

    # ── Serialization ──────────────────────────────────────────────────────

    def pack(self) -> bytes:
        """Serialize header to 32 bytes."""
        src_bytes  = self.source_id.encode()[:8].ljust(8, b'\x00')
        dest_bytes = self.dest_id.encode()[:8].ljust(8, b'\x00')
        body = struct.pack(">II Q", self.packet_id, self.symbol_id, self.timestamp_us)
        return src_bytes + dest_bytes + body  # 8+8+4+4+8 = 32 bytes

    @classmethod
    def unpack(cls, data: bytes) -> "TTPHeader":
        """Deserialize header from 32 bytes."""
        assert len(data) >= 32, f"Header too short: {len(data)} bytes"
        source_id    = data[0:8].rstrip(b'\x00').decode()
        dest_id      = data[8:16].rstrip(b'\x00').decode()
        packet_id, symbol_id, timestamp_us = struct.unpack(">IIQ", data[16:32])
        return cls(source_id=source_id, dest_id=dest_id,
                   symbol_id=symbol_id, packet_id=packet_id,
                   timestamp_us=timestamp_us)

    @property
    def age_ms(self) -> float:
        """Milliseconds since this packet was created."""
        return (time.time() * 1_000_000 - self.timestamp_us) / 1000


# ── TTP Packet ───────────────────────────────────────────────────────────────

@dataclass
class TTPPacket:
    """
    Full TTP Packet = Header + Contextual Framing Payload.

    The payload contains the ContextFrame (emotion vectors, intensity)
    but NEVER the raw neural/thought content (privacy boundary).
    """
    header:       TTPHeader
    symbol:       str             # Human-readable symbol: "focus", "relax", etc.
    valence:      float           # -1.0 (negative) to +1.0 (positive)
    arousal:      float           # 0.0 (calm) to 1.0 (excited)
    intensity:    float           # 0.0 to 1.0  — signal strength
    consent_score: float          # 0.0 to 1.0  — calculated consent level
    domain:       str = "neuro"   # bio | phy | neuro | quantum
    encrypted:    bool = False
    _payload_bytes: Optional[bytes] = field(default=None, repr=False)

    def __post_init__(self):
        # Clamp values
        self.valence       = max(-1.0, min(1.0, self.valence))
        self.arousal       = max(0.0,  min(1.0, self.arousal))
        self.intensity     = max(0.0,  min(1.0, self.intensity))
        self.consent_score = max(0.0,  min(1.0, self.consent_score))

    # ── Serialization ──────────────────────────────────────────────────────

    def pack(self) -> bytes:
        """Serialize full packet to bytes."""
        header_bytes = self.header.pack()
        symbol_bytes = self.symbol.encode()[:16].ljust(16, b'\x00')
        payload = struct.pack(">ffff", self.valence, self.arousal,
                              self.intensity, self.consent_score)
        domain_byte = self.domain.encode()[:8].ljust(8, b'\x00')
        return header_bytes + symbol_bytes + payload + domain_byte

    @classmethod
    def unpack(cls, data: bytes) -> "TTPPacket":
        """Deserialize packet from bytes."""
        header       = TTPHeader.unpack(data[:32])
        symbol       = data[32:48].rstrip(b'\x00').decode()
        valence, arousal, intensity, consent = struct.unpack(">ffff", data[48:64])
        domain       = data[64:72].rstrip(b'\x00').decode() if len(data) >= 72 else "neuro"
        return cls(header=header, symbol=symbol, valence=valence,
                   arousal=arousal, intensity=intensity,
                   consent_score=consent, domain=domain)

    # ── Convenience ────────────────────────────────────────────────────────

    @property
    def is_safe_to_transmit(self) -> bool:
        """Quick safety check before entering TTP pipeline."""
        return (self.consent_score >= 0.5
                and self.arousal <= 0.9
                and not self.header.age_ms > 50)

    def summary(self) -> str:
        return (f"TTPPacket[{self.header.packet_id}] "
                f"symbol={self.symbol} consent={self.consent_score:.2f} "
                f"arousal={self.arousal:.2f} domain={self.domain} "
                f"age={self.header.age_ms:.1f}ms")
