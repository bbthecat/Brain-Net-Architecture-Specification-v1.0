# 🧠 Brain-Net Sprint Execution Plan — Sprint 2: "Signal Bridge"
**Protocol Integration, ML Accuracy & Full E2E Pipeline**

---

## 📌 1. Executive Sprint Summary & Directives

| Attribute | Detail |
|-----------|--------|
| **Sprint Name** | BNET-Sprint-02: "Signal Bridge" |
| **Sprint Duration** | 4 Weeks (20 Working Days: Week 5–8) |
| **Sprint Theme** | ต่อท่อ (Bridge) ทุก Component จาก Sprint 1 ให้ทำงานร่วมกันได้อย่างสมบูรณ์ |
| **Primary Goal** | สร้าง Full E2E Pipeline ที่รัน Node A → Node B ได้โดยไม่ Crash รวมถึง TTP, Firewall, Encryption และ Consensual Handshake ทำงานเป็นระบบเดียว |
| **Secondary Goal** | ยกระดับ ML Accuracy ให้ถึง ≥ 80% (แก้ ISS-001) และลด Quantum Overhead ให้ต่ำกว่า 15ms (แก้ ISS-006) |
| **Sprint Velocity (Target)** | 52 Story Points |
| **Sprint Start** | Week 5 Day 1 |
| **Sprint End** | Week 8 Day 20 |

---

## 🧩 2. Context: สิ่งที่สร้างมาจาก Sprint 1

**Sprint 2 เริ่มต้นด้วย Codebase จาก Sprint 1:**

| Component | สถานะ | หมายเหตุ |
|-----------|-------|----------|
| `connect_bci.py` | ✅ Done | รันได้ แต่ยังเป็น Mock Data |
| `clean_eeg_data.py` | ✅ Done | Bandpass Filter พร้อม |
| `neural_dict_v1.pkl` | ⚠️ Partial | Accuracy 78% (ต้องแก้ ISS-001) |
| `TTPHeader`, `TTPPacket`, `TTPRouter` | ✅ Done | โค้ดสมบูรณ์ |
| `ContextFrame` | ✅ Done | Valence/Arousal แนบได้แล้ว |
| `virtual_network.py` | ✅ Done | 3-Node Simulator พร้อม |
| `BrainFirewall` | ✅ Done | ยังแยกจาก TTP (ต่อท่อ Sprint 2) |
| `mock_qkd_aes.py` | ⚠️ Partial | Overhead 18ms (ต้องแก้ ISS-006) |
| `BrainFirewall ↔ TTPRouter` Integration | ❌ Missing | **Sprint 2 งานหลัก** |
| `Consensual Handshake Protocol` | ❌ Missing | **Sprint 2 งานใหม่** |
| `2-Node E2E Simulator` | ❌ Missing | **Sprint 2 งานใหม่** |

---

## 🎯 3. Sprint 2 Backlog & Acceptance Criteria

### 🔗 Epic 2B: TTP Full Integration & 2-Node Simulator (Owner: เจม)

> ใน Sprint 1 เจมสร้าง TTP แต่ละส่วนแยกกัน Sprint 2 ต้องต่อท่อทั้งหมดให้ทำงานร่วมกันในสภาพแวดล้อม 2-Node จริง

| Ticket | User Story | Story Points | Acceptance Criteria (AC) |
|--------|------------|--------------|--------------------------|
| **BNET-211** | *As an architect, I need the full TTP pipeline (Header → Framing → Router → Output) working end-to-end in a 2-node simulation.* | 8 | 1. ต่อท่อ: `TTPHeader → ContextFrame → TTPRouter → Node B`<br>2. ข้อมูลวิ่งจาก Node A ถึง Node B โดยไม่ Corrupt<br>3. Integration Test ผ่านทุก Scenario<br>4. Latency รวม (ยังไม่รวม Encryption) < 30ms |
| **BNET-212** | *As an engineer, I need the 2-Node simulator to support concurrent bi-directional communication.* | 5 | 1. Node A และ Node B สามารถส่ง-รับพร้อมกันได้ (Bi-directional)<br>2. ไม่มี Deadlock หรือ Race Condition<br>3. Log แสดง Direction ของ Packet ชัดเจน |
| **BNET-213** | *As a developer, I need a Packet Inspector tool to debug TTP packets in transit.* | 3 | 1. เครื่องมือ CLI แสดงเนื้อหา TTP Packet (ยกเว้น Private Payload)<br>2. แสดง: Timestamp, Node Path, Consent Score, Arousal Level<br>3. โอเล่ยืนยันว่าไม่แสดง Neural Payload |

