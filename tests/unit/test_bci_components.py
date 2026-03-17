"""
tests/unit/test_bci_components.py — Unit Tests for BCI Connection and Preprocessing
"""

import numpy as np
import pandas as pd
import pytest
import os
import tempfile
from src.bci.connect_bci import BCIConnection, EEGChunk, N_CHANNELS, CHUNK_SIZE
from src.bci.clean_eeg_data import EEGPreprocessor, CleanEEGFeatures, generate_mock_dataset

class TestBCIComponents:
    def setup_method(self):
        self.subject_id = "TEST_SUBJ"
        self.bci = BCIConnection(self.subject_id, mode="mock")
        self.prep = EEGPreprocessor()

    def test_bci_connection_lifecycle(self):
        assert self.bci.is_connected is False
        self.bci.connect()
        assert self.bci.is_connected is True
        self.bci.disconnect()
        assert self.bci.is_connected is False

    def test_bci_stream_requires_connection(self):
        with pytest.raises(RuntimeError, match="Not connected"):
            next(self.bci.stream(max_chunks=1))

    def test_bci_stream_mock_data(self):
        self.bci.connect()
        stream = self.bci.stream(max_chunks=2)
        chunks = list(stream)
        assert len(chunks) == 2
        assert isinstance(chunks[0], EEGChunk)
        assert chunks[0].samples.shape == (N_CHANNELS, CHUNK_SIZE)
        self.bci.disconnect()

    def test_preprocessor_pipeline(self):
        # Generate a mock chunk
        self.bci.connect()
        chunk = self.bci._generate_mock_chunk()
        self.bci.disconnect()

        features = self.prep.process(chunk)
        assert isinstance(features, CleanEEGFeatures)
        assert features.subject_id == self.subject_id
        assert features.alpha_power >= 0
        assert features.beta_power >= 0
        assert isinstance(features.artifact_detected, bool)

    def test_preprocessor_batch(self):
        self.bci.connect()
        chunks = [self.bci._generate_mock_chunk() for _ in range(3)]
        self.bci.disconnect()

        df = self.prep.process_batch(chunks)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert "alpha_power" in df.columns

    def test_artifact_detection_and_suppression(self):
        # Create a chunk with a massive spike
        samples = np.zeros((N_CHANNELS, CHUNK_SIZE))
        samples[0, 0] = 500.0  # Well above threshold 100.0
        chunk = EEGChunk(subject_id="SPIKE", timestamp=1.0, samples=samples)

        features = self.prep.process(chunk)
        assert features.artifact_detected is True
        # Check if internal _suppress_artifact worked (clipping)
        processed_samples = self.prep._bandpass_filter(chunk.samples) # Filtered first
        # We manually test suppression logic
        clipped = self.prep._suppress_artifact(samples)
        assert clipped.max() <= 100.0

    def test_generate_mock_dataset(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = os.path.join(tmp_dir, "mock_data.csv")
            df = generate_mock_dataset(n_samples=6, save_path=csv_path)
            assert os.path.exists(csv_path)
            assert len(df) == 6
            assert set(df["label"].unique()).issubset({"focus", "relax", "reject"})
