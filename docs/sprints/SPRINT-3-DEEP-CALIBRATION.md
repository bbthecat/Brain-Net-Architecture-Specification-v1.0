# 🧠 Brain-Net Sprint Execution Plan — Sprint 3: "Deep Calibration"
**Fix Issues and Make Improvements**

---

## 📌 1. Executive Sprint Summary & Directives

| Attribute | Detail |
|-----------|--------|
| **Sprint Name** | BNET-Sprint-03: "Deep Calibration" |
| **Sprint Duration** | 4 Weeks (20 Working Days: Week 9–12) |
| **Sprint Theme** | แก้ไขปัญหาจาก Sprint 1–2 และยกระดับระบบให้พร้อมสำหรับ MVP |
| **Primary Goal** | สร้างระบบ **Domain Interface Mapping** ที่แปลงข้อมูลจาก 4 โดเมน (Bio/Phy/Neuro/Quantum) สู่สัญลักษณ์คณิตศาสตร์ (Math Formalization) และผ่านการตรวจสอบจาก **DAFT (Domain Adaptive Formalization & Translation)** |
| **Secondary Goal** | วัดและรับรอง Model/Protocol Maturity ด้วย Quality Metrics พร้อมวางโครงสร้าง Ethics Governance และ Human-in-the-Loop (HITL) ให้สมบูรณ์ |
| **Sprint Velocity (Target)** | 55 Story Points |
| **Sprint Start** | Week 9 Day 1 |
| **Sprint End** | Week 12 Day 20 |

---

## 🧩 2. Context: ปัญหาจาก Sprint ก่อนที่ต้องแก้

จากผลการ Retrospective ของ Sprint 1–2 พบประเด็นสำคัญที่ต้องได้รับการแก้ไขใน Sprint 3:

| Issue ID | ปัญหาที่พบ | Sprint ที่พบ | Priority | Owner |
|----------|----------|-------------|----------|-------|
| **ISS-001** | ML Classifier แยก 3 สถานะได้ความแม่นยำสูงสุด 78% (ต่ำกว่าเป้า 80%) | Sprint 2 | Critical | บี |
| **ISS-002** | TTP ยังไม่รองรับข้อมูลจาก Physical Domain (Bio Signals) | Sprint 2 | High | เจม |
| **ISS-003** | ไม่มีตัวชี้วัด (Metrics) ที่ชัดเจนว่าโปรโตคอล "สมบูรณ์แบบ" (Mature) ระดับไหน | Sprint 1–2 | High | All |
| **ISS-004** | กฎ Ethics ยังไม่ได้บังคับใช้แบบ Automated (ยังเป็น Manual Audit) | Sprint 2 | High | โอเล่ |
| **ISS-005** | ไม่มีกลไก Human-in-the-Loop ที่จะเตือนหรือหยุดระบบเมื่อเกิดเหตุผิดปกติ | Sprint 2 | Critical | รักบี้ |
| **ISS-006** | Quantum Encryption Overhead ยังสูงถึง 18ms (เกินเป้า 15ms) | Sprint 2 | Medium | โยรุ |

---

## 🎯 3. Sprint 3 Backlog & Acceptance Criteria

### 🌐 Epic 5: Domain Interface Mapping & DAFT Validation (Owner: เจม + บี)

> **DAFT = Domain Adaptive Formalization & Translation**
> ระบบแปลงข้อมูลจากโดเมนต่างๆ (Biological, Physical, Neurological, Quantum) ให้กลายเป็นสัญลักษณ์คณิตศาสตร์มาตรฐาน (Universal Math Symbols) ที่ TTP สามารถส่งผ่านเครือข่ายได้