**Epic 2B Total: 16 SP**

---

### 🔒 Epic 4B: Consensual Handshake & Full Security Integration (Owner: รักบี้)

> Sprint 1 มีกลไก Firewall แต่ยังขาด Consensual Handshake Protocol ที่เป็นระบบ Sprint 2 ต้องสร้างและต่อเข้ากับ TTP

| Ticket | User Story | Story Points | Acceptance Criteria (AC) |
|--------|------------|--------------|--------------------------|
| **BNET-411** | *As a security specialist, I need a full Consensual Handshake Protocol that establishes sessions based on subconscious-level authorization.* | 8 | 1. คลาส `ConsensualHandshake` ที่จัดการ Session State<br>2. รองรับ Handshake Rules C-001 ถึง C-004 ทั้งหมด:<br>   - C-001: Auto-Reject เมื่อ Panic State<br>   - C-002: Terminate เมื่อ Subconscious Dissent<br>   - C-003: Block & Log เมื่อ Coercion Marker<br>   - C-004: Establish เมื่อ Mutual Resonance<br>3. Unit Test ครอบคลุมทุก Rule<br>4. เชื่อมต่อกับ TTPRouter ก่อนเปิด Session |
| **BNET-412** | *As security, I need Brain Firewall fully integrated into the TTP pipeline — not running as a separate process.* | 5 | 1. `BrainFirewall` อยู่ใน Pipeline ระหว่าง `TTPRouter` และ Node B<br>2. ทุก Packet ต้องผ่าน Firewall ก่อนถึง Receiver<br>3. Block Packet โดยไม่ทำให้ Stream อื่น Crash<br>4. Integration Test: ส่ง 100 Packets, บาง Packets Stress สูง → ต้องถูก Block |
| **BNET-413** | *As an operator, I need a Soft-Disconnect protocol that gracefully terminates sessions without causing neural shock.* | 3 | 1. Teardown Warning ส่งก่อนตัด 3 วินาที<br>2. เคลียร์ Buffer และ State ทั้งหมดภายใน 10ms<br>3. ทดสอบ Abrupt Disconnect (ไฟดับ) → ระบบ Recover ได้ภายใน 30ms |

**Epic 4B Total: 16 SP**

---

### 🧠 Epic 3B: ML Accuracy Improvement (Owner: บี)

> แก้ ISS-001: ML Accuracy 78% ให้ถึง ≥ 80% และเชื่อมต่อ Real-time Output เข้ากับ TTP Pipeline

| Ticket | User Story | Story Points | Acceptance Criteria (AC) |
|--------|------------|--------------|--------------------------|
| **BNET-311** | *As an AI engineer, I need the ML Classifier to reach ≥ 80% accuracy on the 3-state classification task.* | 8 | 1. เทรนโมเดลใหม่ด้วย Data Augmentation หรือ Feature Engineering เพิ่มเติม<br>2. Accuracy ≥ 80% บน Holdout Test Set<br>3. Confusion Matrix ยืนยันว่า "Reject" Class แม่นยำที่สุด (เพราะ Safety Critical)<br>4. บันทึกโมเดลใหม่เป็น `neural_dict_v1_1.pkl` |
| **BNET-312** | *As an engineer, I need real-time ML inference connected directly to the TTP pipeline input.* | 5 | 1. สคริปต์ `neural_classifier.py` รัน Real-time loop<br>2. ผลลัพธ์ (Symbol ID) ส่งเข้า TTP ภายใน 10ms<br>3. รองรับ Streaming Input (ไม่ใช่ Batch)<br>4. Integration Test: ML Output วิ่งผ่าน TTP ถึง Node B ได้ |

