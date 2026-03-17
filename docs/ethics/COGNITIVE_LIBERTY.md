# ⚖️ Cognitive Liberty Framework & Ethics Compliance
**Brain-Net Project — Neuroethics Foundation Document v1.0**

*Owner: นายรัชชานนท์ ประดับแก้ว (โอเล่) — Neuroethics Lead*

---

## 1. Cognitive Liberty Rulebook v1.0

### 1.1 Core Principles

**Cognitive Liberty** คือ "เสรีภาพทางความคิด" — สิทธิเด็ดขาดของมนุษย์ที่จะรักษาความเป็นส่วนตัวและควบคุมจิตใจตนเองจากการแทรกแซงทางเทคโนโลยี

Brain-Net ยึดถือหลักการ 3 ข้อ:

1. **Right to Mental Privacy** — สิทธิที่จะไม่ถูกอ่านความคิดโดยไม่ได้รับความยินยอม
2. **Right to Mental Integrity** — สิทธิที่จะไม่ถูกยัดเยียดความคิด/อารมณ์โดยไม่ยินยอม
3. **Right to Psychological Continuity** — สิทธิที่จะรักษาเอกลักษณ์และตัวตนของตนเอง

### 1.2 Consent Score Definition

```
Consent Score (CS) ∈ [0.0, 1.0]

CS = w₁·(Voluntary_Signal) + w₂·(Arousal_Baseline_Normal) + w₃·(No_Coercion_Marker)

โดยที่:
  w₁ = 0.5  (น้ำหนักความสมัครใจ)
  w₂ = 0.3  (น้ำหนักสถานะปกติของ Arousal)
  w₃ = 0.2  (น้ำหนักการไม่มีสัญญาณบีบบังคับ)

Threshold:
  CS ≥ 0.7  → ALLOW (ยินยอมและปลอดภัย)
  CS 0.5–0.69 → QUARANTINE (ต้องตรวจสอบเพิ่ม / HITL Alert)
  CS < 0.5   → BLOCK (ห้ามส่งโดยเด็ดขาด)
```

### 1.3 Private Thought Boundary (Mathematical)

```
ข้อมูล EEG Input: X ∈ ℝ^{channels × time}
Feature Space:    F = {f₁, f₂, ..., fₙ}  (EEG Features)
Symbol Space:     S = {focus, relax, reject, neutral}

Private Boundary B_private:
  B_private = {x ∈ X | frequency(x) ∉ [8Hz, 13Hz] AND amplitude(x) > θ_private}

Shareable Space:
  S_shareable = X \ B_private  (เซตส่วนเติมเต็มของ B_private)

กฎ: ห้ามส่ง x ∈ B_private ผ่าน TTP ไม่ว่ากรณีใดทั้งสิ้น
```

### 1.4 Coercion Indicators (สัญญาณการบีบบังคับ)

| Indicator | Definition | Threshold | Action |
|-----------|-----------|----------|--------|
| **Panic State** | Arousal สูงผิดปกติ | Arousal > 0.9 | Auto-Reject + HITL Alert |
| **Stress Spike** | Arousal เพิ่มขึ้น > 50% ใน 2 วินาที | ΔArousal/Δt > 0.25/s | Quarantine + HITL Review |
| **Repeated Rejection** | ผู้ส่งพยายามส่งซ้ำหลังจากถูก Reject | ≥ 3 ครั้งใน 10 วินาที | Block Session + Log |
| **Subconscious Dissent** | Valence ติดลบสูง | Valence < -0.7 | Auto-Reject Connection |
| **Identity Override Attempt** | Pattern ตรงกับ Semantic Injection Signature | Pattern Match ≥ 80% | Block & Log to Ethics DB |

---

## 2. Ethics Rule Engine Specification

### 2.1 Rule Set (Brain Firewall Integration)

