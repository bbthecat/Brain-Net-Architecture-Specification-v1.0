"""
brain_net_pipeline.py — Full Brain-Net E2E Pipeline Orchestrator
Sprint 4 (MVP) | Owner: เจม (Network Architect)

Orchestrates: DomainInterface → DAFTValidator → MLClassifier →
              TTPRouter → EthicsRuleEngine → BrainFirewall →
              HITLCheckpoint → MockQKD → VirtualNetwork
"""

import time
import numpy as np
from dataclasses import dataclass
from typing import Optional

from src.bci.neural_classifier import NeuralClassifier, FEATURE_COLS
from src.protocol.ttp_packet import TTPHeader, TTPPacket
from src.protocol.ttp_router import TTPRouter
from src.protocol.virtual_network import VirtualNetwork
from src.security.brain_firewall import BrainFirewall
from src.security.consensual_handshake import ConsensualHandshake
from src.security.ethics_rule_engine import EthicsRuleEngine, EthicsDecision
from src.security.hitl_checkpoint import HITLCheckpoint
from src.crypto.mock_qkd_aes import MockQKD
from src.daft.domain_interface import DomainInterface, Domain
from src.daft.daft_validator import DAFTValidator
from src.metrics.quality_metrics import QualityMetrics


@dataclass
class PipelineResult:
    success:        bool
    symbol:         str
    latency_ms:     float
    stage_times:    dict
    ethics_decision: str
    hitl_triggered: bool
    error:          Optional[str] = None


class BrainNetPipeline:
    """
    Full Brain-Net MVP Pipeline.

    Pipeline stages:
      1. Domain Interface Mapping   (DAFT Layer)
      2. DAFT Validation
      3. ML Classification
      4. TTP Packet Assembly
      5. Ethics Rule Engine
      6. Brain Firewall
      7. HITL Checkpoint
      8. Mock QKD Encryption
      9. Virtual Network Transmission
    """

    def __init__(self, model_path: str = "models/neural_dict_v1.pkl",
                 source_id: str = "NODE_A", dest_id: str = "NODE_B"):
        self.source_id = source_id
        self.dest_id   = dest_id

        # Components
        self._domain_if  = DomainInterface()
        self._validator  = DAFTValidator()
        self._classifier = NeuralClassifier.load(model_path) if _model_exists(model_path) else None
        self._firewall   = BrainFirewall()
        self._handshake  = ConsensualHandshake()
        self._ethics     = EthicsRuleEngine()
        self._hitl       = HITLCheckpoint()
        self._qkd        = MockQKD(reuse_key=True)
        self._network    = VirtualNetwork(base_latency_ms=5, jitter_ms=2)
        self._metrics    = QualityMetrics()
        self._router     = TTPRouter(source_id)

        self._network.setup(firewall=self._firewall, handshake=self._handshake)

    # ── Public API ───────────────────────────────────────────────────────────

    def open_session(self, arousal: float = 0.3, valence: float = 0.2,
                     consent: float = 0.85) -> bool:
        """Establish consensual session before transmitting."""
        result = self._handshake.request_session(
            self.source_id, self.dest_id,
            arousal=arousal, valence=valence, consent_score=consent
        )
        self._metrics.record_session()
        return result.allowed

    def transmit(self, domain: Domain, raw_input,
                 consent_score: float = 0.85,
                 arousal: float = 0.3,
                 valence: float = 0.2) -> PipelineResult:
        """
        Run full pipeline for one transmission.
        Returns PipelineResult with latency breakdown.
        """
        t_start = time.perf_counter()
        stage_times = {}

        # ── Stage 1: Domain Interface Mapping ───────────────────────────────
        t0 = time.perf_counter()
        try:
            math_symbol = self._domain_if.map(domain, raw_input, consent_score)
        except Exception as e:
            return PipelineResult(False, "error", 0, {}, "ERROR", False, str(e))
        stage_times["domain_map_ms"] = (time.perf_counter() - t0) * 1000

        # ── Stage 2: DAFT Validation ─────────────────────────────────────────
        t0 = time.perf_counter()
        val_result = self._validator.validate(math_symbol)
        stage_times["daft_validate_ms"] = (time.perf_counter() - t0) * 1000
        self._metrics.record_daft_result(val_result.status == "PASS")

        if val_result.status != "PASS":
            return PipelineResult(False, "blocked", _elapsed(t_start),
                                  stage_times, "DAFT_FAIL", False, val_result.message)

        # ── Stage 3: ML Classification ───────────────────────────────────────
        t0 = time.perf_counter()
        symbol = math_symbol.symbol_name
        if self._classifier:
            feat = _symbol_to_features(math_symbol)
            clf_result = self._classifier.predict(feat)
            symbol = clf_result.symbol
        stage_times["ml_inference_ms"] = (time.perf_counter() - t0) * 1000

        # ── Stage 4: TTP Packet Assembly ─────────────────────────────────────
        t0 = time.perf_counter()
        header = TTPHeader(source_id=self.source_id, dest_id=self.dest_id,
                           symbol_id=_name_to_id(symbol))
        packet = TTPPacket(
            header=header, symbol=symbol,
            valence=valence, arousal=arousal,
            intensity=float(math_symbol.confidence),
            consent_score=consent_score,
            domain=domain.value,
        )
        stage_times["ttp_assembly_ms"] = (time.perf_counter() - t0) * 1000

        # ── Stage 5: Ethics Rule Engine ──────────────────────────────────────
        t0 = time.perf_counter()
        eth_result = self._ethics.evaluate(packet)
        stage_times["ethics_ms"] = (time.perf_counter() - t0) * 1000
        self._metrics.record_ethics_result(eth_result.decision == EthicsDecision.ALLOW)

        if eth_result.decision == EthicsDecision.BLOCK:
            return PipelineResult(False, symbol, _elapsed(t_start),
                                  stage_times, eth_result.decision.value, False)

        # ── Stage 6: Brain Firewall ──────────────────────────────────────────
        t0 = time.perf_counter()
        fw_result = self._firewall.evaluate(packet)
        stage_times["firewall_ms"] = (time.perf_counter() - t0) * 1000

        if not fw_result.allow:
            self._hitl.record_blocked(f"{self.source_id}→{self.dest_id}")
            return PipelineResult(False, symbol, _elapsed(t_start),
                                  stage_times, "FIREWALL_BLOCK", False, fw_result.reason)

        # ── Stage 7: HITL Checkpoint ─────────────────────────────────────────
        t0 = time.perf_counter()
        hitl_event = self._hitl.check(packet)
        stage_times["hitl_ms"] = (time.perf_counter() - t0) * 1000
        hitl_triggered = hitl_event is not None

        if hitl_triggered:
            self._metrics.record_hitl_event()
            return PipelineResult(False, symbol, _elapsed(t_start),
                                  stage_times, "HITL_STOP", True)

        # ── Stage 8: QKD Encryption ──────────────────────────────────────────
        t0 = time.perf_counter()
        raw_bytes    = packet.pack()
        enc_bytes    = self._qkd.encrypt_packet(raw_bytes)
        stage_times["qkd_enc_ms"] = (time.perf_counter() - t0) * 1000

        # ── Stage 9: Network Transmission ────────────────────────────────────
        t0 = time.perf_counter()
        # Decrypt at receiver side
        dec_bytes    = self._qkd.decrypt_packet(enc_bytes)
        recv_packet  = TTPPacket.unpack(dec_bytes)
        net_log      = self._network.transmit(recv_packet)
        stage_times["network_ms"] = (time.perf_counter() - t0) * 1000

        total_ms = _elapsed(t_start)
        self._metrics.record_latency(total_ms)

        return PipelineResult(
            success=not net_log.dropped,
            symbol=symbol,
            latency_ms=total_ms,
            stage_times=stage_times,
            ethics_decision=eth_result.decision.value,
            hitl_triggered=False,
        )

    def benchmark(self, n: int = 100) -> dict:
        """Run n transmissions and return quality stats."""
        import random
        domains = [Domain.NEURO, Domain.BIO, Domain.PHY, Domain.QUANTUM]
        latencies, successes = [], []

        self.open_session(consent=0.9)

        for _ in range(n):
            domain = random.choice(domains)
            raw    = _sample_input(domain)
            result = self.transmit(domain, raw, consent_score=0.85,
                                   arousal=0.3, valence=0.2)
            latencies.append(result.latency_ms)
            successes.append(result.success)

        latencies.sort()
        return {
            "n":              n,
            "success_rate":   sum(successes) / n,
            "p50_ms":  latencies[int(n * 0.50)],
            "p95_ms":  latencies[int(n * 0.95)],
            "p99_ms":  latencies[int(n * 0.99)],
            "meets_50ms_target": latencies[int(n * 0.95)] < 50,
            "quality_report": self._metrics.generate_report(),
        }

    @property
    def metrics(self) -> QualityMetrics:
        return self._metrics