**Epic 3B Total: 13 SP**

---

### ⚛️ Epic 4C: Quantum Encryption Optimization (Owner: โยรุ)

> แก้ ISS-006: Quantum Encryption Overhead 18ms ให้ต่ำกว่า 15ms และ Integrate เข้า Full Pipeline

| Ticket | User Story | Story Points | Acceptance Criteria (AC) |
|--------|------------|--------------|--------------------------|
| **BNET-421** | *As quantum specialist, I need to optimize the AES-256 Mock QKD to reduce overhead from 18ms to under 15ms.* | 5 | 1. Profile ส่วนที่ช้าที่สุดใน `mock_qkd_aes.py`<br>2. ปรับปรุงด้วย: Key Caching, Faster Padding, หรือ Selective Encryption (Header Only)<br>3. Overhead < 15ms ใน 100 รอบ Benchmark<br>4. รายงาน Optimization Strategy |
| **BNET-422** | *As quantum specialist, I need encryption fully integrated in the pipeline wrapping TTP packets.* | 3 | 1. Encryption หุ้ม `TTPPacket` ก่อนส่งออก Node A<br>2. Decryption เปิดที่ Node B ก่อนส่งเข้า Firewall<br>3. ทดสอบว่า Firewall อ่านค่า Consent ได้หลัง Decrypt |

**Epic 4C Total: 8 SP**

---

**Sprint 2 Total: 53 SP** *(เกิน Target เล็กน้อย — ตัดทิ้งได้ที่ BNET-213 หาก Velocity ไม่พอ)*

---

## 📅 4. Day-by-Day Execution Plan (20-Day Roadmap)

### 🗓️ Week 5: TTP Integration & Handshake Design (Integration Phase)

**Goal ของสัปดาห์:** ต่อท่อ TTP Pipeline ให้ครบและออกแบบ Consensual Handshake

| Day | Focus Area | Owner(s) | Daily Inputs | Detailed Daily Tasks | Daily Outputs |
|-----|-----------|----------|-------------|---------------------|---------------|
| **Day 1** (Mon) | **Sprint 2 Kick-off & Issue Review** | All | Sprint 1 Retrospective + ISS-001 ถึง 006 | 1. ประชุม Sprint 2 Planning (1 ชม.) — ทบทวน Known Issues<br>2. เปิดตั๋ว BNET-211 ถึง BNET-422<br>3. เจม วาง Integration Architecture ของ Sprint 2<br>4. รักบี้ ออกแบบ Consensual Handshake State Machine บนกระดาน | - Sprint 2 Board พร้อม Tickets ครบ<br>- Integration Architecture Diagram<br>- Handshake State Machine v0.1 |
| **Day 2** (Tue) | **TTP Pipeline Integration Start** | เจม | Sprint 1 Code: TTP + CFL + Router | 1. ต่อท่อ `TTPHeader → ContextFrame → TTPRouter`<br>2. เพิ่ม Timestamp ทุก Stage<br>3. รัน Integration Test เบื้องต้น | - Stage 1–3 ของ Pipeline ต่อกันได้<br>- Latency per Stage รู้แล้ว |
| **Day 3** (Wed) | **2-Node Simulator Setup** | เจม | TTP Pipeline | 1. ปรับ `virtual_network.py` จาก 3-Node เป็น 2-Node (Node A ↔ Node B)<br>2. เพิ่ม Bi-directional Support<br>3. ทดสอบ Concurrent Send/Receive | - 2-Node Simulator รัน Bi-directional ได้<br>- ไม่มี Deadlock |
| **Day 4** (Thu) | **Consensual Handshake Coding** | รักบี้ | Handshake State Machine | 1. เขียน `consensual_handshake.py` ทั้งหมด<br>2. Implement Rules C-001 ถึง C-004<br>3. Unit Test ทุก Rule | - `src/security/consensual_handshake.py` สมบูรณ์<br>- Unit Test ผ่านทุก Rule |
| **Day 5** (Fri) | **Week 5 Sync & Data Format Agreement** | All | Sprint 2 Progress | 1. ทีมประชุมตรวจ Interface: Data Format ระหว่าง ML Output / TTP Input / Firewall Input<br>2. กำหนด JSON/Struct spec ที่ทุกส่วนต้องใช้ร่วมกัน<br>3. โอเล่ตรวจสอบว่า Spec ไม่ละเมิด Privacy | - **Interface Contract Document v1.0**<br>- ทุกคนรู้ Format ที่ตัวเองต้องรับ-ส่ง |

