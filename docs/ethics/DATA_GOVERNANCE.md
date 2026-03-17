# 🗄️ Data Governance Policy
**Brain-Net Project — Neural Data Governance v1.0**

*Owner: นายรัชชานนท์ ประดับแก้ว (โอเล่) — Neuroethics Lead*
*Effective Sprint 4 (MVP)*

---

## 1. Scope

เอกสารนี้ครอบคลุมข้อมูลทุกประเภทที่ Brain-Net Phase 1 ประมวลผล:

| Data Category | Description | Sensitivity |
|--------------|-------------|-------------|
| **Raw EEG Signal** | ข้อมูล EEG ดิบจาก BCI Headset | 🔴 Critical |
| **Neural Payload** | Cognitive State Symbol (focus/relax/reject/neutral) | 🔴 Critical |
| **TTP Packet Metadata** | Header: source/dest IDs, timestamp, symbol_id | 🟡 High |
| **Emotion Vectors** | Valence, Arousal, Intensity (scalar values only) | 🟡 High |
| **Consent Score** | Numeric score 0.0–1.0 | 🟡 High |
| **Audit Log Entries** | Hashed IDs + decision metadata | 🟢 Medium |
| **Quality Metrics** | Latency, PMI scores, pass rates (no user data) | 🟢 Low |

---

## 2. Data Retention Policy

### 2.1 Session Data (Raw EEG + Neural Payload)

```
Retention: SESSION DURATION ONLY
Action:    Auto-purge on session close (within 10ms — Teardown Rule C-005)
Storage:   Memory only — NEVER persisted to disk or logs
Legal:     GDPR Art. 5 (Data Minimization) + Art. 17 (Right to Erasure)
```

### 2.2 Audit Log (Ethics Decisions)

```
Retention: 90 days (configurable per deployment)
Format:    Hashed IDs only — no plaintext user data
Storage:   Append-only, hash-chain protected
Legal:     GDPR Art. 25 (Privacy by Design)
```

### 2.3 Quality Metrics

```
Retention: Indefinite (aggregated, anonymized)
Format:    Latency percentiles, PMI scores — no individual records
Storage:   reports/ directory (JSON + Markdown)
Legal:     No PII — no restriction
```

### 2.4 ML Training Data

```
Retention: Project duration
Format:    Labeled EEG features (no raw waveforms, no subject identity)
Storage:   data/clean_eeg_data.csv (mock/synthetic only in Phase 1)
Legal:     Synthetic data — no real subjects in Phase 1
```

---

## 3. Access Control Matrix

| Role | Raw EEG | Neural Payload | Audit Log | Quality Metrics |
|------|---------|---------------|-----------|-----------------|
| BCI Engineer (บี) | ✅ Read | ❌ No Access | ❌ No Access | ✅ Read |
| Network Architect (เจม) | ❌ No Access | ❌ No Access | ❌ No Access | ✅ Full |
| Security Specialist (รักบี้) | ❌ No Access | ❌ No Access | ✅ Read-Only | ✅ Read |
| Neuroethics Lead (โอเล่) | ❌ No Access | ❌ No Access | ✅ Full | ✅ Full |
| Quantum Specialist (โยรุ) | ❌ No Access | ❌ No Access | ❌ No Access | ✅ Read |
| System (Automated Pipeline) | ✅ Process & Delete | ✅ Transmit Only | ✅ Append Only | ✅ Write |

**Rule: No human operator may read raw neural payload or raw EEG at any time.**

---

## 4. Data Flow Diagram

```
[BCI Headset]
     │
     ▼ Raw EEG (in-memory only)
[EEGPreprocessor]
     │
     ▼ CleanEEGFeatures (numeric features, no waveform)
[NeuralClassifier / DomainInterface]
     │
     ▼ MathSymbol (domain-agnostic representation)
[DAFTValidator] ──── FAIL ──→ [Blocked + Logged (no payload)]
     │
     ▼ PASS
[TTPPacket Assembly] (symbol + emotion vectors + consent score)
     │
     ▼
[EthicsRuleEngine] ──── BLOCK ──→ [AuditLog (hashed IDs only)]
     │
     ▼ ALLOW
[BrainFirewall] ──── BLOCK ──→ [Dropped, no log of content]
     │
     ▼ PASS
[HITLCheckpoint] ──── TRIGGER ──→ [Alert + Pause (content never logged)]
     │
     ▼ CLEAR
[MockQKD Encrypt] ──→ [Encrypted bytes only, key in memory]
     │
     ▼
[VirtualNetwork] ──→ [TransmissionLog (packet_id, latency, symbol_name)]
     │
     ▼
[Session End] ──→ [Auto-purge all session buffers within 10ms]
```

**Data that is NEVER stored anywhere:**
- Raw EEG waveform
- Full neural payload content
- Plaintext user/session IDs
- Decoded thought content

---

## 5. Breach Response Protocol

### 5.1 Detection
- `AuditLog.verify_chain()` runs automatically — any tampering detected within 1 verification cycle
- `QualityMetrics` tracks `private_payload_leak_rate` — target = 0

### 5.2 Response Steps

```
Step 1: Immediately suspend all active sessions
Step 2: Lock AuditLog (freeze append operations)  
Step 3: Notify Neuroethics Lead (โอเล่) within 15 minutes
Step 4: Preserve hash chain for forensic analysis
Step 5: Purge all in-memory session data
Step 6: Root cause analysis + Ethics Rule Engine audit
Step 7: Issue incident report within 72 hours (GDPR Art. 33)
```

### 5.3 Severity Levels

| Level | Description | Example | Response Time |
|-------|-------------|---------|---------------|
| 🔴 Critical | Neural payload accessed without consent | Private thought leaked to log | Immediate (<15 min) |
| 🟠 High | Hash chain broken (potential tampering) | Audit log modified | <1 hour |
| 🟡 Medium | Session data not purged within 10ms | Memory buffer leak | <4 hours |
| 🟢 Low | Metric data anomaly | Unexpected PMI drop | <24 hours |

---

## 6. GDPR Compliance Checklist

| Article | Requirement | Brain-Net Implementation | Status |
|---------|-------------|--------------------------|--------|
| Art. 5 | Data Minimization | Store only metadata, never payload | ✅ Sprint 3 |
| Art. 7 | Consent | Consent Score ≥ 0.7 required for all transmissions | ✅ Sprint 1 |
| Art. 17 | Right to Erasure | Auto-purge on session close | 🔄 Sprint 4 |
| Art. 22 | Automated Decision-Making | HITL ensures human oversight | ✅ Sprint 3 |
| Art. 25 | Privacy by Design | Ethics Engine built into pipeline core | ✅ Sprint 3 |
| Art. 32 | Security of Processing | AES-256 + Brain Firewall | ✅ Sprint 2 |
| Art. 33 | Breach Notification | Breach response protocol defined | ✅ Sprint 4 |

---

## 7. Data Governance Enactment

```
I, นายรัชชานนท์ ประดับแก้ว (โอเล่), Neuroethics Lead,
hereby enact this Data Governance Policy for Brain-Net Phase 1.

This policy takes effect upon MVP delivery and binds all
team members with access to Brain-Net systems.

Enacted: _______________
Signature: _______________  (Neuroethics Lead)
Co-signed: _______________  (Security Specialist)
```

---

*Data Governance Policy v1.0 | Brain-Net Phase 1 MVP*
