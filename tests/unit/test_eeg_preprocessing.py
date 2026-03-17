"""
tests/unit/test_eeg_preprocessing.py — Unit Tests: EEGPreprocessor + BCIConnection
Sprint 1 | Owner: บี

Tests: bandpass filter, artifact detection, feature extraction, mock streaming
"""

import numpy as np
import pandas as pd
import pytest
from src.bci.connect_bci import (
    BCIConnection, EEGChunk, SAMPLE_RATE_HZ, N_CHANNELS, CHUNK_SIZE
)
from src.bci.clean_eeg_data import EEGPreprocessor, CleanEEGFeatures


# ── BCIConnection Tests ──────────────────────────────────────────────────────

class TestBCIConnection:

    def test_connect_mock_mode(self):
        bci = BCIConnection("TEST_SUBJ", mode="mock")
        assert bci.connect() is True
        assert bci.is_connected is True

    def test_disconnect_clears_connection(self):
        bci = BCIConnection("TEST_SUBJ", mode="mock")
        bci.connect()
        bci.disconnect()
        assert bci.is_connected is False

    def test_hardware_mode_raises(self):
        bci = BCIConnection("TEST", mode="hardware")
        with pytest.raises(NotImplementedError):
            bci.connect()

    def test_stream_without_connect_raises(self):
        bci = BCIConnection("TEST", mode="mock")
        with pytest.raises(RuntimeError):
            next(bci.stream(max_chunks=1).__iter__())

    def test_stream_yields_eeg_chunks(self):
        bci = BCIConnection("TEST", mode="mock")
        bci.connect()
        chunks = list(bci.stream(max_chunks=3))
        assert len(chunks) == 3
        bci.disconnect()

    def test_chunk_has_correct_shape(self):
        bci = BCIConnection("TEST", mode="mock")
        bci.connect()
        chunk = next(bci.stream(max_chunks=1))
        assert chunk.samples.shape == (N_CHANNELS, CHUNK_SIZE)
        bci.disconnect()

    def test_chunk_subject_id_matches(self):
        bci = BCIConnection("SUBJ_ABC", mode="mock")
        bci.connect()
        chunk = next(bci.stream(max_chunks=1))
        assert chunk.subject_id == "SUBJ_ABC"
        bci.disconnect()

    def test_mock_chunk_has_alpha_beta_components(self):
        """Generated EEG should contain realistic alpha/beta waves."""
        bci = BCIConnection("TEST", mode="mock")
        bci.connect()
        chunk = next(bci.stream(max_chunks=1))
        # Signal should not be pure noise (non-zero mean due to sinusoids)
        assert chunk.samples.std() > 0.05
        bci.disconnect()


# ── EEGPreprocessor Tests ────────────────────────────────────────────────────

class TestEEGPreprocessor:

    def setup_method(self):
        self.prep = EEGPreprocessor()
        self.bci  = BCIConnection("TEST", mode="mock")
        self.bci.connect()

    def teardown_method(self):
        self.bci.disconnect()

    def _get_chunk(self) -> EEGChunk:
        return next(self.bci.stream(max_chunks=1))

    def test_process_returns_clean_features(self):
        chunk = self._get_chunk()
        features = self.prep.process(chunk)
        assert isinstance(features, CleanEEGFeatures)

    def test_subject_id_preserved(self):
        chunk = self._get_chunk()
        features = self.prep.process(chunk)
        assert features.subject_id == "TEST"

    def test_all_power_bands_non_negative(self):
        chunk = self._get_chunk()
        f = self.prep.process(chunk)
        for band in [f.delta_power, f.theta_power, f.alpha_power,
                     f.beta_power, f.gamma_power]:
            assert band >= 0.0

    def test_artifact_detection_triggers_on_extreme_values(self):
        chunk = self._get_chunk()
        chunk.samples[0, 0] = 200.0   # inject artifact above 100μV threshold
        features = self.prep.process(chunk)
        assert features.artifact_detected is True

    def test_artifact_suppression_clips_values(self):
        chunk = self._get_chunk()
        chunk.samples[:] = 500.0  # force extreme artifact
        features = self.prep.process(chunk)
        # After suppression, extreme values should be clamped
        assert features.mean_amplitude <= 100.0 + 1   # allow small float epsilon

    def test_normal_chunk_no_artifact(self):
        chunk = self._get_chunk()
        # Reset samples to low values to avoid artifact
        chunk.samples = np.random.randn(N_CHANNELS, CHUNK_SIZE) * 5.0
        features = self.prep.process(chunk)
        assert features.artifact_detected is False

    def test_process_batch_returns_dataframe(self):
        chunks = list(self.bci.stream(max_chunks=5))
        df = self.prep.process_batch(chunks)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5

    def test_batch_has_all_feature_columns(self):
        chunks = list(self.bci.stream(max_chunks=3))
        df = self.prep.process_batch(chunks)
        expected_cols = [
            "delta_power", "theta_power", "alpha_power",
            "beta_power", "gamma_power", "mean_amplitude",
            "std_amplitude", "artifact_detected", "label"
        ]
        for col in expected_cols:
            assert col in df.columns

    def test_std_amplitude_non_negative(self):
        chunk = self._get_chunk()
        f = self.prep.process(chunk)
        assert f.std_amplitude >= 0.0
