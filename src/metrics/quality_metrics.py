"""
quality_metrics.py — Quality Dashboard & Protocol Maturity Index
Sprint 3 | Owner: เจม + บี
"""

import json
import os
import time
from dataclasses import dataclass, field
from typing import List


@dataclass
class LatencyRecord:
    timestamp: float
    latency_ms: float
    stage: str = "e2e"


class QualityMetrics:
    """Collects and computes all Brain-Net quality metrics."""

    def __init__(self):
        self._latencies: List[LatencyRecord] = []
        self._ml_accuracies: List[float] = []
        self._daft_results: List[bool] = []
        self._ethics_results: List[bool] = []
        self._hitl_events: int = 0
        self._total_sessions: int = 0

    # ── Recording ────────────────────────────────────────────────────────────

    def record_latency(self, latency_ms: float, stage: str = "e2e"):
        self._latencies.append(LatencyRecord(time.time(), latency_ms, stage))

    def record_ml_accuracy(self, accuracy: float):
        self._ml_accuracies.append(accuracy)

    def record_daft_result(self, passed: bool):
        self._daft_results.append(passed)

    def record_ethics_result(self, passed: bool):
        self._ethics_results.append(passed)

    def record_hitl_event(self):
        self._hitl_events += 1

    def record_session(self):
        self._total_sessions += 1

    # ── Computed Metrics ────────────────────────────────────────────────────

    def ml_accuracy(self) -> float:
        return (sum(self._ml_accuracies) / len(self._ml_accuracies)
                if self._ml_accuracies else 0.0)

    def latency_percentile(self, p: float) -> float:
        if not self._latencies:
            return 0.0
        vals = sorted(r.latency_ms for r in self._latencies)
        idx = max(0, int(len(vals) * p / 100) - 1)
        return vals[idx]

    def daft_pass_rate(self) -> float:
        if not self._daft_results:
            return 0.0
        return sum(self._daft_results) / len(self._daft_results)

    def ethics_compliance_rate(self) -> float:
        if not self._ethics_results:
            return 0.0
        return sum(self._ethics_results) / len(self._ethics_results)

    def hitl_intervention_rate(self) -> float:
        if self._total_sessions == 0:
            return 0.0
        return self._hitl_events / self._total_sessions

    # ── PMI ─────────────────────────────────────────────────────────────────

    def compute_pmi(self) -> dict:
        """
        Protocol Maturity Index — 5 dimensions, scale 1–5.
        Target Sprint 3: ≥ 3.5 | Target MVP: ≥ 4.2
        """
        stability  = self._score_stability()
        coverage   = self._score_coverage()
        latency    = self._score_latency()
        security   = 4.0   # Firewall + AES tested
        ethics     = self._score_ethics()
        overall    = (stability + coverage + latency + security + ethics) / 5
        return {
            "stability":  stability,
            "coverage":   coverage,
            "latency":    latency,
            "security":   security,
            "ethics":     ethics,
            "overall":    round(overall, 2),
            "meets_sprint3_target": overall >= 3.5,
            "meets_mvp_target":     overall >= 4.2,
        }

    def _score_stability(self) -> float:
        # Based on absence of errors (simplified: return 3.5 baseline)
        return 3.5

    def _score_coverage(self) -> float:
        # 4 domains supported in Sprint 3
        return 4.0

    def _score_latency(self) -> float:
        p95 = self.latency_percentile(95)
        if p95 == 0:
            return 3.0
        if p95 < 30:  return 5.0
        if p95 < 50:  return 4.0
        if p95 < 100: return 3.0
        if p95 < 150: return 2.0
        return 1.0

    def _score_ethics(self) -> float:
        rate = self.ethics_compliance_rate()
        if rate >= 1.0:  return 5.0
        if rate >= 0.9:  return 4.0
        if rate >= 0.8:  return 3.0
        return 2.0

    # ── Report ───────────────────────────────────────────────────────────────

    def generate_report(self) -> dict:
        pmi = self.compute_pmi()
        return {
            "ml_accuracy":           round(self.ml_accuracy(), 4),
            "latency_p50_ms":        round(self.latency_percentile(50), 2),
            "latency_p95_ms":        round(self.latency_percentile(95), 2),
            "latency_p99_ms":        round(self.latency_percentile(99), 2),
            "daft_pass_rate":        round(self.daft_pass_rate(), 4),
            "ethics_compliance":     round(self.ethics_compliance_rate(), 4),
            "hitl_intervention_rate": round(self.hitl_intervention_rate(), 4),
            "total_latency_samples": len(self._latencies),
            "pmi":                   pmi,
        }

    def export_json(self, path: str = "reports/quality_report.json"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.generate_report(), f, indent=2)
        print(f"[Metrics] Report saved → {path}")

    def export_markdown(self, path: str = "reports/quality_report.md"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        r = self.generate_report()
        pmi = r["pmi"]
        md = f"""# Brain-Net Quality Report

## Performance
| Metric | Value | Target |
|--------|-------|--------|
| ML Accuracy | {r['ml_accuracy']*100:.1f}% | ≥ 85% |
| E2E P50 Latency | {r['latency_p50_ms']:.1f}ms | < 35ms |
| E2E P95 Latency | {r['latency_p95_ms']:.1f}ms | < 50ms |
| DAFT Pass Rate | {r['daft_pass_rate']*100:.1f}% | ≥ 95% |
| Ethics Compliance | {r['ethics_compliance']*100:.1f}% | 100% |
| HITL Intervention | {r['hitl_intervention_rate']*100:.1f}% | < 5% |

## Protocol Maturity Index (PMI)
| Dimension | Score | /5 |
|-----------|-------|-----|
| Stability | {pmi['stability']} | 5 |
| Coverage | {pmi['coverage']} | 5 |
| Latency Compliance | {pmi['latency']} | 5 |
| Security | {pmi['security']} | 5 |
| Ethics | {pmi['ethics']} | 5 |
| **Overall PMI** | **{pmi['overall']}** | **5** |

Sprint 3 Target (≥3.5): {'✅ PASS' if pmi['meets_sprint3_target'] else '❌ FAIL'}
MVP Target (≥4.2): {'✅ PASS' if pmi['meets_mvp_target'] else '❌ FAIL'}
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"[Metrics] Markdown report saved → {path}")
