# 🧠 Brain-Net Sprint Execution Plan — Sprint 1: "First Whisper"
**Foundation & Synthetic Telepathy**

---

## 📌 1. Executive Sprint Summary & Directives

| Attribute | Detail |
|-----------|--------|
| **Sprint Name** | BNET-Sprint-01: "First Whisper" |
| **Sprint Duration** | 4 Weeks (20 Working Days: 2026-02-23 → 2026-03-20) |
| **Sprint Theme** | วางรากฐานระบบ Brain-Net ทั้งหมด พร้อม Mock E2E ครั้งแรก |
| **Primary Goal** | สร้างโครงประดิษฐ์เสมือน (Mock E2E) เพื่อทดสอบโปรโตคอลการส่งคลื่นสมองพื้นฐานภายใต้ Latency < 50ms และผ่านการรับรองจากฐานข้อมูลกฎจริยธรรม |
| **Secondary Goal** | ยืนยันว่า ML Classifier สามารถจำแนกคำสั่งพื้นฐาน (Basic States) จากข้อมูล EEG ได้ที่ความแม่นยำ > 80% |
| **Sprint Velocity (Target)** | 50 Story Points |
| **Sprint Start** | Week 1 Day 1 — 2026-02-23 |
| **Sprint End** | Week 4 Day 20 — 2026-03-20 |

---

## 🧩 2. Context: จุดเริ่มต้นของ Brain-Net

Sprint 1 คือจุดเริ่มต้นของโปรเจกต์ทั้งหมด ทีมได้รับ Architecture Specification v1.0 และ Implementation Plan v1.0 แล้ว และต้องนำแนวคิดทั้งหมดมาสร้างเป็นโค้ดจริงเป็นครั้งแรก

**สถานะก่อนเริ่ม Sprint 1:**
- ✅ Architecture Specification v1.0 อนุมัติแล้ว (Conditional Approval)
- ✅ Team Roles กำหนดแล้ว (RACI Matrix สมบูรณ์)
- ❌ GitHub Repository ยังไม่มี (ต้องสร้างใน Day 1)
- ❌ ยังไม่มีโค้ดใดๆ
- ❌ ยังไม่มีข้อมูล EEG
- ❌ ยังไม่มีโปรโตคอล TTP

---

## 🎯 3. Sprint 1 Backlog & Acceptance Criteria

### 🛡️ Epic 1: Neuroethics & Cognitive Boundaries (Owner: โอเล่)

| Ticket | User Story | Story Points | Acceptance Criteria (AC) |
|--------|------------|--------------|--------------------------|
| **BNET-101** | *As an ethicist, I need mathematical boundaries for "Private vs Shared Thoughts" so the system knows what is acceptable.* | 5 | 1. เอกสารนิยาม 5 ค่าตัวแปรหลัก (เช่น Arousal Threshold/Frequency)<br>2. สูตรสมการสำหรับคำนวณ Consent Score (0.0 – 1.0)<br>3. สรุปเป็น Rule Text หรือ JSON format |
| **BNET-102** | *As an auditor, I want a logging mechanism that records firewall blocks without keeping the original thought payload.* | 3 | 1. Log เก็บเฉพาะ Timestamp, Reason, และ User ID<br>2. ไม่มีข้อมูล Thought Payload ใน Log File ไม่ว่ากรณีใด |

**Epic 1 Total: 8 SP**

---

### 🌐 Epic 2: Thought Transfer Protocol (TTP) & Context (Owner: เจม)

| Ticket | User Story | Story Points | Acceptance Criteria (AC) |
|--------|------------|--------------|--------------------------|
| **BNET-201** | *As an architect, I need a detailed TTP Header structure to route symbolic logic.* | 5 | 1. ออกแบบคลาส `TTPHeader` ใน Python<br>2. รองรับขนาดข้อมูล Payload แบบ Dynamic<br>3. Unit Test ยืนยันว่า Header สร้าง-แยก (Parse) ได้ถูกต้อง |
| **BNET-202** | *As a network, I need a Contextual Framing Layer to append Emotional Vectors.* | 8 | 1. โมดูล `ContextFrame` ที่แนบค่า Valence (-1 ถึง 1) และ Arousal (0 ถึง 1)<br>2. การรวม (Assembly) กับ TTP ใช้เวลาน้อยกว่า 5ms |
| **BNET-203** | *As an engineer, I want a simulator tracking latency to prevent Neural Dissonance.* | 3 | 1. สคริปต์จำลอง Network Node 3 ตัว (Sender, Router, Receiver)<br>2. เครื่องมือจับเวลา Timestamp จากต้นทางสู่ปลายทาง (End-to-End) |