| Ticket | User Story | Story Points | Acceptance Criteria (AC) |
|--------|------------|--------------|--------------------------|
| **BNET-501** | *As an architect, I need a Domain Interface Layer that maps Bio/Phy/Neuro/Quantum inputs to a unified mathematical representation.* | 8 | 1. คลาส `DomainInterface` รองรับ 4 โดเมน (Bio, Phy, Neuro, Quantum)<br>2. แต่ละโดเมนมี `mapper()` method ที่คืนค่า `MathSymbol` object<br>3. Unit Test ครอบคลุมทุก Domain ผ่านหมด<br>4. Mapping เสร็จใน < 5ms ต่อ 1 input |
| **BNET-502** | *As an engineer, I need formal mathematical definitions for each domain's signal space.* | 5 | 1. เอกสาร Math Formalization สำหรับแต่ละโดเมน (สูตร LaTeX)<br>2. Bio: Neural firing rate → frequency vector `f ∈ ℝⁿ`<br>3. Phy: EEG amplitude → normalized tensor `T ∈ [0,1]^{d×t}`<br>4. Neuro: Cognitive state → discrete symbol `s ∈ S = {focus, relax, reject, neutral}`<br>5. Quantum: Entanglement state → complex vector `|ψ⟩ ∈ ℂ²ⁿ` |
| **BNET-503** | *As a validator, I need DAFT to verify that all domain-mapped symbols are mathematically consistent before entering TTP.* | 8 | 1. คลาส `DAFTValidator` ที่รับ `MathSymbol` และตรวจสอบ:<br>   - ค่าอยู่ในช่วงที่กำหนด (Range Check)<br>   - มิติข้อมูลถูกต้อง (Dimension Check)<br>   - ค่า Consent Score ≥ 0.5<br>2. คืนค่า `ValidationResult(status, score, domain)` <br>3. Integration Test กับ TTPRouter ผ่าน |
| **BNET-504** | *As a team, we need a cross-domain consistency test to verify no information is lost during domain translation.* | 5 | 1. สคริปต์ทดสอบแปลงข้อมูลไป-กลับ (Round-trip Test) ทุกโดเมน<br>2. ข้อมูลที่แปลงกลับมาต้องมีค่า Cosine Similarity ≥ 0.95 กับต้นฉบับ<br>3. สรุปผลเป็น Domain Consistency Report |

---

### 📊 Epic 6: Model & Protocol Maturity / Quality Metrics (Owner: บี + เจม)

| Ticket | User Story | Story Points | Acceptance Criteria (AC) |
|--------|------------|--------------|--------------------------|
| **BNET-601** | *As a team lead, I need a formal Quality Dashboard that tracks all system metrics in one place.* | 5 | 1. ไฟล์ `quality_metrics.py` คำนวณและแสดงผล:<br>   - ML Accuracy (ต่อ Domain)<br>   - TTP Latency (P50 / P95 / P99)<br>   - Firewall Block Rate<br>   - DAFT Validation Pass Rate<br>2. Export เป็น JSON และ Markdown Report ได้ |
| **BNET-602** | *As an engineer, I need the ML Classifier to reach ≥ 85% accuracy across all 4 domain inputs.* | 8 | 1. เทรน Model ใหม่ด้วยข้อมูลครบ 4 โดเมน<br>2. Accuracy ≥ 85% บน Holdout Test Set (ไม่ใช่แค่ Train Set)<br>3. Confusion Matrix ที่แสดงความผิดพลาดต่อ Class<br>4. โมเดลบันทึกเป็น `neural_dict_v2.pkl` |
| **BNET-603** | *As a protocol owner, I need TTP Protocol Maturity Index (PMI) to be defined and measured.* | 3 | 1. นิยาม PMI ≥ 3 ด้าน: Stability, Coverage, Latency Compliance<br>2. PMI Score อยู่ใน Scale 1–5 (เป้าหมาย Sprint 3: ≥ 3.5)<br>3. บันทึกสูตรคำนวณ PMI ใน `docs/metrics/QUALITY_METRICS.md` |
| **BNET-604** | *As QA, I need automated regression tests for every component so quality doesn't degrade between sprints.* | 5 | 1. pytest test suite ครอบคลุม: TTP, Firewall, DAFT, ML<br>2. Test Coverage ≥ 80%<br>3. CI/CD Pipeline (GitHub Actions) รัน tests อัตโนมัติทุก Push |

---

### ⚖️ Epic 7: Ethics, Regulations & Governance (Owner: โอเล่)

