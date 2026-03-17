"""
data/generate_mock_dataset.py — Standalone Mock EEG Dataset Generator
Sprint 1 | Owner: บี (BCI Engineer)

Generates labeled synthetic EEG feature dataset for ML training.
Can be run directly: python data/generate_mock_dataset.py

Output: data/clean_eeg_data.csv
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

# Allow running from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bci.connect_bci import BCIConnection, SAMPLE_RATE_HZ
from src.bci.clean_eeg_data import EEGPreprocessor

# ── Constants ─────────────────────────────────────────────────────────────────

OUTPUT_PATH    = "data/clean_eeg_data.csv"
DEFAULT_N      = 600
LABELS         = ["focus", "relax", "reject", "neutral"]

# Per-label feature modifiers — simulate distinct EEG patterns
LABEL_MODIFIERS = {
    "focus":   {"alpha_power": 0.0, "beta_power": 0.3,  "gamma_power": 0.4, "std_amplitude": 0.3},
    "relax":   {"alpha_power": 0.4, "beta_power": 0.0,  "gamma_power": 0.0, "std_amplitude": 0.0},
    "reject":  {"alpha_power": 0.0, "beta_power": 0.1,  "gamma_power": 0.0, "std_amplitude": 0.7},
    "neutral": {"alpha_power": 0.1, "beta_power": 0.05, "gamma_power": 0.0, "std_amplitude": 0.0},
}


def generate_dataset(n_samples: int = DEFAULT_N,
                     save_path: str = OUTPUT_PATH,
                     seed: int = 42) -> pd.DataFrame:
    """
    Generate a balanced mock EEG dataset with realistic inter-class variation.

    Args:
        n_samples: Total number of samples (evenly split across 4 labels).
        save_path: Output CSV path.
        seed:      Random seed for reproducibility.

    Returns:
        DataFrame with feature columns + label.
    """
    np.random.seed(seed)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    bci  = BCIConnection("MOCK_GEN", mode="mock")
    prep = EEGPreprocessor()
    bci.connect()

    rows = []
    labels_cycle = LABELS * (n_samples // len(LABELS)) + LABELS[:n_samples % len(LABELS)]

    print(f"[DataGen] Generating {n_samples} samples across {len(LABELS)} labels...")

    for i, label in enumerate(labels_cycle):
        chunk    = bci._generate_mock_chunk()
        features = prep.process(chunk)
        mods     = LABEL_MODIFIERS[label]

        row = {
            "delta_power":    features.delta_power,
            "theta_power":    features.theta_power,
            "alpha_power":    max(0.0, features.alpha_power    + mods.get("alpha_power", 0)),
            "beta_power":     max(0.0, features.beta_power     + mods.get("beta_power", 0)),
            "gamma_power":    max(0.0, features.gamma_power    + mods.get("gamma_power", 0)),
            "mean_amplitude": features.mean_amplitude,
            "std_amplitude":  max(0.0, features.std_amplitude  + mods.get("std_amplitude", 0)),
            "label":          label,
        }
        rows.append(row)

        if (i + 1) % 100 == 0:
            print(f"  [{i+1}/{n_samples}] Generated...")

    bci.disconnect()
    df = pd.DataFrame(rows)
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)  # shuffle

    df.to_csv(save_path, index=False)
    print(f"\n[DataGen] ✅ Saved {len(df)} samples → {save_path}")
    return df


def print_stats(df: pd.DataFrame):
    """Print dataset statistics."""
    print("\n── Label Distribution ─────────────────────────────")
    print(df["label"].value_counts().to_string())

    print("\n── Feature Statistics ─────────────────────────────")
    feature_cols = ["alpha_power", "beta_power", "gamma_power",
                    "delta_power", "theta_power", "std_amplitude"]
    print(df[feature_cols].describe().round(4).to_string())

    print("\n── Per-Label Alpha/Beta Means ─────────────────────")
    print(df.groupby("label")[["alpha_power", "beta_power", "gamma_power"]].mean().round(4).to_string())


def verify_separability(df: pd.DataFrame) -> float:
    """
    Quick sanity check: train a simple classifier and verify
    the dataset has enough class separability for ≥ 80% accuracy.
    """
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import cross_val_score
    from sklearn.preprocessing import LabelEncoder

    feature_cols = ["delta_power", "theta_power", "alpha_power",
                    "beta_power", "gamma_power", "mean_amplitude", "std_amplitude"]
    X = df[feature_cols].values
    y = LabelEncoder().fit_transform(df["label"].values)

    clf    = RandomForestClassifier(n_estimators=50, random_state=42)
    scores = cross_val_score(clf, X, y, cv=5, scoring="accuracy")
    mean   = scores.mean()

    status = "✅" if mean >= 0.80 else "⚠️"
    print(f"\n── Separability Check (5-fold CV) ─────────────────")
    print(f"   CV Accuracy: {mean:.4f} ± {scores.std():.4f}  {status}")
    if mean < 0.80:
        print("   ⚠️  Below 80% target — consider increasing n_samples or adjusting modifiers")
    return mean


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Brain-Net Mock EEG Dataset Generator"
    )
    parser.add_argument(
        "--n", type=int, default=DEFAULT_N,
        help=f"Number of samples to generate (default: {DEFAULT_N})"
    )
    parser.add_argument(
        "--output", type=str, default=OUTPUT_PATH,
        help=f"Output CSV path (default: {OUTPUT_PATH})"
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed (default: 42)"
    )
    parser.add_argument(
        "--verify", action="store_true",
        help="Run separability check after generation"
    )
    args = parser.parse_args()

    print("╔═══════════════════════════════════════╗")
    print("║   Brain-Net Mock Dataset Generator    ║")
    print("╚═══════════════════════════════════════╝")
    print(f"  Samples : {args.n}")
    print(f"  Output  : {args.output}")
    print(f"  Seed    : {args.seed}")
    print()

    df = generate_dataset(n_samples=args.n, save_path=args.output, seed=args.seed)
    print_stats(df)

    if args.verify:
        verify_separability(df)

    print("\n[DataGen] Done. Run neural_classifier.py to train the model.")


if __name__ == "__main__":
    main()
