"""
connect_bci.py — BCI Hardware Connection & Raw EEG Stream
Sprint 1 | Owner: บี (BCI Engineer)

จำลองการเชื่อมต่อ BCI Headset และส่ง Raw EEG Stream
ใน Phase 1 ใช้ Simulated Data แทน Hardware จริง
"""

import numpy as np
import time
from dataclasses import dataclass, field
from typing import Generator


# ── Constants ──────────────────────────────────────────────────────────────
SAMPLE_RATE_HZ = 256          # EEG sampling rate (Hz)
N_CHANNELS = 14               # Number of EEG channels
CHUNK_DURATION_S = 0.125      # 125ms chunks (32 samples)
CHUNK_SIZE = int(SAMPLE_RATE_HZ * CHUNK_DURATION_S)

EEG_BANDS = {
    "delta":  (0.5, 4),
    "theta":  (4,   8),
    "alpha":  (8,   13),
    "beta":   (13,  30),
    "gamma":  (30,  100),
}


@dataclass
class EEGChunk:
    """One chunk of raw EEG data from BCI hardware."""
    subject_id: str
    timestamp: float
    samples: np.ndarray          # shape: (n_channels, chunk_size)
    sample_rate: int = SAMPLE_RATE_HZ
    channel_names: list = field(default_factory=lambda: [f"CH{i}" for i in range(N_CHANNELS)])

    def __post_init__(self):
        assert self.samples.shape == (N_CHANNELS, CHUNK_SIZE), \
            f"Expected shape ({N_CHANNELS}, {CHUNK_SIZE}), got {self.samples.shape}"


class BCIConnection:
    """
    Manages connection to BCI Headset (simulated in Phase 1).

    Usage:
        bci = BCIConnection(subject_id="SUBJ_001")
        bci.connect()
        for chunk in bci.stream():
            process(chunk)
        bci.disconnect()
    """

    def __init__(self, subject_id: str, mode: str = "mock"):
        """
        Args:
            subject_id: Unique identifier for the subject.
            mode: 'mock' uses simulated EEG data; 'hardware' connects to real device.
        """
        self.subject_id = subject_id
        self.mode = mode
        self._connected = False
        self._session_start: float = 0.0

    # ── Connection ──────────────────────────────────────────────────────────

    def connect(self) -> bool:
        """Establish connection to BCI device."""
        if self.mode == "hardware":
            raise NotImplementedError("Hardware BCI not available in Phase 1 — use mode='mock'")
        self._connected = True
        self._session_start = time.time()
        print(f"[BCI] Connected (mock) | Subject: {self.subject_id}")
        return True

    def disconnect(self):
        """Gracefully disconnect and clear session buffers."""
        self._connected = False
        duration = time.time() - self._session_start
        print(f"[BCI] Disconnected | Session duration: {duration:.1f}s")

    @property
    def is_connected(self) -> bool:
        return self._connected

    # ── Streaming ───────────────────────────────────────────────────────────

    def stream(self, max_chunks: int = None) -> Generator[EEGChunk, None, None]:
        """
        Yield EEG data chunks continuously.

        Args:
            max_chunks: Stop after this many chunks (None = stream forever).
        Yields:
            EEGChunk with simulated raw EEG data.
        """
        if not self._connected:
            raise RuntimeError("Not connected — call connect() first")

        count = 0
        while max_chunks is None or count < max_chunks:
            yield self._generate_mock_chunk()
            count += 1
            time.sleep(CHUNK_DURATION_S)

    def _generate_mock_chunk(self) -> EEGChunk:
        """Generate realistic simulated EEG data with alpha/beta bands."""
        t = np.linspace(0, CHUNK_DURATION_S, CHUNK_SIZE)
        samples = np.zeros((N_CHANNELS, CHUNK_SIZE))

        for ch in range(N_CHANNELS):
            # Alpha wave (8–13 Hz) dominant in relaxed state
            alpha = 0.5 * np.sin(2 * np.pi * 10 * t + np.random.uniform(0, 2 * np.pi))
            # Beta wave (13–30 Hz) for focused state
            beta = 0.3 * np.sin(2 * np.pi * 20 * t + np.random.uniform(0, 2 * np.pi))
            # Background noise
            noise = 0.1 * np.random.randn(CHUNK_SIZE)
            # Eye blink artifact (occasional)
            artifact = np.zeros(CHUNK_SIZE)
            if np.random.rand() < 0.05:
                blink_pos = np.random.randint(0, CHUNK_SIZE)
                artifact[blink_pos:blink_pos+3] = np.random.uniform(50, 100)

            samples[ch] = alpha + beta + noise + artifact

        return EEGChunk(
            subject_id=self.subject_id,
            timestamp=time.time(),
            samples=samples,
        )


# ── CLI entry point ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    bci = BCIConnection(subject_id="SUBJ_DEMO", mode="mock")
    bci.connect()
    print("[BCI] Streaming 5 chunks...")
    for i, chunk in enumerate(bci.stream(max_chunks=5)):
        print(f"  Chunk {i+1}: shape={chunk.samples.shape}, "
              f"mean={chunk.samples.mean():.4f}, ts={chunk.timestamp:.3f}")
    bci.disconnect()