| Ticket | User Story | Story Points | Acceptance Criteria (AC) |
|--------|------------|--------------|--------------------------|
| **BNET-701** | *As an ethics lead, I need to formalize Brain-Net compliance against international neuroethics regulations.* | 5 | 1. เอกสาร Ethics Compliance Matrix เทียบกับ:<br>   - UNESCO Recommendation on AI Ethics (2021)<br>   - Neurorights Foundation Framework<br>   - GDPR (สำหรับ Neural Data)<br>2. ระบุ Compliant / Non-Compliant / Partial ต่อแต่ละกฎ<br>3. แผนแก้ไขส่วนที่ Non-Compliant |
| **BNET-702** | *As an auditor, I need automated Ethics Rule Engine that enforces Cognitive Liberty rules in real-time.* | 8 | 1. คลาส `EthicsRuleEngine` ที่ประเมิน packet ทุกชิ้นก่อนส่ง:<br>   - ตรวจสอบ Consent Score<br>   - ตรวจสอบ Private Thought Boundary<br>   - ตรวจสอบ Coercion Indicators<br>2. คืนค่า `EthicsDecision(ALLOW / BLOCK / QUARANTINE)`<br>3. เชื่อมต่อกับ Brain Firewall อัตโนมัติ (ไม่ต้อง Manual) |
| **BNET-703** | *As a regulator, I need an immutable Ethics Audit Log that cannot be tampered with.* | 3 | 1. ระบบ Logging เก็บเฉพาะ: Timestamp, Decision, Rule ID, Domain<br>2. Log ใช้ Hash Chain เพื่อป้องกันการแก้ไขย้อนหลัง<br>3. ไม่มี Neural Payload อยู่ใน Log ไม่ว่ากรณีใด |
| **BNET-704** | *As a governance committee, I need a formal Data Governance Policy for all neural data collected.* | 3 | 1. เอกสาร Neural Data Governance Policy v1.0<br>2. กำหนด: Retention Period (0 วัน / ลบทันที), Access Rights, Anonymization<br>3. ลงนามโดย Neuroethics Lead และ Network Architect |

---

### 🤝 Epic 8: Human-in-the-Loop (HITL) Governance (Owner: รักบี้ + โอเล่)

| Ticket | User Story | Story Points | Acceptance Criteria (AC) |
|--------|------------|--------------|--------------------------|
| **BNET-801** | *As a safety officer, I need a HITL Checkpoint system that pauses transmission and alerts a human operator when anomalies are detected.* | 8 | 1. โมดูล `HITLCheckpoint` ตรวจจับ Trigger Events:<br>   - Arousal > 0.9 (Panic State)<br>   - Consent Score < 0.3<br>   - Repeated Semantic Injection Attempts ≥ 3 ครั้ง<br>2. ส่ง Alert (Console + Log) ภายใน 500ms<br>3. หยุด TTP Stream อัตโนมัติ (Hard Stop) ระหว่างรอคำตัดสินจาก Operator<br>4. มี Manual Override Command สำหรับ Operator ตัดสินใจ Resume/Abort |
| **BNET-802** | *As an operator, I need a HITL Dashboard (CLI-based) that shows real-time system status and lets me intervene.* | 5 | 1. CLI Dashboard แสดง: Latency, Active Sessions, Ethics Violations, HITL Queue<br>2. Commands: `resume <session_id>`, `abort <session_id>`, `inspect <packet_id>`<br>3. รีเฟรชทุก 1 วินาที<br>4. Log การตัดสินใจของ Operator ทุกครั้ง |
| **BNET-803** | *As a researcher, I need HITL intervention data to analyze system behavior patterns.* | 3 | 1. เก็บ HITL Event Log: Trigger Type, Response Time, Operator Decision<br>2. สรุป HITL Statistics Report ต่อ Session<br>3. คำนวณ HITL Intervention Rate (เป้าหมาย < 5% ของ Sessions) |

---

## 📅 4. Day-by-Day Execution Plan (20-Day Roadmap)

### 🗓️ Week 9: Domain Mapping Foundation & DAFT Architecture

**Goal ของสัปดาห์:** วางโครงสร้าง DAFT และนิยาม Math Formalization ของทุกโดเมน พร้อมแก้ ISS-002