**Epic 2 Total: 16 SP**

---

### 🧠 Epic 3: BCI Dictionary & Translation (Owner: บี)

| Ticket | User Story | Story Points | Acceptance Criteria (AC) |
|--------|------------|--------------|--------------------------|
| **BNET-301** | *As a BCI engineer, I need to collect and clean baseline EEG data.* | 8 | 1. นำเข้าฐานข้อมูล EEG (เช่น PhysioNet/MIMIC)<br>2. สคริปต์ทำ Bandpass Filter ตัดย่านความถี่เกิน และนำ Artifacts (กระพริบตา/ขยับกราม) ออก |
| **BNET-302** | *As an AI, I need a Random Forest model to classify 3 basic states.* | 8 | 1. โมเดลจำแนกสถานะ: Focus, Relax, Reject<br>2. Cross-Validation Accuracy > 80%<br>3. โมเดลบันทึกเป็น `.pkl` พร้อมจำลองรันแบบ Real-time |

**Epic 3 Total: 16 SP**

---

### 🔒 Epic 4: Brain Firewall & Mock Quantum Security (Owner: รักบี้ & โยรุ)

| Ticket | User Story | Story Points | Acceptance Criteria (AC) |
|--------|------------|--------------|--------------------------|
| **BNET-401** | *As security, I need a Firewall evaluating BNET-101 rules in real-time.* | 8 | 1. คลาส `BrainFirewall` ที่ดักจับ TTP Stream<br>2. ตัด Connection (Return 403) หาก Consent Score ต่ำกว่าเกณฑ์ |
| **BNET-402** | *As quantum specialist, I want AES-256 mocking future QKD payload.* | 5 | 1. ฟังก์ชันเข้ารหัส/ถอดรหัสข้อมูล TTP<br>2. Overhead การเข้ารหัส/ถอดรหัสรวมกันไม่เกิน 15ms |
| **BNET-403** | *As a user, I need Soft-disconnect so abrupt network cuts don't shock my system.* | 5 | 1. โปรโตคอลส่งคำสั่งปิดเซสชันย้อนกลับ (Teardown Warning)<br>2. ยืนยันการเคลียร์ State เครือข่ายทั้งหมดภายใน 10ms |

**Epic 4 Total: 18 SP**

---

**Sprint 1 Total: 58 SP** *(Velocity เป้าหมาย 50 SP — ส่วนที่เกินเป็น Buffer สำหรับ BNET-302 ที่ซับซ้อน)*

---

## 📅 4. Day-by-Day Execution Plan (20-Day Roadmap)

### 🗓️ Week 1: Requirements, Ethics & Architecture Blueprint (Foundation Phase)

**Goal ของสัปดาห์:** กำหนดกฎกติกา โครงสร้างเบื้องต้น แจกจ่าย Software/Hardware และตีกรอบโครงสร้างของโปรโตคอลให้เสร็จ