---

### 🗓️ Week 6: ML Boost & Security Integration (Build & Fix Phase)

**Goal ของสัปดาห์:** แก้ ISS-001 (ML Accuracy) และต่อ Firewall + Handshake เข้า TTP Pipeline

| Day | Focus Area | Owner(s) | Daily Inputs | Detailed Daily Tasks | Daily Outputs |
|-----|-----------|----------|-------------|---------------------|---------------|
| **Day 6** (Mon) | **ML Data Augmentation** | บี | `clean_eeg_data.csv` + Interface Contract | 1. เพิ่ม Data Augmentation (Gaussian Noise, Time Shifting)<br>2. Feature Engineering เพิ่ม: Power Spectral Density, Band Power<br>3. เทรนโมเดลใหม่รอบแรก | - Dataset ขยายใหญ่ขึ้น<br>- โมเดลรอบแรก (เป้า > 78%) |
| **Day 7** (Tue) | **ML Hyperparameter Tuning Round 2** | บี | โมเดลรอบแรก | 1. Grid Search หา Hyperparameter ที่ดีที่สุด<br>2. วัด Accuracy per Class (Focus / Relax / Reject)<br>3. ยืนยัน Reject Class Accuracy สูงสุด | - โมเดล `neural_dict_v1_1.pkl`<br>- Accuracy ≥ 80% บน Holdout Set |
| **Day 8** (Wed) | **Firewall ↔ TTP Integration** | รักบี้, เจม | TTP Pipeline + BrainFirewall | 1. แทรก `BrainFirewall` เข้าใน Pipeline ระหว่าง TTPRouter และ Node B<br>2. ทดสอบ: ส่ง 50 Packets (30 Normal, 20 Stress=High)<br>3. ยืนยัน Stress Packets ถูก Block | - Firewall อยู่ใน Pipeline แล้ว<br>- Block Rate = 100% สำหรับ Stress Packets |
| **Day 9** (Thu) | **Handshake ↔ TTP Integration** | รักบี้, เจม | ConsensualHandshake + TTPRouter | 1. เพิ่ม Handshake ก่อนเปิด Session ใน TTPRouter<br>2. ทดสอบ C-001 (Panic) และ C-004 (Mutual Resonance)<br>3. วัด Handshake Overhead | - Handshake เปิด/ปิด Session ได้จริง<br>- Handshake Overhead < 5ms |
| **Day 10** (Fri) | **Mid-Sprint Demo & Integration Check** | All | Sprint 2 Pipeline ปัจจุบัน | 1. รัน Full Pipeline Demo: ML → TTP → Handshake → Firewall → Node B<br>2. วัด Latency รวม (ยังไม่รวม Encryption)<br>3. ถก Blockers | - Demo Video (Internal)<br>- Latency Breakdown Report<br>- Blocker List Week 7 |

---

### 🗓️ Week 7: Encryption Integration, Optimization & Full E2E (Sync Phase)

**Goal ของสัปดาห์:** ต่อ Encryption เข้า Pipeline และรัน Full E2E ครั้งแรก

