# 📊 Quality Metrics & Protocol Maturity Index (PMI)
**Brain-Net Phase 1 — Quality Standards Document**

---

## 1. Quality Metrics Overview

### 1.1 Core Performance Metrics

| Metric | Definition | Unit | Sprint 1 | Sprint 2 | Sprint 3 Target | Sprint 4 (MVP) Target |
|--------|-----------|------|----------|----------|-----------------|----------------------|
| **ML Accuracy** | Holdout Test Set Accuracy of Neural Dict Classifier | % | 78% | 78% | ≥ 85% | ≥ 85% |
| **E2E P50 Latency** | 50th percentile End-to-End transmission time | ms | ~60ms | ~70ms | < 40ms | < 35ms |
| **E2E P95 Latency** | 95th percentile End-to-End transmission time | ms | ~85ms | ~90ms | < 55ms | < 50ms |
| **E2E P99 Latency** | 99th percentile End-to-End transmission time | ms | ~110ms | ~115ms | < 75ms | < 75ms |
| **Encryption Overhead** | Time added by AES-256 Mock QKD | ms | N/A | 18ms | < 15ms | < 15ms |
| **DAFT Validation Time** | Time for Domain→MathSymbol mapping + validation | ms | N/A | N/A | < 5ms | < 5ms |

### 1.2 Quality Metrics

| Metric | Definition | Unit | Target (Sprint 3) | Target (MVP) |
|--------|-----------|------|------------------|--------------|
| **Test Coverage** | pytest line coverage | % | ≥ 80% | ≥ 80% |
| **DAFT Pass Rate** | % of packets passing DAFTValidator | % | ≥ 95% | ≥ 95% |
| **Firewall Block Accuracy** | % of correctly blocked malicious packets | % | ≥ 99% | ≥ 99% |
| **Semantic Injection Detection** | Rate of detected injection attempts | % | ≥ 95% | ≥ 99% |
| **Critical Bug Count** | Open Critical severity bugs | Count | 0 | 0 |
| **High Bug Count** | Open High severity bugs | Count | ≤ 2 | 0 |

### 1.3 Ethics & HITL Metrics

| Metric | Definition | Unit | Target (Sprint 3) | Target (MVP) |
|--------|-----------|------|------------------|--------------|
| **Ethics Compliance Rate** | % of Ethics Rules passing automated check | % | ≥ 80% | 100% |
| **Private Payload Leak Rate** | Instances of Neural Payload found in Logs | Count | 0 | 0 |
| **HITL Intervention Rate** | % of Sessions triggering HITL Hard Stop | % | < 10% | < 5% |
| **HITL Detection Recall** | % of true anomalies correctly detected | % | ≥ 90% | ≥ 95% |
| **HITL False Positive Rate** | % of normal sessions incorrectly flagged | % | < 10% | < 5% |
| **HITL Response Time** | Time from Trigger to Hard Stop | ms | < 1000ms | < 500ms |

---

## 2. Protocol Maturity Index (PMI)

### 2.1 PMI Definition

**PMI (Protocol Maturity Index)** คือตัวชี้วัดความสมบูรณ์ของ Brain-Net Protocol โดยรวม ประเมินใน 5 มิติ Scale 1–5 (1 = ต้องปรับปรุง, 5 = Excellent)

### 2.2 PMI Dimensions & Scoring Criteria

#### Dimension 1: Stability (ความเสถียร)
| Score | Criteria |
|-------|---------|
| 1 | System crashes > 5 times per 100 sessions |
| 2 | System crashes 2–5 times per 100 sessions |
| 3 | System crashes < 2 times per 100 sessions |
| 4 | No crashes; occasional recoverable errors |
| 5 | Zero errors; automatic recovery from all edge cases |

#### Dimension 2: Coverage (ความครอบคลุม)
| Score | Criteria |
|-------|---------|
| 1 | Supports 1 domain only |
| 2 | Supports 2 domains |
| 3 | Supports 3 domains with DAFT validation |
| 4 | Supports all 4 domains (Bio/Phy/Neuro/Quantum) with full validation |
| 5 | Supports 4+ domains with round-trip consistency ≥ 0.98 |

#### Dimension 3: Latency Compliance (ตรงตามเป้า Latency)
| Score | Criteria |
|-------|---------|
| 1 | P95 Latency > 150ms |
| 2 | P95 Latency 100–150ms |
| 3 | P95 Latency 50–100ms |
| 4 | P95 Latency < 50ms |
| 5 | P95 Latency < 30ms with encryption overhead < 10ms |