| Day | Focus Area | Owner(s) | Daily Inputs | Detailed Daily Tasks | Daily Outputs |
|-----|-----------|----------|-------------|---------------------|---------------|
| **Day 1** (Mon) | **Sprint 3 Kick-off & Issue Review** | All | Sprint 2 Retrospective Report | 1. ประชุม Sprint 3 Planning (1 ชม.) รีวิว Issues 001–006<br>2. เปิดตั๋ว Tickets ใน Board (BNET-501 ถึง BNET-803)<br>3. เจม ร่าง Domain Interface Architecture บนกระดาน<br>4. โอเล่ เตรียม Regulatory Research List | - Sprint 3 Board พร้อม Tickets ครบ<br>- Draft Domain Architecture Diagram |
| **Day 2** (Tue) | **Bio & Physical Domain Math Formalization** | บี, เจม | Physics/Biology Signal Theory | 1. **บี:** นิยาม Neural Firing Rate → Frequency Vector สำหรับ Bio Domain<br>2. **เจม:** นิยาม EEG Amplitude → Normalized Tensor สำหรับ Physical Domain<br>3. ทั้งคู่ร่างสูตรเป็น LaTeX | - เอกสาร Math Formalization: Bio & Phy Domain v0.1<br>- Draft สูตร `f ∈ ℝⁿ` และ `T ∈ [0,1]^{d×t}` |
| **Day 3** (Wed) | **Neuro & Quantum Domain Math Formalization** | บี, โยรุ | Quantum State Theory + Neuro Signals | 1. **บี:** นิยาม Cognitive State → Discrete Symbol Set `S`<br>2. **โยรุ:** นิยาม Quantum Entanglement State → Complex Vector `|ψ⟩`<br>3. โอเล่ ตรวจทานว่านิยามไม่ละเมิด Cognitive Liberty | - เอกสาร Math Formalization: Neuro & Quantum Domain v0.1<br>- Ethics Sign-off บน Neuro Symbol Set |
| **Day 4** (Thu) | **DomainInterface Class Coding** | เจม, บี | Math Formalization Docs (Day 2–3) | 1. เขียนคลาส `DomainInterface` ด้วย 4 mappers<br>2. เขียน `MathSymbol` data class<br>3. เขียน Unit Tests สำหรับแต่ละ Domain | - `src/daft/domain_interface.py` ผ่าน Unit Test ≥ 90%<br>- Code Review จาก รักบี้ |
| **Day 5** (Fri) | **DAFT Validator Architecture & Week 9 Sync** | เจม, All | DomainInterface Code | 1. เจม ออกแบบ `DAFTValidator` Architecture<br>2. ทีม Review Domain Formalization ทั้งหมด<br>3. อัปเดต `docs/planning/` ด้วย Progress Week 9 | - DAFT Validator Design Document<br>- Week 9 Progress Report |

---

### 🗓️ Week 10: DAFT Validation Engine & ML Improvement

**Goal ของสัปดาห์:** สร้าง DAFT Validator ให้สมบูรณ์ แก้ ISS-001 (ML Accuracy < 80%) ด้วยข้อมูลครบ 4 โดเมน

