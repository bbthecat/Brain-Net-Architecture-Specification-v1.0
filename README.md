# 🧠 Brain-Net Protocol — Phase 1 MVP

**Brain-Computer Interface Neural Communication Protocol**
*Thought Transfer Protocol (TTP) with Cognitive Liberty Protection*

---

## 🏗️ Project Structure

```
brain-net/
├── src/
│   ├── bci/                    # BCI Hardware & EEG Processing
│   │   ├── __init__.py
│   │   ├── connect_bci.py      # BCIConnection — mock EEG stream
│   │   ├── clean_eeg_data.py   # EEGPreprocessor — feature extraction
│   │   └── neural_classifier.py # NeuralClassifier — Random Forest
│   ├── daft/                   # Domain Adaptive Formalization & Translation
│   │   ├── __init__.py
│   │   ├── domain_interface.py # 4-domain mapper (Bio/Phy/Neuro/Quantum)
│   │   └── daft_validator.py   # MathSymbol validator
│   ├── protocol/               # Thought Transfer Protocol
│   │   ├── __init__.py
│   │   ├── ttp_packet.py       # TTPHeader + TTPPacket (32-byte header)
│   │   ├── ttp_router.py       # TTPRouter — latency-budget routing
│   │   ├── virtual_network.py  # 2-node network simulator
│   │   └── context_frame.py    # Contextual framing (Data Link Layer)
│   ├── security/               # Cognitive Liberty Security Stack
│   │   ├── __init__.py
│   │   ├── brain_firewall.py   # BrainFirewall (FW-001 to FW-003)
│   │   ├── consensual_handshake.py # ConsensualHandshake (C-001 to C-004)
│   │   ├── ethics_rule_engine.py   # EthicsRuleEngine (E-001 to E-005)
│   │   ├── hitl_checkpoint.py  # Human-in-the-Loop (H-001 to H-004)
│   │   └── audit_log.py        # Immutable hash-chain audit log
│   ├── crypto/                 # Cryptography
│   │   ├── __init__.py
│   │   └── mock_qkd_aes.py     # MockQKD — AES-256-GCM
│   ├── metrics/                # Quality Metrics
│   │   ├── __init__.py
│   │   └── quality_metrics.py  # QualityMetrics + PMI
│   ├── brain_net_pipeline.py   # Full E2E Pipeline Orchestrator
    ├── gui_app.py              # Desktop GUI (Tkinter)
    └── web_gui.py              # 🚀 Modern Web GUI Dashboard (Recommended)
├── tests/
│   ├── conftest.py             # Shared pytest fixtures
│   ├── unit/                   # Unit tests (fast, isolated)
│   │   ├── test_ttp_packet.py
│   │   ├── test_brain_firewall.py
│   │   ├── test_consensual_handshake.py
│   │   ├── test_audit_log.py
│   │   ├── test_ethics_rule_engine.py
│   │   ├── test_hitl_checkpoint.py
│   │   ├── test_daft.py
│   │   ├── test_mock_qkd.py
│   │   ├── test_quality_metrics.py
│   │   ├── test_eeg_preprocessing.py
│   │   └── test_ttp_router.py
│   ├── integration/            # Integration tests (multi-component)
│   │   ├── test_security_stack.py
│   │   └── test_daft_pipeline.py
│   └── e2e/                    # End-to-end tests (full pipeline)
│       └── test_brain_net_e2e.py
├── docs/
│   ├── architecture/
│   │   └── ARCHITECTURE.md     # Architecture Specification
│   ├── ethics/
│   │   ├── COGNITIVE_LIBERTY.md
│   │   ├── COMPLIANCE_MATRIX.md
│   │   └── DATA_GOVERNANCE.md
│   ├── metrics/
│   │   └── QUALITY_METRICS.md
│   ├── planning/
│   │   ├── IMPLEMENTATION_PLAN.md
│   │   ├── RESPONSIBILITIES.md
│   │   └── ROADMAP_PHASE2.md
│   └── sprints/
│       ├── SPRINT-1-FIRST-WHISPER.md
│       ├── SPRINT-2-SIGNAL-BRIDGE.md
│       ├── SPRINT-3-DEEP-CALIBRATION.md
│       └── SPRINT-4-MVP-FINAL.md
├── data/
│   └── generate_mock_dataset.py
├── CHANGELOG.md                # Project history and version tracking
├── README.md                   # This file
├── GITHUB_SETUP_GUIDE.md       # Guide for repository setup
├── ci.yml                      # GitHub Actions CI/CD workflow
├── pyproject.toml              # Project metadata & build tool config
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
└── .gitignore                  # Git ignore rules
```

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate mock EEG dataset
python data/generate_mock_dataset.py --n 600 --verify

# 3. Train neural classifier
python -m src.bci.neural_classifier

# 4. Run full pipeline demo
python -m src.brain_net_pipeline

# 5. Run Modern Web GUI (Recommended)
streamlit run src/web_gui.py

# 6. Run Classic Desktop GUI
python src/gui_app.py

# 7. Run all tests
python -m pytest tests/ --cov=src/ --cov-report=term-missing

# 8. Run only unit tests (fast)
python -m pytest tests/unit/ -v

# 9. Run E2E tests
python -m pytest tests/e2e/ -v
```

---

## 🔒 Security Architecture

```
[Input] → [DAFT Validator] → [Ethics Engine (E-001–E-005)]
                                      ↓ ALLOW
                            [Brain Firewall (FW-001–FW-003)]
                                      ↓ PASS
                             [HITL Checkpoint (H-001–H-004)]
                                      ↓ CLEAR
                              [MockQKD AES-256-GCM]
                                      ↓
                              [Virtual Network]
```

---

## 📊 MVP Quality Gates

| Metric | Target | Description |
|--------|--------|-------------|
| ML Accuracy | ≥ 85% | Neural Dict classifier holdout accuracy |
| E2E P95 Latency | < 50ms | End-to-end transmission time |
| DAFT Pass Rate | ≥ 95% | Valid inputs passing DAFT validation |
| Ethics Compliance | 100% | All Ethics Rules E-001 to E-005 |
| Firewall Block Accuracy | ≥ 99% | Malicious packet block rate |
| HITL Hard Stop | < 500ms | Response time from trigger to stop |
| QKD Overhead | < 15ms | AES-256 encryption overhead |
| Test Coverage | ≥ 80% | pytest line coverage |
| PMI | ≥ 4.2 | Protocol Maturity Index overall score |

---

## ⚖️ Cognitive Liberty Principles

Brain-Net is built on 3 core principles:

1. **Right to Mental Privacy** — Raw EEG and neural payload are NEVER stored or logged
2. **Right to Mental Integrity** — Consent Score ≥ 0.7 required for every transmission
3. **Right to Psychological Continuity** — HITL oversight prevents coerced transmission

---

## 👥 Team

| Role | Person | Responsibility |
|------|--------|----------------|
| BCI Engineer | บี | EEG preprocessing, ML classifier |
| Network Architect | เจม | TTP protocol, routing, pipeline |
| Security Specialist | รักบี้ | Firewall, handshake, HITL |
| Neuroethics Lead | โอเล่ | Ethics engine, audit log, compliance |
| Quantum Specialist | โยรุ | MockQKD, encryption |

---

*Brain-Net Phase 1 MVP | Cognitive Liberty Framework v1.0*
