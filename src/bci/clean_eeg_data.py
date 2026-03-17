"""
clean_eeg_data.py — EEG Preprocessing Pipeline
Sprint 1 | Owner: บี (BCI Engineer)

Bandpass filter, artifact rejection, feature extraction
"""

import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt
from dataclasses import dataclass
from typing import Tuple

from src.bci.connect_bci import EEGChunk, SAMPLE_RATE_HZ


# ── Constants ───────────────────────────────────────────────────────────────
BANDPASS_LOW_HZ  = 1.0
BANDPASS_HIGH_HZ = 50.0
ARTIFACT_THRESHOLD = 100.0    # μV — reject samples above this


@dataclass
class CleanEEGFeatures:
    """Extracted features from one cleaned EEG chunk."""
    subject_id: str
    timestamp: float
    delta_power: float    # 0.5–4 Hz
    theta_power: float    # 4–8 Hz
    alpha_power: float    # 8–13 Hz
    beta_power:  float    # 13–30 Hz
    gamma_power: float    # 30–50 Hz
    mean_amplitude: float
    std_amplitude:  float
    artifact_detected: bool
    label: str = "unknown"   # focus | relax | reject | neutral


class EEGPreprocessor:
    """
    Cleans raw EEG chunks and extracts spectral features.

    Pipeline:
        1. Bandpass filter (1–50 Hz)
        2. Artifact rejection (threshold-based)
        3. Power Spectral Density per band
        4. Statistical features
    """

    def __init__(self,
                 sample_rate: int = SAMPLE_RATE_HZ,
                 bandpass_low: float = BANDPASS_LOW_HZ,
                 bandpass_high: float = BANDPASS_HIGH_HZ,
                 artifact_threshold: float = ARTIFACT_THRESHOLD):
        self.sample_rate = sample_rate
        self.bandpass_low = bandpass_low
        self.bandpass_high = bandpass_high
        self.artifact_threshold = artifact_threshold
        self._b, self._a = self._design_bandpass_filter()

    # ── Public API ──────────────────────────────────────────────────────────

    def process(self, chunk: EEGChunk) -> CleanEEGFeatures:
        """Full preprocessing pipeline for one EEG chunk."""
        filtered = self._bandpass_filter(chunk.samples)
        artifact = self._detect_artifact(filtered)
        if artifact:
            filtered = self._suppress_artifact(filtered)

        features = self._extract_features(filtered)
        return CleanEEGFeatures(
            subject_id=chunk.subject_id,
            timestamp=chunk.timestamp,
            artifact_detected=artifact,
            **features,
        )

    def process_batch(self, chunks: list) -> pd.DataFrame:
        """Process a list of EEGChunks and return a DataFrame."""
        rows = []
        for chunk in chunks:
            f = self.process(chunk)
            rows.append({
                "subject_id":       f.subject_id,
                "timestamp":        f.timestamp,
                "delta_power":      f.delta_power,
                "theta_power":      f.theta_power,
                "alpha_power":      f.alpha_power,
                "beta_power":       f.beta_power,
                "gamma_power":      f.gamma_power,
                "mean_amplitude":   f.mean_amplitude,
                "std_amplitude":    f.std_amplitude,
                "artifact_detected": f.artifact_detected,
                "label":            f.label,
            })
        return pd.DataFrame(rows)

    # ── Private helpers ─────────────────────────────────────────────────────

    def _design_bandpass_filter(self) -> Tuple:
        nyq = self.sample_rate / 2
        low  = self.bandpass_low  / nyq
        high = self.bandpass_high / nyq
        b, a = butter(4, [low, high], btype="band")
        return b, a

    def _bandpass_filter(self, samples: np.ndarray) -> np.ndarray:
        return filtfilt(self._b, self._a, samples, axis=1)

    def _detect_artifact(self, samples: np.ndarray) -> bool:
        return bool(np.any(np.abs(samples) > self.artifact_threshold))

    def _suppress_artifact(self, samples: np.ndarray) -> np.ndarray:
        """Clip extreme values (simple artifact suppression)."""
        return np.clip(samples, -self.artifact_threshold, self.artifact_threshold)

    def _band_power(self, samples: np.ndarray, low: float, high: float) -> float:
        """Average power in a frequency band across all channels."""
        nyq = self.sample_rate / 2
        b, a = butter(4, [low / nyq, high / nyq], btype="band")
        filtered = filtfilt(b, a, samples, axis=1)
        return float(np.mean(filtered ** 2))

    def _extract_features(self, samples: np.ndarray) -> dict:
        return {
            "delta_power":    self._band_power(samples, 0.5, 4),
            "theta_power":    self._band_power(samples, 4,   8),
            "alpha_power":    self._band_power(samples, 8,   13),
            "beta_power":     self._band_power(samples, 13,  30),
            "gamma_power":    self._band_power(samples, 30,  50),
            "mean_amplitude": float(np.mean(samples)),
            "std_amplitude":  float(np.std(samples)),
        }


def generate_mock_dataset(n_samples: int = 300, save_path: str = "data/clean_eeg_data.csv") -> pd.DataFrame:
    """
    Generate a labeled mock EEG dataset for ML training.
    Labels: focus (0), relax (1), reject (2)
    """
    import os
    from src.bci.connect_bci import BCIConnection

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    bci = BCIConnection("MOCK_GEN", mode="mock")
    bci.connect()
    prep = EEGPreprocessor()

    labels = ["focus", "relax", "reject"]
    rows = []

    for i in range(n_samples):
        chunk = next(bci.stream(max_chunks=1).__iter__() if False else iter([bci._generate_mock_chunk()]))
        features = prep.process(chunk)
        label = labels[i % 3]

        # Skew features to simulate different states
        row = {
            "delta_power":    features.delta_power + (0.1 if label == "relax" else 0),
            "theta_power":    features.theta_power,
            "alpha_power":    features.alpha_power + (0.2 if label == "relax" else 0),
            "beta_power":     features.beta_power  + (0.2 if label == "focus" else 0),
            "gamma_power":    features.gamma_power + (0.3 if label == "focus" else 0),
            "mean_amplitude": features.mean_amplitude,
            "std_amplitude":  features.std_amplitude + (0.5 if label == "reject" else 0),
            "label":          label,
        }
        rows.append(row)

    bci.disconnect()
    df = pd.DataFrame(rows)
    df.to_csv(save_path, index=False)
    print(f"[Preprocessor] Saved {len(df)} samples → {save_path}")
    return df


if __name__ == "__main__":
    df = generate_mock_dataset(n_samples=300)
    print(df["label"].value_counts())
    print(df.describe())
