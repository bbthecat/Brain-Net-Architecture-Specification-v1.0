# 📋 CHANGELOG — Brain-Net Project

All notable changes to Brain-Net are documented here.
Format: `[vX.Y] — Sprint Name — Date`

---

## [v4.0] — Sprint 4: "Final Whisper" (MVP) — Week 13–16 🚀 Planned

### Added
- `BrainNetPipeline` — Full E2E orchestrator integrating all Sprint 1–3 components
- Final Security Penetration Test (Semantic Injection, Header Spoofing, Replay Attack)
- Ethics Certificate v1.0 (Signed by Neuroethics Lead)
- Neural Data Governance Policy v1.0 (Enacted & Signed)
- HITL Stress Test (50 concurrent sessions, 10% anomaly rate)
- Demo Video (Full E2E MVP walkthrough, ≤ 10 minutes)
- Final Presentation Slides (10–15 pages)
- ROADMAP_PHASE2.md — Strategic path to Sensory Casting
- GitHub Release Tag: `v1.0-mvp`

### Improved
- E2E P95 Latency < 50ms (from ~85ms in Sprint 1)
- Test Coverage ≥ 80% (from ~30% in Sprint 1)

### Targets
| Metric | Target |
|--------|--------|
| ML Accuracy | ≥ 85% |
| E2E P95 Latency | < 50ms |
| PMI Score | ≥ 3.5 |
| Ethics Compliance | 100% |
| Critical Bugs | 0 |

---

## [v3.0] — Sprint 3: "Deep Calibration" — Week 9–12 🔄 In Progress

### Added
- **DAFT (Domain Adaptive Formalization & Translation)** — `src/daft/`
  - `DomainInterface` class: 4 domain mappers (Bio/Phy/Neuro/Quantum)
  - `MathSymbol` data class: Universal mathematical representation
  - `DAFTValidator`: Range, Dimension, Consent validation
- **Math Formalization Documents** for all 4 domains (LaTeX)
- **Multi-Domain ML Dataset** — `data/multi_domain_dataset.csv`
- **Neural Dictionary v2** — `models/neural_dict_v2.pkl` (≥ 85% accuracy)
- **Quality Dashboard** — `src/metrics/quality_metrics.py`
- **Protocol Maturity Index (PMI)** definition and measurement
- **Ethics Rule Engine** — `src/security/ethics_rule_engine.py` (Automated)
- **Immutable Audit Log** with Hash Chain — `src/security/audit_log.py`
- **HITL Checkpoint** — `src/security/hitl_checkpoint.py`
- **HITL CLI Dashboard** — `src/dashboard/hitl_cli.py`
- **Ethics Compliance Matrix** vs UNESCO/Neurorights/GDPR
- **Neural Data Governance Policy v0.9**
- **GitHub Actions CI/CD** — Automated pytest on every push

### Fixed
- ISS-001: ML Accuracy improved from 78% to ≥ 85% (Multi-domain data)
- ISS-002: TTP now supports Bio/Physical Domain inputs via DomainInterface
- ISS-003: Formal Quality Metrics Dashboard established (PMI)
- ISS-004: Ethics Rules now automated via EthicsRuleEngine (not manual)
- ISS-005: HITL Checkpoint added for anomaly hard-stop
- ISS-006: Quantum Encryption overhead reduced from 18ms to < 15ms

### Sprint 3 Metrics
| Metric | Sprint 2 | Sprint 3 |
|--------|----------|----------|
| ML Accuracy | 78% | ≥ 85% |
| Domains Supported | 1 | 4 |
| Ethics Automation | 0% | 100% |
| HITL System | None | Complete |

---

## [v2.0] — Sprint 2: "Signal Bridge" — Week 5–8 ✅ Completed

### Added
- TTP full implementation with Contextual Framing Layer
- Brain Firewall E2E integration with TTP stream
- Consensual Handshake Protocol v1.0
- Network Simulator: 2-node topology (Node A ↔ Node B)
- Mock QKD (AES-256) encryption pipeline
- ML Classifier v1: 3-state classification (Focus/Relax/Reject)
- Soft-Disconnect teardown protocol

### Improved
- ML Accuracy: 72% → 78% (Hyperparameter tuning)
- Encryption Overhead reduced to 18ms

### Known Issues (→ Sprint 3)
- ISS-001: ML Accuracy 78% (below 80% target)
- ISS-002: TTP does not support Bio/Physical domain inputs
- ISS-003: No formal Quality Metrics system
- ISS-004: Ethics Audit remains manual process
- ISS-005: No Human-in-the-Loop safety mechanism
- ISS-006: Quantum Overhead 18ms (above 15ms target)

---

## [v1.0] — Sprint 1: "First Whisper" — Week 1–4 ✅ Completed

### Added
- Project scaffolding and GitHub repository setup
- Cognitive Liberty Rulebook v1.0 (โอเล่)
- TTP Header Architecture Blueprint (เจม)
- `TTPHeader`, `TTPRouter`, `TTPPacket` classes
- `ContextFrame` module with Valence/Arousal vectors
- Brain Threat Model document (รักบี้)
- `BrainFirewall` class with Consent Score evaluation
- `MockQKD_AES` AES-256 encryption module
- EEG Data import from PhysioNet/MIMIC
- Bandpass Filter and Artifact Rejection pipeline
- `neural_dict_v1.pkl` — Random Forest Classifier (Focus/Relax/Reject)
- Network Simulator: 3-node (Sender/Router/Receiver)
- Ethics Audit Log (Timestamp, Reason, User ID only)
- Sprint 1 Demo Video

### Sprint 1 Metrics
| Metric | Result |
|--------|--------|
| ML Accuracy | 78% |
| E2E Latency | ~85ms |
| Domains Supported | 1 (Neuro) |
| Ethics Audit | Manual PASS |

---

## [v0.1] — Pre-Sprint: Architecture & Planning — 2026-02-22

### Added
- `ARCHITECTURE.md` — Brain-Net Protocol Stack v1.0
- `IMPLEMENTATION_PLAN.md` — 4-week implementation framework
- `RESPONSIBILITIES.md` — RACI Matrix & Role Boundaries
- Team Roles: Assigned (เจม, บี, รักบี้, โอเล่, โยรุ)
- Strategic Roadmap: Phase 1–5 (2026–2500+)

---

*Brain-Net Project | Phase 1: Synthetic Telepathy*