# ── Helpers ──────────────────────────────────────────────────────────────────

def _elapsed(t_start: float) -> float:
    return (time.perf_counter() - t_start) * 1000

def _name_to_id(name: str) -> int:
    return {"focus": 0, "relax": 1, "reject": 2, "neutral": 3}.get(name, 3)

def _model_exists(path: str) -> bool:
    import os
    return os.path.exists(path)

def _symbol_to_features(sym) -> np.ndarray:
    """Convert MathSymbol vector to ML feature vector."""
    v = sym.vector
    if len(v) >= 7:
        return v[:7].astype(float)
    padded = np.zeros(7)
    padded[:len(v)] = v
    return padded

def _sample_input(domain: Domain):
    """Generate sample input for each domain."""
    if domain == Domain.BIO:
        return np.random.rand(64)
    elif domain == Domain.PHY:
        return np.random.rand(14, 32)
    elif domain == Domain.NEURO:
        return np.random.choice(["focus", "relax", "reject", "neutral"])
    elif domain == Domain.QUANTUM:
        raw = np.random.randn(8) + 1j * np.random.randn(8)
        return raw / np.linalg.norm(raw)


if __name__ == "__main__":
    print("=== Brain-Net MVP Pipeline ===")
    pipeline = BrainNetPipeline()

    print("\n[1] Opening session...")
    ok = pipeline.open_session(consent=0.9)
    print(f"    Session: {'ACTIVE' if ok else 'REJECTED'}")

    print("\n[2] Single transmission (Neuro domain)...")
    result = pipeline.transmit(Domain.NEURO, "focus", consent_score=0.9)
    print(f"    Symbol: {result.symbol}  Latency: {result.latency_ms:.1f}ms  "
          f"Success: {result.success}")
    print(f"    Stages: {result.stage_times}")

    print("\n[3] Running 50-packet benchmark...")
    stats = pipeline.benchmark(n=50)
    print(f"    P95: {stats['p95_ms']:.1f}ms | "
          f"Success: {stats['success_rate']*100:.0f}% | "
          f"PMI: {stats['quality_report']['pmi']['overall']}")
    print(f"    Meets 50ms target: {'✅' if stats['meets_50ms_target'] else '⚠️'}")
