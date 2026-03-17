# 🗺️ Brain-Net Phase 2 Roadmap
**Post-MVP Development Plan**

*Owner: ทีม Brain-Net*
*Base: MVP v1.0 delivered at end of Sprint 4*

---

## 1. Phase 2 Vision

Phase 1 (MVP) ได้พิสูจน์ว่า Brain-Net Protocol สามารถส่ง Cognitive State Symbols ระหว่าง 2 โหนดได้อย่างปลอดภัยและมีจริยธรรม

**Phase 2 Vision:** ขยายจาก 2-node simulation สู่ **Multi-Node Brain-Net Mesh** พร้อม Real QKD Integration และ Clinical-Grade Security

---

## 2. Phase 2 Epics

### Epic P2-01: Multi-Node Mesh Network
**Goal:** รองรับ N โหนด (N ≥ 10) พร้อม Mesh Routing

| Story | Description | Owner | Estimate |
|-------|-------------|-------|----------|
| P2-01-01 | Mesh Router: ขยาย TTPRouter เป็น Multi-hop routing | เจม | 8 SP |
| P2-01-02 | Node Discovery Protocol: Auto-discover nodes ใน subnet | เจม | 5 SP |
| P2-01-03 | Multi-node Consensual Handshake: N-party consent | รักบี้ | 8 SP |
| P2-01-04 | Mesh Firewall: Distributed firewall rules | รักบี้ | 5 SP |
| P2-01-05 | Latency Budget: ขยาย latency budget สำหรับ multi-hop | เจม | 3 SP |

### Epic P2-02: Real QKD Integration
**Goal:** แทนที่ MockQKD ด้วย Real Quantum Key Distribution

| Story | Description | Owner | Estimate |
|-------|-------------|-------|----------|
| P2-02-01 | QKD Hardware Adapter: Interface กับ BB84 protocol device | โยรุ | 13 SP |
| P2-02-02 | Key Distribution Service: Centralized QKD key management | โยรุ | 8 SP |
| P2-02-03 | Post-Quantum Fallback: Kyber-1024 fallback เมื่อ QKD ไม่พร้อม | โยรุ | 8 SP |
| P2-02-04 | QKD Performance Test: Verify overhead ยังคง < 15ms | โยรุ + เจม | 3 SP |

### Epic P2-03: Real BCI Hardware Support
**Goal:** เชื่อมต่อกับ BCI Headset จริง (OpenBCI, Emotiv, Neuralink API)

| Story | Description | Owner | Estimate |
|-------|-------------|-------|----------|
| P2-03-01 | OpenBCI Adapter: Hardware driver สำหรับ OpenBCI Cyton | บี | 8 SP |
| P2-03-02 | Emotiv EPOC+ Adapter | บี | 8 SP |
| P2-03-03 | Real-time EEG Calibration: Per-subject baseline calibration | บี | 5 SP |
| P2-03-04 | Artifact Rejection Upgrade: ICA-based artifact removal | บี | 8 SP |
| P2-03-05 | ML Model Retraining: Train on real human EEG data | บี | 13 SP |

### Epic P2-04: Neural Dictionary Expansion
**Goal:** ขยาย Neural Dictionary จาก 4 symbols สู่ 64+ symbols

| Story | Description | Owner | Estimate |
|-------|-------------|-------|----------|
| P2-04-01 | Neural Dict v2: เพิ่ม 20 symbols (emotions, intents) | บี | 13 SP |
| P2-04-02 | DAFT v2: Domain mapping สำหรับ 64 symbols | เจม + บี | 8 SP |
| P2-04-03 | Ambiguity Resolution: Handle overlapping EEG patterns | บี | 8 SP |
| P2-04-04 | Multi-label Classification: Support compound states | บี | 5 SP |

### Epic P2-05: Clinical-Grade Ethics & Compliance
**Goal:** เตรียม Brain-Net สำหรับ Clinical Trial Submission

| Story | Description | Owner | Estimate |
|-------|-------------|-------|----------|
| P2-05-01 | IRB Compliance Package: Prepare Institutional Review Board docs | โอเล่ | 13 SP |
| P2-05-02 | Ethics v2: 10 rules (E-001 to E-010) | โอเล่ | 8 SP |
| P2-05-03 | Longitudinal Consent: Time-bound consent with renewal | โอเล่ + รักบี้ | 8 SP |
| P2-05-04 | Clinical Audit: FDA 21 CFR Part 11 compliant audit log | โอเล่ | 13 SP |
| P2-05-05 | Neurorights Legal Framework: Engage legal counsel | โอเล่ | 5 SP |