| Day | Focus Area | Owner(s) | Daily Inputs | Detailed Daily Tasks | Daily Outputs |
|-----|-----------|----------|-------------|---------------------|---------------|
| **Day 6** (Mon) | **DAFT Validator Implementation** | เจม | DAFT Architecture Doc | 1. โค้ด `DAFTValidator` class ทั้งหมด<br>2. Range Check, Dimension Check, Consent Check<br>3. Integration Test กับ TTPRouter | - `src/daft/daft_validator.py` สมบูรณ์<br>- Integration Test ผ่าน TTPRouter |
| **Day 7** (Tue) | **Round-trip Consistency Test** | เจม, บี | DAFTValidator Code | 1. เขียนสคริปต์ทดสอบ Round-trip ทุกโดเมน<br>2. คำนวณ Cosine Similarity<br>3. บันทึก Domain Consistency Report | - ผล Round-trip Test (เป้า Similarity ≥ 0.95)<br>- `docs/metrics/domain_consistency_report.md` |
| **Day 8** (Wed) | **Multi-Domain ML Data Preparation** | บี | EEG Dataset + Domain Definitions | 1. รวบรวม Dataset ครบ 4 โดเมน (Bio/Phy/Neuro/Quantum Sim)<br>2. Normalize ข้อมูลแต่ละโดเมนให้เป็น Feature Vector เดียวกัน<br>3. Label ข้อมูลใหม่: 4 Classes per Domain | - `data/multi_domain_dataset.csv` พร้อม Labels<br>- Data Preprocessing Report |
| **Day 9** (Thu) | **ML Model Retraining (v2)** | บี | Multi-Domain Dataset | 1. เทรน Model v2 ด้วย 4-Domain Data<br>2. Cross-Validation และ Hyperparameter Tuning<br>3. วัด Accuracy per Domain | - `models/neural_dict_v2.pkl` <br>- Accuracy Report (เป้า ≥ 85%) |
| **Day 10** (Fri) | **Mid-Sprint Demo & DAFT Integration Test** | All | DAFT + ML v2 | 1. รัน Pipeline ทดสอบ: Domain Input → DAFT → TTP → Firewall<br>2. วัด Latency รวม (เป้า < 50ms)<br>3. ถกปัญหา Blockers | - Demo Video (Internal)<br>- Blocker List สำหรับ Week 11 |

---

### 🗓️ Week 11: Ethics Engine, Regulations & HITL System

**Goal ของสัปดาห์:** สร้าง Ethics Rule Engine แบบ Automated พร้อม HITL Checkpoint ที่สมบูรณ์

| Day | Focus Area | Owner(s) | Daily Inputs | Detailed Daily Tasks | Daily Outputs |
|-----|-----------|----------|-------------|---------------------|---------------|
| **Day 11** (Mon) | **Regulatory Compliance Mapping** | โอเล่ | UNESCO AI Ethics, Neurorights, GDPR | 1. วิเคราะห์ Brain-Net vs กฎระเบียบ 3 ฉบับ<br>2. กรอก Ethics Compliance Matrix<br>3. ระบุ Action Items สำหรับส่วนที่ Non-Compliant | - `docs/ethics/COMPLIANCE_MATRIX.md` ฉบับสมบูรณ์<br>- Action Item List สำหรับทีม |
| **Day 12** (Tue) | **Ethics Rule Engine Development** | โอเล่, รักบี้ | Cognitive Liberty Rules v1.0 + Compliance Matrix | 1. โอเล่ แปลงกฎจริยธรรมเป็น If-Else Logic<br>2. รักบี้ โค้ด `EthicsRuleEngine` class<br>3. เชื่อมต่อกับ Brain Firewall | - `src/security/ethics_rule_engine.py`<br>- Unit Test ผ่านทุก Rule |
| **Day 13** (Wed) | **Immutable Audit Log System** | โอเล่, โยรุ | Ethics Engine | 1. โยรุ ออกแบบ Hash Chain สำหรับ Audit Log<br>2. โอเล่ กำหนด Log Schema (ไม่มี Payload)<br>3. ทดสอบว่า Log ไม่สามารถแก้ไขได้ | - `src/security/audit_log.py` ด้วย Hash Chain<br>- Tamper-Detection Test ผ่าน |
| **Day 14** (Thu) | **HITL Checkpoint System** | รักบี้ | Ethics Engine + Trigger Conditions | 1. โค้ด `HITLCheckpoint` module<br>2. ตั้ง Trigger Rules (Arousal > 0.9, Consent < 0.3, ฯลฯ)<br>3. ทดสอบ Hard Stop และ Manual Resume | - `src/security/hitl_checkpoint.py`<br>- HITL Test: Hard Stop ใน < 500ms |
| **Day 15** (Fri) | **HITL Dashboard (CLI) & Ethics Freeze** | รักบี้, โอเล่ | HITL Checkpoint + Ethics Engine | 1. โค้ด CLI Dashboard (real-time display)<br>2. เพิ่ม Operator Commands: resume/abort/inspect<br>3. โอเล่ ตรวจ Ethics ภาพรวม Week 11<br>4. **Ethics Freeze ชั่วคราว:** ห้ามแก้ Logic จริยธรรมโดยไม่แจ้ง | - `src/dashboard/hitl_cli.py`<br>- Ethics Checkpoint Report |