| Day | Focus Area | Owner(s) | Daily Inputs | Detailed Daily Tasks | Daily Outputs |
|-----|-----------|----------|-------------|---------------------|---------------|
| **Day 11** (Mon) | **Quantum Overhead Optimization** | โยรุ | `mock_qkd_aes.py` + Profiling Tools | 1. Profile ส่วนที่ช้าที่สุดใน AES-256<br>2. ทดสอบ Key Caching Strategy<br>3. ทดสอบ Header-Only Encryption (แทน Full Payload) | - Encryption Overhead < 15ms<br>- Optimization Strategy Report |
| **Day 12** (Tue) | **Encryption ↔ TTP Integration** | โยรุ, เจม | Optimized `mock_qkd_aes.py` + TTP Pipeline | 1. หุ้ม `TTPPacket` ด้วย Encryption ก่อนส่งออก Node A<br>2. Decrypt ที่ Node B ก่อนส่งเข้า Firewall<br>3. ทดสอบว่า Firewall อ่านค่า Consent ได้หลัง Decrypt | - Full Pipeline พร้อม Encryption<br>- Firewall อ่านข้อมูลได้ถูกต้อง |
| **Day 13** (Wed) | **ML Real-time Stream Integration** | บี, เจม | `neural_dict_v1_1.pkl` + TTP Pipeline | 1. เชื่อมต่อ Real-time ML Output เข้า TTP<br>2. ทดสอบ Latency: ML Inference → TTP Packet (เป้า < 10ms)<br>3. รัน Streaming Loop 60 วินาที ไม่มี Crash | - ML Output วิ่งเข้า TTP Real-time<br>- Streaming Loop Stable |
| **Day 14** (Thu) | **Full E2E Pipeline Run (First Complete)** | All | ทุก Component Sprint 2 | 1. รัน Full E2E ครั้งแรก: EEG → ML → TTP → Encrypt → Handshake → Firewall → Node B → Decrypt<br>2. วัด Total Latency<br>3. บันทึกทุก Error ที่พบ | - **Full E2E รันสำเร็จครั้งแรก**<br>- Total Latency Measurement<br>- Error Log |
| **Day 15** (Fri) | **Ethics Audit & Audit Log Upgrade** | โอเล่, All | Full E2E System | 1. โอเล่ตรวจสอบ Log ทั้งหมด: ไม่มี Payload รั่ว<br>2. ตรวจสอบว่า Consensual Handshake บันทึก Log ถูกต้อง<br>3. อัปเกรด Audit Log ให้ครอบคลุม Handshake Events | - Ethics Audit Sprint 2: PASSED<br>- Upgraded Audit Log |

---

### 🗓️ Week 8: Performance Tuning, Bug Bash & Delivery (Delivery Phase)

**Goal ของสัปดาห์:** ปรับ Performance ให้ผ่านทุก Metric เป้าหมาย และส่งมอบ Sprint 2

