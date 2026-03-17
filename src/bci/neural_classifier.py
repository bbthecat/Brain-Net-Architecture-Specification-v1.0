"""
neural_classifier.py — ML Neural Dictionary Classifier
Sprint 1–3 | Owner: บี (BCI Engineer)

Random Forest classifier: EEG features → Cognitive State Symbol
v1: Focus / Relax / Reject  (Sprint 1)
v2: + Neutral domain states (Sprint 3, multi-domain)
"""

import numpy as np
import pandas as pd
import joblib
import os
import time
from dataclasses import dataclass
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix

FEATURE_COLS = ["delta_power", "theta_power", "alpha_power",
                "beta_power", "gamma_power", "mean_amplitude", "std_amplitude"]
LABEL_COL    = "label"
MODEL_DIR    = "models"


@dataclass
class ClassificationResult:
    """Output of the ML classifier for one EEG chunk."""
    symbol: str            # focus | relax | reject | neutral
    confidence: float      # 0.0 – 1.0
    inference_time_ms: float
    domain: str = "neuro"


class NeuralClassifier:
    """
    Random Forest classifier mapping EEG features to Cognitive State Symbols.

    Usage:
        clf = NeuralClassifier()
        clf.train("data/clean_eeg_data.csv")
        clf.save("models/neural_dict_v1.pkl")

        loaded = NeuralClassifier.load("models/neural_dict_v1.pkl")
        result = loaded.predict(feature_vector)
    """

    def __init__(self, n_estimators: int = 200, random_state: int = 42):
        self._model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=10,
            min_samples_split=4,
            random_state=random_state,
            n_jobs=-1,
        )
        self._encoder = LabelEncoder()
        self._trained = False
        self._accuracy: float = 0.0

    # ── Training ────────────────────────────────────────────────────────────

    def train(self, data_path: str) -> float:
        """Train on CSV dataset. Returns holdout accuracy."""
        df = pd.read_csv(data_path)
        X = df[FEATURE_COLS].values
        y = self._encoder.fit_transform(df[LABEL_COL].values)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=42
        )
        self._model.fit(X_train, y_train)
        self._trained = True

        self._accuracy = self._model.score(X_test, y_test)
        y_pred = self._model.predict(X_test)
        labels = list(self._encoder.classes_)

        print(f"[ML] Holdout Accuracy: {self._accuracy:.4f} ({self._accuracy*100:.1f}%)")
        print("[ML] Classification Report:")
        print(classification_report(y_test, y_pred, target_names=labels))
        print("[ML] Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        return self._accuracy

    def cross_validate(self, data_path: str, cv: int = 5) -> float:
        """Run k-fold cross-validation. Returns mean CV accuracy."""
        df = pd.read_csv(data_path)
        X = df[FEATURE_COLS].values
        y = self._encoder.fit_transform(df[LABEL_COL].values)
        scores = cross_val_score(self._model, X, y, cv=cv, scoring="accuracy")
        mean_acc = scores.mean()
        print(f"[ML] CV({cv}) Accuracy: {mean_acc:.4f} ± {scores.std():.4f}")
        return mean_acc

    # ── Inference ───────────────────────────────────────────────────────────

    def predict(self, features: np.ndarray) -> ClassificationResult:
        """
        Predict cognitive state from feature vector.

        Args:
            features: 1D array of shape (7,) matching FEATURE_COLS
        """
        if not self._trained:
            raise RuntimeError("Model not trained — call train() or load() first")

        t0 = time.perf_counter()
        features_2d = features.reshape(1, -1)
        pred_idx   = self._model.predict(features_2d)[0]
        proba      = self._model.predict_proba(features_2d)[0]
        inference_ms = (time.perf_counter() - t0) * 1000

        symbol     = self._encoder.inverse_transform([pred_idx])[0]
        confidence = float(proba[pred_idx])

        return ClassificationResult(
            symbol=symbol,
            confidence=confidence,
            inference_time_ms=inference_ms,
        )

    def predict_from_features_dict(self, feat: dict) -> ClassificationResult:
        """Predict from a dict with FEATURE_COLS keys."""
        vec = np.array([feat[c] for c in FEATURE_COLS])
        return self.predict(vec)

    # ── Persistence ─────────────────────────────────────────────────────────

    def save(self, path: str):
        """Save model to disk."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({"model": self._model, "encoder": self._encoder,
                     "accuracy": self._accuracy}, path)
        print(f"[ML] Model saved -> {path}  (accuracy={self._accuracy:.3f})")

    @classmethod
    def load(cls, path: str) -> "NeuralClassifier":
        """Load model from disk."""
        data = joblib.load(path)
        obj = cls()
        obj._model    = data["model"]
        obj._encoder  = data["encoder"]
        obj._accuracy = data.get("accuracy", 0.0)
        obj._trained  = True
        print(f"[ML] Model loaded <- {path}  (accuracy={obj._accuracy:.3f})")
        return obj

    @property
    def accuracy(self) -> float:
        return self._accuracy

    @property
    def classes(self) -> list:
        return list(self._encoder.classes_) if self._trained else []


# ── CLI entry point ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    from src.bci.clean_eeg_data import generate_mock_dataset

    print("=== Brain-Net Neural Classifier ===")
    data_path  = "data/clean_eeg_data.csv"
    model_path = "models/neural_dict_v1.pkl"

    # Generate mock data if not present
    if not os.path.exists(data_path):
        print("[Setup] Generating mock EEG dataset...")
        generate_mock_dataset(n_samples=600, save_path=data_path)

    clf = NeuralClassifier()
    acc = clf.train(data_path)

    if acc >= 0.80:
        clf.save(model_path)
        print(f"\n✅ Model meets Sprint 1 target (≥80%) — saved to {model_path}")
    else:
        print(f"\n⚠️  Accuracy {acc:.1%} below 80% target — review ISS-001")
        clf.save(model_path)  # save anyway for debugging