| Day | Focus Area | Owner(s) | Daily Inputs | Detailed Daily Tasks | Daily Outputs |
|-----|-----------|----------|-------------|---------------------|---------------|
| **Day 1** (Mon) | **Sprint Kick-off & Tooling** | All | เอกสาร Project Scope | 1. ประชุมรับทราบ Sprint Goals (30 นาที)<br>2. Setup GitHub Repo, ตั้งสาขา (Branching Rules)<br>3. แบ่งตั๋วในบอร์ด (Assign Trello/Jira tickets)<br>4. ถกเถียงข้อจำกัดของ TCP/IP (Architect นำ) | - แจกจ่ายตั๋วครบทุกคน<br>- Dev Environment ของทุกคนพร้อม<br>- ร่างแนวคิดโปรโตคอลใหม่ 1 หน้า |
| **Day 2** (Tue) | **Cognitive Liberty Definition** | โอเล่ | ทฤษฎีประสาทจริยธรรม | 1. ร่างขอบเขต "จิตใต้สำนึกส่วนตัว" (Private Unconscious)<br>2. กำหนดเกณฑ์ Consent (การรับรู้ว่ากำลังส่งข้อมูล)<br>3. แยกแยะ "อารมณ์" สู่สาธารณะ vs "ความนึกคิด" ห้ามออก | - เอกสาร **Cognitive Liberty Rulebook v1.0**<br>- ส่งให้รักบี้ (Security) รีวิว |
| **Day 3** (Wed) | **BCI Hardware Setup & TTP Draft** | บี, เจม | Spec BCI ล่าสุด + Rulebook จากโอเล่ | **(บี):** เตรียมสคริปต์ดึง Data (Raw Stream) จาก Headset<br>**(เจม):** ออกแบบร่าง TTP Header Fields (Source, Dest, Timestamp, Symbol ID) | - สคริปต์ `connect_bci.py` รันสำเร็จ<br>- โครงสร้าง `TTPHeader` ร่างเสร็จสมบูรณ์ |
| **Day 4** (Thu) | **Firewall Threat Model & QKD** | รักบี้, โยรุ | TTP Draft ของเจม | **(รักบี้):** วาง Logic ของ Brain Firewall (ดัก Preamble อย่างไร)<br>**(โยรุ):** เลือก Library สำหรับ AES-256 (Mock QKD) และทดสอบ Latency เปล่า | - **Brain Threat Model** Document<br>- โครงร่างสคริปต์ `mock_qkd_aes.py` |
| **Day 5** (Fri) | **Week 1 Sync & Preamble Design** | All | ร่างงานของทั้ง 4 วัน | 1. ทีมประชุมเช็คความพร้อมสถาปัตยกรรม (1 ชม.)<br>2. เจมปรับแก้ TTP Header ให้สอดคล้องกับ Firewall และความจุ Encryption ของโยรุ | - **Preamble / TTP Architecture Blueprint** เสร็จสมบูรณ์<br>- ปิดตั๋ว Epic 1 และ 2 บางส่วน |

---

### 🗓️ Week 2: Core Routing & ML Baseline (Build Phase)

**Goal ของสัปดาห์:** บีเทรน AI ให้แยกแยะคลื่นสมองพื้นฐานสำเร็จ (Accuracy > 80%) และเจม-รักบี้ เขียนโค้ดกลไกของ Protocol & Firewall

| Day | Focus Area | Owner(s) | Daily Inputs | Detailed Daily Tasks | Daily Outputs |
|-----|-----------|----------|-------------|---------------------|---------------|
| **Day 6** (Mon) | **ML Feature Extraction** | บี | Raw Data จาก Day 3 | 1. เขียนสคริปต์ Bandpass Filter ขจัดคลื่นรบกวน (Artifacts)<br>2. วาง Label ข้อมูล: Focus, Relax, Reject (3 สถานะ) | - ไฟล์ `clean_eeg_data.csv`<br>- สคริปต์สกัด Feature พร้อมใช้งาน |
| **Day 7** (Tue) | **TTP Coding & Framing Rules** | เจม | Architecture Blueprint | 1. เขียนโค้ด Python สร้าง Class ของ Transmission Protocol<br>2. โค้ดส่วน Contextual Framing (ยัดค่าอารมณ์/ความเครียดใส่ Payload) | - คลาส `TTPRouter` และ `TTPPacket`<br>- Unit Test Pack/Unpack ผ่าน |
| **Day 8** (Wed) | **First ML Training & Firewall Sync** | บี, รักบี้ | Clean Data + Framing Rules | **(บี):** เทรนโมเดลแรก (Random Forest / SVM)<br>**(รักบี้):** เขียนโค้ด `BrainFirewall` ตรวจจับค่า Contextual — ถ้าเครียดสูง → Drop | - ML Accuracy Matrix (เป้าหมาย > 70%)<br>- โค้ด Firewall ฟิลเตอร์เบื้องต้น |
| **Day 9** (Thu) | **Hyperparameter Tuning** | บี | โมเดลจาก Day 8 | 1. ตัด Feature ที่กวนออก (Noise Reduction)<br>2. ปรับจูน Hyperparameter (เป้าหมาย 80–85%)<br>3. บันทึกโมเดลเป็น `.pkl` | - ไฟล์ `neural_dict_v1.pkl`<br>- Validation Report (โอเล่ยืนยันไม่แปลลึกเกิน) |
| **Day 10** (Fri) | **Mid-Sprint Demo** | All | Component ของ Week 2 | 1. บี รัน Live Classification ผ่านโมเดล<br>2. เจม โชว์การ Pack ข้อมูลเข้า TTP<br>3. ถก Bottleneck ที่พบ | - วิดีโอ Demo (Internal Build)<br>- Blocker List สำหรับ Week 3 |