| Day | Focus Area | Owner(s) | Daily Inputs | Detailed Daily Tasks | Daily Outputs |
|-----|-----------|----------|-------------|---------------------|---------------|
| **Day 16** (Mon) | **Latency Profiling Full Pipeline** | เจม, All | Full E2E System | 1. Profile Latency ทุก Stage<br>2. ระบุ Top 3 Bottleneck<br>3. วางแผน Optimization | - Latency Breakdown: ทุก Stage<br>- Top 3 Bottleneck + Mitigation Plan |
| **Day 17** (Tue) | **Performance Optimization** | เจม, บี, โยรุ | Bottleneck Analysis | 1. เจม Optimize TTPRouter (เช่น Reduce Serialization)<br>2. บี Optimize ML Inference (Pre-load Model)<br>3. โยรุ Fine-tune Encryption (Session Key Reuse) | - Latency Improvement Report<br>- เป้า P95 < 70ms |
| **Day 18** (Wed) | **Bug Bash** | All | Full E2E Latest | 1. สลับบทบาทมาหาบั๊ก<br>2. บีทดลอง Replay Attack บน Handshake<br>3. โยรุทดสอบ Key Exchange Edge Cases<br>4. รักบี้ทดสอบ Session Hijacking Mock | - 0 Critical Bugs<br>- **Code Freeze** |
| **Day 19** (Thu) | **Documentation Sprint** | All | Code Freeze Version | 1. อัปเดต `README.md` ให้ครอบคลุม Sprint 2<br>2. เพิ่ม Docstring ทุก Class ที่สร้างใหม่<br>3. อัปเดต `CHANGELOG.md` ส่วน Sprint 2<br>4. สร้าง Sprint 2 Demo Video | - Docs สมบูรณ์<br>- Demo Video Sprint 2 |
| **Day 20** (Fri) | **Sprint Review & Retrospective** | All | ชิ้นงานทั้งหมด | 1. Sprint Review ให้ Instructor ฟัง<br>2. Demo Full E2E Pipeline: EEG → ML → TTP → Encrypt → Node B<br>3. Retrospective: สรุปประเด็นสำคัญ<br>4. เปิด Backlog Sprint 3 เบื้องต้น | - **Delivery ZIP/Repo Sprint 2**<br>- **Sprint 3 Initial Backlog**<br>- Retrospective Document |

---

## ⚙️ 5. Agile Ceremonies

| Ceremony | Schedule | Duration | Agenda |
|----------|----------|----------|--------|
| **Daily Standup** | ทุกวัน 10:00 AM | 15 นาที | งานวานนี้ / แผนวันนี้ / Blocker |
| **Backlog Grooming** | พุธ 2:00 PM | 45 นาที | รีวิว Tickets Week ถัดไป, ปรับ Story Points |
| **Integration Sync** | อังคาร & พฤหัส 4:00 PM | 30 นาที | เจม, บี, โยรุ, รักบี้ คุยเรื่อง Interface Contract ป้องกัน Format Mismatch |
| **Sprint Review** | Day 20, 1:00 PM | 60 นาที | Demo Full E2E Pipeline ให้ Instructor |
| **Retrospective** | Day 20, 2:30 PM | 45 นาที | Start / Stop / Continue + เปิด Sprint 3 Backlog |

---

## ⛓️ 6. Definition of Done (DoD) — Sprint 2

1. ✅ **Build Passes:** ไม่มี Fatal Errors / Syntax Errors
2. ✅ **Integration Test Passes:** ต่อท่อกับ Component อื่นแล้วไม่ Crash
3. ✅ **Peer Reviewed:** ถูกตรวจจาก Cross-role อย่างน้อย 1 คน
4. ✅ **Interface Contract Compliant:** ใช้ Data Format ตาม Interface Contract v1.0
5. ✅ **Ethics Cleared:** โอเล่ยืนยันว่า Component ไม่ละเมิด Privacy Boundary
6. ✅ **Documented:** Docstring และ Markdown Docs อัปเดตแล้ว
7. ✅ **Latency Respect:** Component ที่เพิ่มต้องไม่ทำให้ Total Latency เกิน 80ms

---

## 🚨 7. Sprint 2 Risk Register

| Risk | Probability | Severity | Mitigation |
|------|-------------|----------|------------|
| Interface Mismatch ระหว่าง ML Output และ TTP Input | สูง | วิกฤต | กำหนด Interface Contract Document ใน Day 5 Week 5 ก่อนเริ่มต่อท่อ |
| ML Accuracy ยังไม่ถึง 80% แม้ Augment Data แล้ว | กลาง | วิกฤต | Fallback: ลด Class เหลือ Binary (Focus/Not-Focus) เพื่อให้ผ่าน 80% ก่อน |
| Consensual Handshake เพิ่ม Latency เกิน 10ms | กลาง | สูง | ใช้ Async Handshake; Pre-compute Consent Score ก่อน Session เริ่ม |
| Firewall ใน Pipeline ทำให้ Performance ลดลงมาก | สูง | สูง | รัน Firewall บน Separate Thread; ใช้ Queue แทน Blocking Call |
| Encryption ยังคง Overhead > 15ms แม้ Optimize | กลาง | กลาง | ตัดสินใจใช้ Header-Only Encryption เป็น Sprint 2 Solution; Full Encryption ใน Sprint 3 |