```python
# Ethics Rules — สามารถใช้งานได้ใน EthicsRuleEngine

ETHICS_RULES = [
    # Rule E-001: Consent Required
    {
        "id": "E-001",
        "name": "Consent Score Minimum",
        "condition": "packet.consent_score >= 0.7",
        "violation_action": "BLOCK",
        "log_message": "Consent Score below threshold"
    },
    # Rule E-002: No Private Thought Transmission
    {
        "id": "E-002",
        "name": "Private Thought Boundary",
        "condition": "not packet.is_in_private_boundary()",
        "violation_action": "BLOCK",
        "log_message": "Private thought boundary violation"
    },
    # Rule E-003: No Coercion
    {
        "id": "E-003",
        "name": "Coercion-Free Transmission",
        "condition": "packet.arousal <= 0.9 and packet.valence >= -0.7",
        "violation_action": "BLOCK_AND_HITL",
        "log_message": "Coercion indicator detected"
    },
    # Rule E-004: No Payload in Logs
    {
        "id": "E-004",
        "name": "Log Privacy Protection",
        "condition": "log_entry.contains_no_payload()",
        "violation_action": "QUARANTINE",
        "log_message": "Attempted payload logging detected"
    },
    # Rule E-005: Session Teardown Cleanliness
    {
        "id": "E-005",
        "name": "Clean Session Teardown",
        "condition": "session.all_buffers_cleared()",
        "violation_action": "FORCE_CLEAR",
        "log_message": "Session teardown incomplete"
    }
]
```

---

## 3. International Regulations Compliance Matrix

| Regulation | Relevant Article | Brain-Net Requirement | Status |
|-----------|-----------------|----------------------|--------|
| **UNESCO AI Ethics (2021)** | Art. 4.1 — Human dignity | Private Thought Boundary enforced | 🔄 Sprint 3 |
| **UNESCO AI Ethics (2021)** | Art. 4.6 — Transparency | Ethics Audit Log (Immutable) | ✅ Sprint 3 |
| **Neurorights Foundation** | Mental Privacy | Consent Score ≥ 0.7 required | 🔄 Sprint 3 |
| **Neurorights Foundation** | Mental Integrity | Semantic Injection Prevention | ✅ Sprint 2 |
| **Neurorights Foundation** | Cognitive Liberty | Voluntary Opt-in only | ✅ Sprint 1 |
| **GDPR (Neural Data)** | Art. 5 — Data Minimization | Auto-delete after session | 🔄 Sprint 4 |
| **GDPR (Neural Data)** | Art. 17 — Right to Erasure | Session data purge protocol | 🔄 Sprint 4 |
| **GDPR (Neural Data)** | Art. 25 — Privacy by Design | Ethics Rule Engine built-in | ✅ Sprint 3 |

**Legend:** ✅ Compliant | 🔄 In Progress | ❌ Non-Compliant | ⚠️ Partial

---

## 4. Audit Log Schema

```json
// Ethics Audit Log Entry — GDPR Compliant Schema
// ห้ามมี neural_payload, raw_eeg, thought_content ใน Log ไม่ว่ากรณีใด

{
  "log_id": "uuid-v4",
  "timestamp": "ISO-8601",
  "session_id": "hash(session)",     // hashed — ไม่ใช่ raw session ID
  "user_id": "hash(user)",           // hashed — ไม่ใช่ plaintext
  "rule_id": "E-001",
  "decision": "BLOCK | ALLOW | QUARANTINE | HITL",
  "domain": "bio | phy | neuro | quantum",
  "consent_score": 0.65,             // numeric score เท่านั้น
  "arousal_level": 0.45,             // numeric เท่านั้น
  "previous_hash": "sha256(prev)",   // Hash Chain
  "this_hash": "sha256(this)"        // Immutable verification
}
```

---

## 5. Ethics Certificate Template (Sprint 4)

```
╔═══════════════════════════════════════════════════════════╗
║           BRAIN-NET ETHICS CERTIFICATE v1.0               ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  I, นายรัชชานนท์ ประดับแก้ว (โอเล่),                      ║
║  Neuroethics Lead of Brain-Net Project,                   ║
║  hereby certify that Brain-Net MVP v1.0 has been          ║
║  reviewed and found to be in compliance with:             ║
║                                                           ║
║  ✅ Cognitive Liberty Framework v1.0                      ║
║  ✅ All 5 Core Ethics Rules (E-001 to E-005)              ║
║  ✅ UNESCO AI Ethics Recommendation (2021)                ║
║  ✅ Neurorights Foundation Framework                      ║
║  ✅ GDPR Neural Data Requirements                         ║
║                                                           ║
║  The system:                                              ║
║  - Does NOT store Neural Payload in any log               ║
║  - Requires Consent Score ≥ 0.7 for all transmissions    ║
║  - Detects and blocks all Coercion Indicators             ║
║  - Maintains Immutable Ethics Audit Log                   ║
║  - Purges all session data after session ends             ║
║                                                           ║
║  Issued: _______________                                  ║
║  Signed: _______________  (Neuroethics Lead)              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

*Cognitive Liberty Framework v1.0 | Brain-Net Phase 1*
*Owner: นายรัชชานนท์ ประดับแก้ว (โอเล่) — Neuroethics Lead*