---

### 🗓️ Week 3: Integration & Simulator Execution (Sync Phase)

**Goal ของสัปดาห์:** นำโค้ด ML, TTP, Encryption และ Firewall มาต่อเข้าด้วยกันเป็น Pipeline เดียวผ่าน Network Simulator

| Day | Focus Area | Owner(s) | Daily Inputs | Detailed Daily Tasks | Daily Outputs |
|-----|-----------|----------|-------------|---------------------|---------------|
| **Day 11** (Mon) | **Building the Network Simulator** | เจม | — | 1. สร้าง `virtual_network.py` จำลอง Node A และ Node B<br>2. ใส่ Fake Latency และ Packet Loss เพื่อจำลองสภาพจริง | - Simulator Environment รันปกติ (ยังไม่มีข้อมูล BCI) |
| **Day 12** (Tue) | **ML to TTP Pipeline (The Bridge)** | บี, เจม | โมเดล + Simulator | 1. นำผลลัพธ์ "Focus" / "Reject" จากโมเดล<br>2. ยัดเข้า Preamble ของ TTP และโยนเข้า Simulator | - Symbol Data วิ่งผ่าน Simulator สำเร็จครั้งแรก |
| **Day 13** (Wed) | **Quantum Fallback Integration** | โยรุ, เจม | TTP Pipeline | 1. โยรุนำคลาสเข้ารหัสมาหุ้ม `TTPPacket`<br>2. วัด Overhead การเข้ารหัส/ถอดรหัส | - ข้อมูลเข้ารหัสตอนวิ่งข้ามโหนด<br>- Logs บันทึก Latency Overhead |
| **Day 14** (Thu) | **Firewall E2E Checks** | รักบี้, เจม | Encrypted Pipeline | 1. นำ `BrainFirewall` วางคั่นหน้า Node B (Receiver)<br>2. จำลองค่า Stress=High เพื่อทดสอบ Drop Packet | - Firewall บล็อคข้อมูลได้แม้เจอการเข้ารหัส<br>- Consensual Handshake ทำงานสมบูรณ์ |
| **Day 15** (Fri) | **Audit Logging & Ethics Freeze** | โอเล่ | E2E Version 0.9 | 1. โอเล่และรักบี้ตรวจสอบ Log ทั้งหมด<br>2. ยืนยันว่าไม่มี Payload ความคิดส่วนตัวใน Log | - **Audit Report: PASSED**<br>- Merge โค้ดลง Main Branch เตรียม Week 4 |

---

### 🗓️ Week 4: End-to-End Validation & Tuning (Delivery Phase)

**Goal ของสัปดาห์:** ปรับโค้ดให้เร็ว (เป้า < 50ms) ถ่ายทำวิดีโอ ยืนยันบั๊กให้หมด และ Package ส่งมอบ