#### Dimension 4: Security Integrity (ความปลอดภัย)
| Score | Criteria |
|-------|---------|
| 1 | No Firewall; no encryption |
| 2 | Basic Firewall; no encryption |
| 3 | Firewall + Encryption; no penetration testing |
| 4 | Firewall + Encryption; penetration tested; 0 Critical vulnerabilities |
| 5 | Full Zero-Trust; all attack vectors tested; automated threat detection |

#### Dimension 5: Ethics Compliance (จริยธรรม)
| Score | Criteria |
|-------|---------|
| 1 | No Ethics Rules |
| 2 | Basic Ethics Rules (manual audit only) |
| 3 | Automated Ethics Engine; partial compliance |
| 4 | Full Automated Ethics Engine; ≥ 80% compliance; HITL present |
| 5 | 100% Compliance; Ethics Certified; HITL validated; Immutable Audit Log |

### 2.3 PMI Formula

```
PMI = (Stability + Coverage + Latency + Security + Ethics) / 5
```

### 2.4 PMI Sprint History

| Sprint | Stability | Coverage | Latency | Security | Ethics | **PMI** |
|--------|-----------|----------|---------|----------|--------|---------|
| Sprint 1 | 2.5 | 1.0 | 1.5 | 2.0 | 1.5 | **1.7** |
| Sprint 2 | 3.0 | 1.5 | 2.0 | 3.0 | 2.0 | **2.3** |
| Sprint 3 Target | 3.5 | 3.5 | 3.5 | 4.0 | 4.0 | **≥ 3.7** |
| Sprint 4 (MVP) Target | 4.0 | 4.0 | 4.0 | 4.0 | 5.0 | **≥ 4.2** |

---

## 3. Quality Gate Thresholds

### Sprint 3 Quality Gate (ต้องผ่านก่อน Sprint 4)
```
[ ] ML Accuracy ≥ 85%
[ ] DAFT Pass Rate ≥ 95%
[ ] E2E P95 Latency < 55ms
[ ] PMI ≥ 3.5
[ ] Test Coverage ≥ 80%
[ ] Critical Bugs = 0
[ ] Ethics Compliance ≥ 80%
[ ] HITL Detection Recall ≥ 90%
```

### MVP Quality Gate (ต้องผ่านก่อน Delivery)
```
[ ] ML Accuracy ≥ 85%
[ ] DAFT Pass Rate ≥ 95%
[ ] E2E P95 Latency < 50ms
[ ] Mock QKD Overhead < 15ms
[ ] PMI ≥ 3.5
[ ] Test Coverage ≥ 80%
[ ] Critical Bugs = 0
[ ] High Bugs = 0
[ ] Security Audit: PASSED
[ ] Ethics Compliance: 100%
[ ] Ethics Certificate: SIGNED
[ ] Data Governance: ENACTED
[ ] HITL Detection Recall ≥ 95%
[ ] HITL False Positive < 5%
[ ] HITL Hard Stop < 500ms
```

---

## 4. Measurement Implementation

```python
# src/metrics/quality_metrics.py — ตัวอย่างโครงสร้าง

class QualityMetrics:
    def compute_pmi(self, stability, coverage, latency_compliance, security, ethics) -> float:
        """คำนวณ Protocol Maturity Index"""
        return (stability + coverage + latency_compliance + security + ethics) / 5

    def generate_report(self) -> dict:
        """สร้าง Quality Report ครอบคลุมทุก Metric"""
        return {
            "ml_accuracy": self.get_ml_accuracy(),
            "latency_p95": self.get_latency_percentile(95),
            "daft_pass_rate": self.get_daft_pass_rate(),
            "pmi": self.compute_pmi(...),
            "ethics_compliance": self.get_ethics_compliance_rate(),
            "hitl_stats": self.get_hitl_statistics(),
            "test_coverage": self.get_test_coverage(),
        }

    def export_markdown(self, filepath: str):
        """Export รายงานเป็น Markdown"""
        ...

    def export_json(self, filepath: str):
        """Export รายงานเป็น JSON"""
        ...
```

---

*Brain-Net Quality Metrics Document | อัปเดตล่าสุด: Sprint 3*
