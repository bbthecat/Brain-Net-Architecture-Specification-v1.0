"""
tests/unit/test_neural_classifier.py — Unit Tests: ML Neural Dictionary Classifier
"""

import os
import tempfile
import numpy as np
import pandas as pd
import pytest

from src.bci.neural_classifier import NeuralClassifier, ClassificationResult, FEATURE_COLS, LABEL_COL

class TestNeuralClassifier:
    def setup_method(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.data_path = os.path.join(self.tmp_dir.name, "test_eeg_data.csv")
        self.model_path = os.path.join(self.tmp_dir.name, "test_model.pkl")

        # Generate a small mock dataset
        np.random.seed(42)
        n_samples = 100
        data = {col: np.random.rand(n_samples) for col in FEATURE_COLS}
        data[LABEL_COL] = np.random.choice(["focus", "relax", "reject", "neutral"], n_samples)
        pd.DataFrame(data).to_csv(self.data_path, index=False)
        
        self.clf = NeuralClassifier(n_estimators=10, random_state=42)

    def teardown_method(self):
        self.tmp_dir.cleanup()

    def test_train(self):
        acc = self.clf.train(self.data_path)
        assert acc >= 0.0
        assert self.clf._trained is True
        assert len(self.clf.classes) == 4

    def test_cross_validate(self):
        self.clf.train(self.data_path)
        mean_acc = self.clf.cross_validate(self.data_path, cv=2)
        assert mean_acc >= 0.0

    def test_predict_requires_trained(self):
        clf = NeuralClassifier()
        with pytest.raises(RuntimeError, match="Model not trained"):
            clf.predict(np.random.rand(7))

    def test_predict(self):
        self.clf.train(self.data_path)
        features = np.random.rand(7)
        result = self.clf.predict(features)
        
        assert isinstance(result, ClassificationResult)
        assert result.symbol in ["focus", "relax", "reject", "neutral"]
        assert 0.0 <= result.confidence <= 1.0
        assert result.inference_time_ms > 0

    def test_predict_from_features_dict(self):
        self.clf.train(self.data_path)
        features_dict = {col: np.random.rand() for col in FEATURE_COLS}
        result = self.clf.predict_from_features_dict(features_dict)
        
        assert isinstance(result, ClassificationResult)
        assert result.symbol in ["focus", "relax", "reject", "neutral"]

    def test_save_load(self):
        self.clf.train(self.data_path)
        self.clf.save(self.model_path)
        assert os.path.exists(self.model_path)
        
        loaded = NeuralClassifier.load(self.model_path)
        assert loaded._trained is True
        assert loaded.accuracy == self.clf.accuracy
        assert len(loaded.classes) == len(self.clf.classes)
        
        features = np.random.rand(7)
        result_original = self.clf.predict(features)
        result_loaded = loaded.predict(features)
        
        assert result_original.symbol == result_loaded.symbol
        assert abs(result_original.confidence - result_loaded.confidence) < 1e-6