| Day | Focus Area | Owner(s) | Daily Inputs | Detailed Daily Tasks | Daily Outputs |
|-----|-----------|----------|-------------|---------------------|---------------|
| **Day 16** (Mon) | **Stress Test & Soft Disconnects** | เจม, รักบี้ | E2E Version 0.9 | 1. รัวข้อมูลมหาศาล (Spam) จำลองสมองตื่นตระหนก<br>2. ทดสอบกลไก Soft Disconnect<br>3. ตรวจสอบ No Memory Leak | - Bug Report ส่วน Memory Leak |
| **Day 17** (Tue) | **Latency Profiling & Tuning** | ทีม Tech | Profiling Tools | 1. จับเวลาตั้งแต่สกัด ML จนถึง Node B<br>2. ตัด Process ที่ไม่จำเป็นออก (เป้า < 50ms) | - Benchmarking Report E2E Latency<br>- แนวทางแก้ไขหากไม่ถึงเป้า |
| **Day 18** (Wed) | **Bug Bash & Polish** | All | โค้ดล่าสุด | 1. วันนี้งดเขียนฟีเจอร์ใหม่ มารุมหาบั๊ก<br>2. บีทดลอง Hack Firewall / รักบี้เช็คช่องโหว่ Header | - 0 Critical Bugs, 0 High Bugs<br>- **Code Freeze** |
| **Day 19** (Thu) | **Documentation & Demo Prep** | โอเล่, โยรุ | Code Freeze Version | 1. อัปเดต `README.md`, คู่มือรัน Simulator<br>2. อัดวิดีโอรันโค้ด: ML (บี) → TTP (เจม) → Encrypt & Filter (โยรุ, รักบี้)<br>3. ยืนยันความบริสุทธิ์ของข้อมูล | - Demo Video พร้อมพรีเซนต์<br>- `requirements.txt` และ Docs สมบูรณ์ |
| **Day 20** (Fri) | **Sprint Review & Retrospective** | All | ชิ้นงานทั้งหมด | 1. Sprint Review ให้ Instructor ฟัง<br>2. นำเสนอสิ่งที่ทำได้ + สถิติ ML/Latency<br>3. Retrospective สรุปตลอด 4 สัปดาห์ | - **Delivery ZIP/Repo** ส่งมอบให้ Instructor<br>- **Action Items สำหรับ Sprint 2** |

---

## ⚙️ 5. Agile Ceremonies

| Ceremony | Schedule | Duration | Format & Agenda |
|----------|----------|----------|-----------------|
| **Daily Standup** | ทุกวัน 10:00 AM | 15 นาที | Discord Voice/Chat — อัปเดตงานวานนี้ / แผนวันนี้ / Blocker (กระชับ ไม่ถกเถียงลึก) |
| **Backlog Grooming** | พุธ 2:00 PM | 45 นาที | โหวตลด/เพิ่ม Story Points หรือหั่นงาน (Slice) ถ้ายากไป |
| **Integration Sync** | อังคาร & พฤหัส 4:00 PM | 30 นาที | เฉพาะทีม Dev คุยเรื่อง API/Data Format ที่จะส่งข้ามพาร์ต ป้องกันปัญหาต่อท่อไม่ติด |
| **Sprint Review** | Day 20, 1:00 PM | 60 นาที | Demo โค้ดรันจริงให้ PO/Instructor ดู (No Slides, Just Code/Results) |
| **Retrospective** | Day 20, 2:30 PM | 45 นาที | Start doing / Stop doing / Continue doing |

---

## ⛓️ 6. Definition of Done (DoD) — Sprint 1

1. ✅ **Build Passes:** ไม่มี Fatal Errors / Syntax Errors
2. ✅ **Peer Reviewed:** ถูกตรวจโค้ดหรือเอกสารจากเพื่อนร่วมทีม (Cross-role) อย่างน้อย 1 คน
3. ✅ **Documented:** ฟังก์ชันหรือคลาสมี Docstring หรือระบุวิธีใช้ใน Markdown
4. ✅ **Ethics Sign-off (ถ้าเกี่ยวกับ Data):** โอเล่อนุมัติกรอบการเก็บข้อมูลแล้ว
5. ✅ **Latency Respect:** โค้ดที่เพิ่มเข้ามาต้องไม่สร้าง Bottleneck หรือหน่วงเกินกว่าค่ารับได้

---

## 🚨 7. Sprint 1 Risk Register

