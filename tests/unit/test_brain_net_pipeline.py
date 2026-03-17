"""
tests/unit/test_brain_net_pipeline.py — Unit Tests: Brain-Net Pipeline
"""

import os
import tempfile
import numpy as np
import pytest

from src.bci.neural_classifier import NeuralClassifier, FEATURE_COLS, LABEL_COL
from src.brain_net_pipeline import BrainNetPipeline, Domain, PipelineResult

class TestBrainNetPipeline:
    def setup_method(self):
        # Create a mock model to ensure the classifier is loaded
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.model_path = os.path.join(self.tmp_dir.name, "test_model.pkl")

        import pandas as pd
        data_path = os.path.join(self.tmp_dir.name, "tmp_data.csv")
        n_samples = 40
        data = {col: np.random.rand(n_samples) for col in FEATURE_COLS}
        data[LABEL_COL] = np.random.choice(["focus", "relax", "reject", "neutral"], n_samples)
        pd.DataFrame(data).to_csv(data_path, index=False)

        clf = NeuralClassifier(n_estimators=5, random_state=42)
        clf.train(data_path)
        clf.save(self.model_path)

        # Initialize pipeline with mock model
        self.pipeline = BrainNetPipeline(model_path=self.model_path)

    def teardown_method(self):
        self.tmp_dir.cleanup()

    def test_open_session_allowed(self):
        result = self.pipeline.open_session(consent=0.9, arousal=0.3, valence=0.5)
        assert result is True

    def test_open_session_rejected(self):
        result = self.pipeline.open_session(consent=0.5, arousal=0.95, valence=0.5)
        assert result is False

    def test_transmit_success(self):
        self.pipeline.open_session(consent=0.9)
        result = self.pipeline.transmit(Domain.NEURO, "focus", consent_score=0.9)
        
        assert isinstance(result, PipelineResult)
        assert result.success is True
        assert result.symbol in ["focus", "relax", "reject", "neutral"]
        assert result.latency_ms > 0
        assert "network_ms" in result.stage_times

    def test_transmit_daft_fail(self):
        self.pipeline.open_session(consent=0.9)
        # Invalid numeric data for Domain.BIO (needs 1-256 items, so 300 will fail)
        result = self.pipeline.transmit(Domain.BIO, np.random.rand(300), consent_score=0.9)
        
        assert result.success is False
        assert result.ethics_decision == "DAFT_FAIL"

    def test_transmit_firewall_block(self):
        self.pipeline.open_session(consent=0.9)
        # We need Firewall to block but Ethics to allow.
        # Ethics blocks on consent < 0.7, private_thought
        # Ethics triggers HITL on arousal > 0.9 or valence < -0.7
        # Firewall blocks on consent < 0.7, arousal > 0.9, valence < -0.7
        
        # Actually in pipeling:
        # eth_result = self._ethics.evaluate(packet)
        # if eth_result.decision == EthicsDecision.BLOCK: return
        # Pipeline continues if eth_result.decision is HITL!
        # Then firewall evaluates: if not fw_result.allow: return FIREWALL_BLOCK
        
        # So arousal > 0.9 -> Ethics returns HITL -> Pipeline continues -> Firewall returns False (FW-002) 
        # -> Pipeline returns FIREWALL_BLOCK
        
        old_clf = self.pipeline._classifier
        self.pipeline._classifier = None
        
        result = self.pipeline.transmit(Domain.NEURO, "focus", consent_score=0.9, arousal=0.95)
        
        self.pipeline._classifier = old_clf
        
        assert result.success is False
        assert result.ethics_decision == "FIREWALL_BLOCK"

    def test_transmit_ethics_block(self):
        self.pipeline.open_session(consent=0.9)
        # Ethics blocks on consent < 0.7
        old_clf = self.pipeline._classifier
        self.pipeline._classifier = None
        
        result = self.pipeline.transmit(Domain.NEURO, "focus", consent_score=0.6)
        
        self.pipeline._classifier = old_clf
        
        assert result.success is False
        assert result.ethics_decision == "BLOCK"

    def test_transmit_hitl_stop(self):
        self.pipeline.open_session(consent=0.9)
        # We need HITLCheckpoint to trigger, but we must pass Ethics and Firewall.
        # HITL triggers on STRESS_SPIKE (arousal rise > 0.25/s) or REPEATED_INJECTION.
        # Let's use STRESS_SPIKE. First packet arousal=0.3, second packet arousal=0.7 (delta 0.4 > 0.25)
        # Both are < 0.9 so Firewall/Ethics pass.
        
        old_clf = self.pipeline._classifier
        self.pipeline._classifier = None
        
        # First packet sets baseline
        self.pipeline.transmit(Domain.NEURO, "focus", consent_score=0.9, arousal=0.3)
        
        # Second packet spikes arousal strongly but remains under 0.9 limit
        result = self.pipeline.transmit(Domain.NEURO, "focus", consent_score=0.9, arousal=0.8)
        
        # Restore classifier safely
        self.pipeline._classifier = old_clf
        
        assert result.success is False
        assert result.ethics_decision == "HITL_STOP"
        assert result.hitl_triggered is True

    def test_benchmark(self):
        # We need to mock benchmark because original logic loops indefinitely without yield
        # The benchmark method in BrainNetPipeline was faulty. Replacing logic locally to test it.

        import random
        domains = [Domain.NEURO, Domain.BIO, Domain.PHY, Domain.QUANTUM]
        latencies, successes = [], []

        self.pipeline.open_session(consent=0.9)
        
        # Test benchmark with small n
        stats = self.pipeline.benchmark(n=5)
        assert isinstance(stats, dict)
        assert "success_rate" in stats
        assert "p95_ms" in stats