### Epic P2-06: Developer SDK & API
**Goal:** เปิด Brain-Net Protocol เป็น Public SDK

| Story | Description | Owner | Estimate |
|-------|-------------|-------|----------|
| P2-06-01 | Python SDK: `brainnet-sdk` PyPI package | เจม | 8 SP |
| P2-06-02 | REST API: HTTP wrapper for Brain-Net pipeline | เจม | 8 SP |
| P2-06-03 | WebSocket Support: Real-time streaming API | เจม | 5 SP |
| P2-06-04 | Documentation Site: Full API docs (Sphinx/MkDocs) | ทีม | 5 SP |
| P2-06-05 | Example Applications: 3 demo apps using SDK | ทีม | 8 SP |

---

## 3. Phase 2 Sprint Plan (Tentative)

```
Sprint 5  (Weeks 1–2):  P2-01 Multi-Node Foundation + P2-03 Hardware Adapters
Sprint 6  (Weeks 3–4):  P2-02 QKD Integration + P2-04 Neural Dict v2
Sprint 7  (Weeks 5–6):  P2-03 Real BCI Integration + P2-05 Ethics v2
Sprint 8  (Weeks 7–8):  P2-01 Mesh Complete + P2-06 SDK Alpha
Sprint 9  (Weeks 9–10): Integration Testing + Clinical Validation
Sprint 10 (Weeks 11–12): Phase 2 MVP — Clinical Trial Submission Ready
```

---

## 4. Phase 2 Quality Targets

| Metric | Phase 1 MVP | Phase 2 Target |
|--------|-------------|----------------|
| **ML Accuracy** | ≥ 85% (4 symbols) | ≥ 90% (64 symbols) |
| **E2E P95 Latency** | < 50ms (2-node) | < 75ms (10-node mesh) |
| **QKD Overhead** | < 15ms (AES mock) | < 10ms (Real QKD) |
| **Neural Dictionary Size** | 4 symbols | 64+ symbols |
| **Supported BCI Devices** | Mock only | 3 real devices |
| **Ethics Rules** | 5 rules | 10 rules |
| **PMI** | ≥ 4.2 | ≥ 4.8 |
| **Nodes Supported** | 2 | 10+ |

---

## 5. Technology Dependencies

| Technology | Current (Phase 1) | Phase 2 Upgrade |
|-----------|-------------------|-----------------|
| Encryption | AES-256-GCM (Mock QKD) | Real BB84 QKD + Kyber-1024 |
| BCI | Simulated EEG | OpenBCI Cyton + Emotiv EPOC+ |
| ML Model | Random Forest | Transformer-based EEG model |
| Network | 2-node VirtualNetwork | Mesh (10+ nodes, IP-based) |
| Ethics | 5 rules, automated | 10 rules + IRB-certified |
| Deployment | Local Python | Docker + Kubernetes |

---

## 6. Risk Register (Phase 2)

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Real QKD hardware not available | Medium | High | Use Kyber-1024 fallback |
| Real EEG data collection ethics approval delayed | High | High | Use public EEG datasets (BCIC IV) |
| ML accuracy drops with 64 symbols | Medium | Medium | Start with 16 symbols, expand iteratively |
| Clinical trial IRB rejection | Low | Critical | Pre-consult with IRB before Sprint 9 |
| Latency degradation in mesh routing | Medium | High | Optimize routing algorithm early in Sprint 5 |

---

## 7. Team Scaling Plan

| Role | Phase 1 | Phase 2 Addition |
|------|---------|-----------------|
| BCI Engineer | บี | + 1 EEG Data Scientist |
| Network Architect | เจม | + 1 Distributed Systems Engineer |
| Security Specialist | รักบี้ | + 1 Quantum Cryptographer |
| Neuroethics Lead | โอเล่ | + 1 Clinical Ethics Advisor |
| Quantum Specialist | โยรุ | + 1 QKD Hardware Engineer |

---

*Brain-Net Phase 2 Roadmap v1.0*
*Prepared post-Sprint 4 MVP delivery*