---

## 📊 8. Sprint 2 Success Metrics

| Metric | Sprint 1 Result | Sprint 2 Target | Measurement Method |
|--------|-----------------|-----------------|-------------------|
| **ML Accuracy** | 78% | ≥ 80% | Holdout Test Set |
| **Full E2E Latency (P95)** | ~85ms | < 70ms | 100-round Benchmark |
| **Encryption Overhead** | 18ms | < 15ms | AES-256 Enc/Dec Timer |
| **Handshake Overhead** | N/A | < 5ms | Timestamp Log |
| **Firewall Block Accuracy** | ~90% | ≥ 99% | Simulated Stress Packets |
| **Ethics Audit** | PASSED | PASSED | โอเล่ Manual Audit |
| **Integration Test Pass Rate** | N/A | 100% | pytest Integration Suite |
| **No Memory Leak** | Unknown | VERIFIED | Stress Test 30 นาที |

---

## 🏷️ 9. Sprint 2 Deliverables Checklist

**New Code:**
- [ ] `src/security/consensual_handshake.py` — Full Handshake Protocol (C-001 ถึง C-004)
- [ ] `src/bci/neural_classifier.py` — Updated with Real-time Streaming
- [ ] `src/protocol/virtual_network.py` — Upgraded to 2-Node Bi-directional
- [ ] `src/protocol/packet_inspector.py` — CLI Debug Tool

**Updated Code:**
- [ ] `src/security/brain_firewall.py` — Integrated into TTP Pipeline
- [ ] `src/crypto/mock_qkd_aes.py` — Optimized (< 15ms overhead)
- [ ] `src/protocol/ttp_router.py` — Integrated with Handshake and Firewall

**Models:**
- [ ] `models/neural_dict_v1_1.pkl` — Improved Model (≥ 80% accuracy)

**Documents:**
- [ ] `docs/planning/INTERFACE_CONTRACT_V1.md` — Data Format Spec ระหว่าง Components
- [ ] `README.md` — Updated Sprint 2 results
- [ ] `CHANGELOG.md` — Sprint 2 entry

**Reports:**
- [ ] ML Accuracy Report v2 (Confusion Matrix + Per-Class Accuracy)
- [ ] Full E2E Latency Benchmark Report
- [ ] Encryption Optimization Report
- [ ] Ethics Audit Sprint 2: PASSED

**Media:**
- [ ] Sprint 2 Demo Video (Full E2E Pipeline Demo)

---

## 🔍 10. Known Issues → Sprint 3 Backlog (Post-Sprint 2)

| Issue ID | ปัญหาที่พบ | Priority | Owner ใน Sprint 3 |
|----------|----------|----------|-------------------|
| **ISS-001** | ML Accuracy ยังหยุดที่ 78–80% (ยังต่ำกว่าเป้า 85% ระยะยาว) | Critical | บี |
| **ISS-002** | TTP ยังไม่รองรับ Bio/Physical Domain inputs | High | เจม |
| **ISS-003** | ไม่มีตัวชี้วัด Quality Metrics / Protocol Maturity Index | High | All |
| **ISS-004** | Ethics Audit ยังเป็น Manual Process (ต้องทำให้ Automated) | High | โอเล่ |
| **ISS-005** | ไม่มีกลไก Human-in-the-Loop (HITL) สำหรับ Anomaly Detection | Critical | รักบี้ |
| **ISS-006** | Quantum Encryption Overhead ลดลงเหลือ 15ms แต่ยังต้องเพิ่มประสิทธิภาพ | Low | โยรุ |

---

*Brain-Net Sprint 2 — "Signal Bridge" | Brain-Net Project Team*
*Sprint Period: Week 5–8 (ต่อเนื่องจาก Sprint 1: 2026-03-23 onwards)*
