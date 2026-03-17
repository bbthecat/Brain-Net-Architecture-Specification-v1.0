"""
tests/unit/test_quality_metrics.py — Unit Tests: QualityMetrics + PMI
Sprint 3 | Owner: เจม + บี

Tests: latency percentiles, pass rates, PMI scoring, report generation
"""

import json
import os
import tempfile
import pytest
from src.metrics.quality_metrics import QualityMetrics


class TestQualityMetrics:

    def setup_method(self):
        self.qm = QualityMetrics()

    # ── Recording ────────────────────────────────────────────────────────────

    def test_record_latency(self):
        self.qm.record_latency(25.0)
        assert self.qm.latency_percentile(50) == 25.0

    def test_record_multiple_latencies(self):
        for ms in [10, 20, 30, 40, 50]:
            self.qm.record_latency(ms)
        assert self.qm.latency_percentile(50) > 0

    def test_latency_percentile_empty(self):
        assert self.qm.latency_percentile(95) == 0.0

    def test_p95_above_p50(self):
        for ms in [10, 15, 20, 25, 30, 35, 40, 45, 50, 200]:
            self.qm.record_latency(ms)
        assert self.qm.latency_percentile(95) >= self.qm.latency_percentile(50)

    # ── DAFT Pass Rate ───────────────────────────────────────────────────────

    def test_daft_pass_rate_all_pass(self):
        for _ in range(10):
            self.qm.record_daft_result(True)
        assert self.qm.daft_pass_rate() == 1.0

    def test_daft_pass_rate_mixed(self):
        for _ in range(95):
            self.qm.record_daft_result(True)
        for _ in range(5):
            self.qm.record_daft_result(False)
        assert abs(self.qm.daft_pass_rate() - 0.95) < 0.01

    def test_daft_pass_rate_empty(self):
        assert self.qm.daft_pass_rate() == 0.0

    # ── Ethics Compliance ────────────────────────────────────────────────────

    def test_ethics_compliance_all_pass(self):
        for _ in range(20):
            self.qm.record_ethics_result(True)
        assert self.qm.ethics_compliance_rate() == 1.0

    # ── HITL Intervention Rate ───────────────────────────────────────────────

    def test_hitl_rate_zero_without_events(self):
        self.qm.record_session()
        self.qm.record_session()
        assert self.qm.hitl_intervention_rate() == 0.0

    def test_hitl_rate_calculated_correctly(self):
        for _ in range(10):
            self.qm.record_session()
        for _ in range(1):
            self.qm.record_hitl_event()
        assert abs(self.qm.hitl_intervention_rate() - 0.1) < 0.01

    # ── PMI ──────────────────────────────────────────────────────────────────

    def test_pmi_structure(self):
        pmi = self.qm.compute_pmi()
        for key in ["stability", "coverage", "latency", "security",
                    "ethics", "overall", "meets_sprint3_target", "meets_mvp_target"]:
            assert key in pmi

    def test_pmi_overall_in_range(self):
        pmi = self.qm.compute_pmi()
        assert 1.0 <= pmi["overall"] <= 5.0

    def test_pmi_meets_sprint3_with_good_latency(self):
        """Feed latencies under 50ms → latency score = 4.0 → PMI should meet Sprint 3."""
        for _ in range(20):
            self.qm.record_latency(30.0)
        for _ in range(20):
            self.qm.record_ethics_result(True)
        pmi = self.qm.compute_pmi()
        assert pmi["meets_sprint3_target"] is True

    def test_latency_score_5_under_30ms(self):
        """P95 < 30ms → latency score = 5.0."""
        for _ in range(100):
            self.qm.record_latency(25.0)
        pmi = self.qm.compute_pmi()
        assert pmi["latency"] == 5.0

    def test_latency_score_1_over_150ms(self):
        for _ in range(100):
            self.qm.record_latency(200.0)
        pmi = self.qm.compute_pmi()
        assert pmi["latency"] == 1.0

    # ── Report Generation ────────────────────────────────────────────────────

    def test_generate_report_keys(self):
        report = self.qm.generate_report()
        expected = [
            "ml_accuracy", "latency_p50_ms", "latency_p95_ms", "latency_p99_ms",
            "daft_pass_rate", "ethics_compliance", "hitl_intervention_rate",
            "total_latency_samples", "pmi",
        ]
        for key in expected:
            assert key in report

    def test_export_json(self):
        for ms in [20, 30, 40]:
            self.qm.record_latency(ms)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "reports", "test_report.json")
            self.qm.export_json(path)
            assert os.path.exists(path)
            with open(path) as f:
                data = json.load(f)
            assert "pmi" in data

    def test_export_markdown(self):
        for ms in [20, 30, 40]:
            self.qm.record_latency(ms)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "reports", "test_report.md")
            self.qm.export_markdown(path)
            assert os.path.exists(path)
            content = open(path).read()
            assert "PMI" in content
            assert "Latency" in content