---

### 🗓️ Week 12: Quality Metrics, Testing & Sprint 3 Delivery

**Goal ของสัปดาห์:** ประกอบ Quality Dashboard ให้สมบูรณ์ เขียน Regression Tests ครบ และส่งมอบ Sprint 3

| Day | Focus Area | Owner(s) | Daily Inputs | Detailed Daily Tasks | Daily Outputs |
|-----|-----------|----------|-------------|---------------------|---------------|
| **Day 16** (Mon) | **Quality Dashboard Implementation** | เจม, บี | System Metrics Data | 1. โค้ด `quality_metrics.py` รวบรวม Metrics ทั้งหมด<br>2. คำนวณ Protocol Maturity Index (PMI)<br>3. Export JSON และ Markdown | - `src/metrics/quality_metrics.py`<br>- ผล PMI Score (เป้า ≥ 3.5) |
| **Day 17** (Tue) | **Automated Regression Test Suite** | All | Codebase Sprint 3 | 1. เขียน pytest ครอบคลุม DAFT, ML, Firewall, HITL<br>2. Setup GitHub Actions Workflow<br>3. วัด Test Coverage | - `tests/` ครบถ้วน<br>- GitHub Actions CI/CD ผ่าน<br>- Coverage ≥ 80% |
| **Day 18** (Wed) | **Bug Bash & Full Pipeline Test** | All | Integrated System | 1. Bug Bash: ทุกคนสลับบทบาทหาบั๊ก<br>2. รัน Full E2E Pipeline: Domain Input → DAFT → ML → TTP → Firewall → HITL → Output<br>3. วัด Latency ทุก Stage | - Bug List (เป้า 0 Critical)<br>- E2E Pipeline Report พร้อม Latency Breakdown |
| **Day 19** (Thu) | **Documentation & Data Governance** | โอเล่, All | Code Freeze Version | 1. โอเล่ เขียน Neural Data Governance Policy v1.0<br>2. อัปเดต `docs/` ทุกไฟล์<br>3. อัปเดต CHANGELOG.md ด้วยสรุป Sprint 3 | - `docs/ethics/DATA_GOVERNANCE.md`<br>- `CHANGELOG.md` อัปเดต Sprint 3 |
| **Day 20** (Fri) | **Sprint 3 Review & Retrospective** | All | ชิ้นงานทั้งหมด | 1. Sprint Review (1 ชม.): Demo ทุก Epic 5–8<br>2. Retrospective (45 นาที)<br>3. วางแผน Sprint 4 Backlog เบื้องต้น | - **Sprint 3 Delivery Package** (ZIP/Repo Tag: `v3.0`)<br>- Sprint 4 Initial Backlog |

---

## ⚙️ 5. Agile Ceremonies

| Ceremony | Schedule | Duration | Agenda |
|----------|----------|----------|--------|
| **Daily Standup** | ทุกวัน 10:00 AM | 15 นาที | งานวานนี้ / แผนวันนี้ / Blocker |
| **Backlog Grooming** | พุธ 2:00 PM | 45 นาที | รีวิว Tickets Week ถัดไป, ปรับ Story Points |
| **HITL Protocol Review** | อังคาร & พฤหัส 4:00 PM | 30 นาที | รักบี้ + โอเล่ ทบทวนเหตุการณ์ HITL |
| **Ethics Standing Meeting** | ทุกศุกร์ 3:00 PM | 30 นาที | โอเล่ รายงาน Ethics Status ให้ทีม |
| **Sprint Review** | Day 20, 1:00 PM | 60 นาที | Demo ทุก Epic, รับ Feedback |
| **Retrospective** | Day 20, 2:30 PM | 45 นาที | Start / Stop / Continue |

---

## ⛓️ 6. Definition of Done (DoD) — Sprint 3

ตั๋วจะถือว่า "Done" เมื่อผ่านทุกข้อต่อไปนี้:

1. ✅ **Build Passes:** ไม่มี Fatal Error / Syntax Error
2. ✅ **Peer Reviewed:** ถูกตรวจโดยสมาชิกอื่นอย่างน้อย 1 คน (Cross-role)
3. ✅ **DAFT Validated:** ข้อมูลที่ประมวลผลผ่าน `DAFTValidator` แล้ว
4. ✅ **Ethics Cleared:** โอเล่ (Neuroethics Lead) ยืนยันว่าไม่ละเมิด Cognitive Liberty
5. ✅ **Quality Metric Recorded:** บันทึก Metric เข้า Quality Dashboard
6. ✅ **Test Covered:** มี pytest ครอบคลุม ≥ 80%
7. ✅ **Documented:** อัปเดต Docstring และ Markdown Docs

---

## 🚨 7. Sprint 3 Risk Register

| Risk | Probability | Severity | Mitigation |
|------|-------------|----------|------------|
| ML v2 ยังไม่แม่นยำ ≥ 85% แม้ใช้ Multi-Domain Data | กลาง | วิกฤต | ลดโดเมนเหลือ 2 (Neuro + Bio) ก่อน แล้ว Expand ใน Sprint 4 |
| DAFT Validation ทำให้ Latency รวมเกิน 50ms | สูง | วิกฤต | ปรับ DAFT ให้ทำงานแบบ Async / ใช้ Caching สำหรับ Repeated Patterns |
| Ethics Rule Engine ขัดแย้งกับ Brain Firewall Rules เดิม | กลาง | สูง | จัด Sync Meeting เฉพาะกิจ รักบี้ + โอเล่ ทันทีที่พบปัญหา |
| HITL อาจ Interrupt Transmission บ่อยเกินไป (False Positive) | สูง | กลาง | Tune Threshold ก่อน Deploy; เริ่มที่ Arousal > 0.95 แล้วค่อยลดลง |
| ทีมไม่เข้าใจ Quantum Math Formalization (`|ψ⟩`) | ต่ำ | กลาง | โยรุ จัดทำ Tutorial สั้น 30 นาที ใน Week 9 Day 1 |

---

## 📊 8. Sprint 3 Success Metrics (Definition of Sprint Done)

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **DAFT Validation Pass Rate** | ≥ 95% | `DAFTValidator` statistics |
| **Domain Round-trip Similarity** | ≥ 0.95 Cosine | Round-trip Test Script |
| **ML Classifier Accuracy** | ≥ 85% | Holdout Test Set |
| **E2E Latency (incl. DAFT)** | < 50ms | Benchmark Script |
| **Protocol Maturity Index (PMI)** | ≥ 3.5 / 5.0 | `quality_metrics.py` |
| **Ethics Compliance** | ≥ 80% Rules Covered | Ethics Compliance Matrix |
| **HITL Response Time** | < 500ms | HITL Checkpoint Log |
| **HITL Intervention Rate** | < 5% of sessions | HITL Statistics Report |
| **Test Coverage** | ≥ 80% | pytest coverage report |
| **Critical Bugs** | 0 | Bug Bash Report |

---

## 🏷️ 9. GitHub Labels & Branch Naming (Sprint 3)

**Labels ใน Issues:**
- `sprint-3` — ตั๋วทุกใบใน Sprint 3
- `epic-5-daft` — งาน Domain Mapping & DAFT
- `epic-6-metrics` — งาน Quality Metrics
- `epic-7-ethics` — งาน Ethics & Regulations
- `epic-8-hitl` — งาน HITL Governance
- `bug` — บั๊กที่ต้องแก้
- `ethics-review-required` — ต้องผ่าน Neuroethics Lead ก่อน Merge

**Branch Naming:**
```
feat/BNET-501-domain-interface
feat/BNET-503-daft-validator
feat/BNET-602-ml-v2-training
feat/BNET-702-ethics-rule-engine
feat/BNET-801-hitl-checkpoint
fix/ISS-001-ml-accuracy
fix/ISS-006-quantum-overhead
```

---

*Brain-Net Sprint 3 — "Deep Calibration" | สร้างโดย Brain-Net Project Team*
