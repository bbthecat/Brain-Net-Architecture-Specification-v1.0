"""
domain_interface.py — Domain Interface Mapping (DAFT Layer)
Sprint 3 | Owner: เจม + บี

Maps inputs from 4 domains (Bio/Phy/Neuro/Quantum) to universal MathSymbol.
Mapping must complete in < 5ms per input.
"""

import time
import numpy as np
from dataclasses import dataclass
from enum import Enum
from typing import Any


class Domain(Enum):
    BIO     = "bio"
    PHY     = "phy"
    NEURO   = "neuro"
    QUANTUM = "quantum"


@dataclass
class MathSymbol:
    """
    Universal mathematical representation of a neural/physical signal.

    Bio:     f ∈ ℝⁿ  (neural firing rate frequency vector)
    Phy:     T ∈ [0,1]^{d×t}  (normalized EEG amplitude tensor)
    Neuro:   s ∈ S = {focus, relax, reject, neutral}
    Quantum: |ψ⟩ ∈ ℂ²ⁿ (entanglement state vector)
    """
    domain:       Domain
    symbol_id:    int
    symbol_name:  str
    vector:       np.ndarray     # Unified float vector representation
    consent_score: float = 0.8
    confidence:   float = 1.0

    def is_valid(self) -> bool:
        return (0 <= self.consent_score <= 1.0
                and 0 <= self.confidence <= 1.0
                and len(self.vector) > 0
                and not np.any(np.isnan(self.vector)))


# ── Mappers ──────────────────────────────────────────────────────────────────

class DomainInterface:
    """
    Maps domain-specific inputs to unified MathSymbol representation.
    """

    SYMBOL_MAP = {"focus": 0, "relax": 1, "reject": 2, "neutral": 3}

    def map(self, domain: Domain, raw_input: Any,
            consent_score: float = 0.8) -> MathSymbol:
        """Map raw input from given domain to MathSymbol. Must complete < 5ms."""
        t0 = time.perf_counter()

        if domain == Domain.BIO:
            result = self._map_bio(raw_input, consent_score)
        elif domain == Domain.PHY:
            result = self._map_phy(raw_input, consent_score)
        elif domain == Domain.NEURO:
            result = self._map_neuro(raw_input, consent_score)
        elif domain == Domain.QUANTUM:
            result = self._map_quantum(raw_input, consent_score)
        else:
            raise ValueError(f"Unknown domain: {domain}")

        elapsed_ms = (time.perf_counter() - t0) * 1000
        assert elapsed_ms < 5.0, f"Mapping too slow: {elapsed_ms:.2f}ms (limit 5ms)"
        return result

    # ── Bio Domain: Neural Firing Rate → Frequency Vector f ∈ ℝⁿ ─────────

    def _map_bio(self, firing_rates: np.ndarray, consent: float) -> MathSymbol:
        """
        Bio mapping: normalize firing rate array to frequency vector.
        f ∈ ℝⁿ where n = number of neurons sampled.
        """
        if not isinstance(firing_rates, np.ndarray):
            firing_rates = np.array(firing_rates, dtype=float)
        norm = firing_rates / (firing_rates.max() + 1e-8)
        sym_id = int(np.argmax(norm[:4])) if len(norm) >= 4 else 3
        names  = ["focus", "relax", "reject", "neutral"]
        return MathSymbol(domain=Domain.BIO, symbol_id=sym_id,
                          symbol_name=names[sym_id], vector=norm,
                          consent_score=consent, confidence=float(norm.max()))

    # ── Physical Domain: EEG Amplitude → Normalized Tensor T ∈ [0,1]^{d×t} ─

    def _map_phy(self, eeg_matrix: np.ndarray, consent: float) -> MathSymbol:
        """
        Physical mapping: normalize EEG amplitude matrix channel × time.
        T ∈ [0,1]^{d×t}
        """
        if not isinstance(eeg_matrix, np.ndarray):
            eeg_matrix = np.array(eeg_matrix, dtype=float)
        mn, mx = eeg_matrix.min(), eeg_matrix.max()
        T = (eeg_matrix - mn) / (mx - mn + 1e-8)
        # Derive symbol from average alpha-band power (channels 7-12 Hz proxy)
        mean_power = float(T.mean())
        sym_id  = 0 if mean_power > 0.6 else (1 if mean_power > 0.4 else 3)
        names   = ["focus", "relax", "reject", "neutral"]
        vector  = T.flatten()[:32]   # compact to 32 elements
        return MathSymbol(domain=Domain.PHY, symbol_id=sym_id,
                          symbol_name=names[sym_id], vector=vector,
                          consent_score=consent, confidence=mean_power)

    # ── Neuro Domain: Cognitive State → Discrete Symbol s ∈ S ────────────

    def _map_neuro(self, state: str, consent: float) -> MathSymbol:
        """
        Neuro mapping: cognitive state string to one-hot vector.
        s ∈ S = {focus, relax, reject, neutral}
        """
        names  = ["focus", "relax", "reject", "neutral"]
        sym_id = self.SYMBOL_MAP.get(str(state).lower(), 3)
        one_hot = np.zeros(4)
        one_hot[sym_id] = 1.0
        return MathSymbol(domain=Domain.NEURO, symbol_id=sym_id,
                          symbol_name=names[sym_id], vector=one_hot,
                          consent_score=consent, confidence=1.0)

    # ── Quantum Domain: Entanglement State → |ψ⟩ ∈ ℂ²ⁿ ─────────────────

    def _map_quantum(self, state_vector: Any, consent: float) -> MathSymbol:
        """
        Quantum mapping: complex state vector to real representation.
        |ψ⟩ ∈ ℂ²ⁿ → real amplitudes via |amplitude|²
        """
        if not isinstance(state_vector, np.ndarray):
            state_vector = np.array(state_vector, dtype=complex)
        probabilities = np.abs(state_vector) ** 2
        probabilities /= (probabilities.sum() + 1e-8)  # normalize
        sym_id = int(np.argmax(probabilities)) % 4
        names  = ["focus", "relax", "reject", "neutral"]
        return MathSymbol(domain=Domain.QUANTUM, symbol_id=sym_id,
                          symbol_name=names[sym_id], vector=probabilities.real,
                          consent_score=consent, confidence=float(probabilities.max()))