| Risk | Probability | Severity | Mitigation |
|------|-------------|----------|------------|
| ML Accuracy ของบี ฝึกกี่รอบก็ไม่เกิน 60% (Noise เยอะมาก) | สูง | วิกฤต | ⚠️ ลด Target: กลับมาใช้ Binary (Yes/No) แทน 3 สถานะ เพื่อให้ผ่าน 80% ก่อน |
| เวลาเข้ารหัสของโยรุ ทำให้ Latency รวมทะลุ 100ms | กลาง | วิกฤต | ⚠️ เข้ารหัสแค่ `TTPHeader` แทน `Payload` หรือเปลี่ยนเป็น Hash จำลองชั่วคราว |
| ท่อคุยกันไม่ติด (เจม และ รักบี้ ประกอบ Firewall เข้า TTP ไม่ได้) | สูง | สูง | ⚠️ Pair Programming บังคับ: นั่งเขียนด้วยกันจนท่อต่อติด ห้ามทำแยกกันเด็ดขาด |
| นโยบาย Ethics ของโอเล่ มองไม่เห็นภาพในเชิงโค้ด | ต่ำ | กลาง | ⚠️ เจมจัดทำ Mock JSON ให้โอเล่ดู 1 ชุดว่า Firewall เห็นข้อมูลหน้าตาเป็นอย่างไร |

---

## 📊 8. Sprint 1 Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **ML Classifier Accuracy** | > 80% | Cross-Validation บน Clean EEG Data |
| **E2E Latency (Happy Path)** | < 50ms | Timestamp Log จาก Simulator |
| **Firewall Block Test** | PASS | จำลองค่า Stress สูง → ต้อง Drop |
| **Audit Log Privacy** | 0 Payload | ตรวจ Log File ไม่มี Neural Data |
| **Encryption Overhead** | ≤ 15ms | จับเวลา AES-256 Enc/Dec |
| **Soft Disconnect** | < 10ms | วัดเวลา Session Teardown |
| **Ethics Audit** | PASSED | โอเล่รับรองเป็นลายลักษณ์อักษร |

---

## 🏷️ 9. Sprint 1 Deliverables Checklist

**Code:**
- [ ] `src/bci/connect_bci.py` — BCI Connection Script
- [ ] `src/bci/clean_eeg_data.py` — EEG Preprocessing + Bandpass Filter
- [ ] `src/bci/neural_classifier.py` — Random Forest Classifier
- [ ] `src/protocol/ttp_packet.py` — TTPHeader, TTPPacket classes
- [ ] `src/protocol/ttp_router.py` — TTPRouter class
- [ ] `src/protocol/context_frame.py` — ContextFrame (Valence/Arousal)
- [ ] `src/protocol/virtual_network.py` — 3-Node Network Simulator
- [ ] `src/security/brain_firewall.py` — BrainFirewall class
- [ ] `src/crypto/mock_qkd_aes.py` — AES-256 Mock QKD

**Data & Models:**
- [ ] `data/clean_eeg_data.csv` — Cleaned EEG Dataset
- [ ] `models/neural_dict_v1.pkl` — Trained ML Model (Accuracy > 80%)

**Documentation:**
- [ ] `docs/ethics/COGNITIVE_LIBERTY.md` — Cognitive Liberty Rulebook v1.0
- [ ] `docs/architecture/ARCHITECTURE.md` — Updated post-Sprint 1
- [ ] `README.md` — Updated with Sprint 1 results
- [ ] `CHANGELOG.md` — Sprint 1 entry added

**Reports:**
- [ ] Brain Threat Model Document
- [ ] ML Validation Report (Accuracy + Confusion Matrix)
- [ ] E2E Latency Benchmark Report
- [ ] Ethics Audit Report: PASSED

**Media:**
- [ ] Sprint 1 Demo Video (Internal)

---

## 🔍 10. Known Issues → Sprint 2 Backlog

| Issue ID | ปัญหาที่พบ | Priority | Owner ใน Sprint 2 |
|----------|----------|----------|-------------------|
| **ISS-001** | ML Accuracy หยุดที่ 78% (ต่ำกว่าเป้า 80%) | Critical | บี |
| **ISS-002** | TTP ยังไม่รองรับ Bio/Physical Domain inputs | High | เจม |
| **ISS-003** | ไม่มีตัวชี้วัด Quality Metrics ที่เป็นทางการ | High | All |
| **ISS-004** | Ethics Audit ยังเป็น Manual Process | High | โอเล่ |
| **ISS-005** | ไม่มีกลไก Human-in-the-Loop (HITL) | Critical | รักบี้ |
| **ISS-006** | Quantum Encryption Overhead 18ms (เกินเป้า 15ms) | Medium | โยรุ |

---

*Brain-Net Sprint 1 — "First Whisper" | Brain-Net Project Team*
*Sprint Period: 2026-02-23 → 2026-03-20*
