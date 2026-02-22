# Brain-Net Project: Roles, Responsibilities & Boundaries Matrix
**Team Boundaries and Operational Framework - Phase 1 Foundation**

---

## 1. Team Role Assignment Table

| Role | Assigned To | Primary Responsibilities | Secondary Responsibilities | Decision Authority | Reporting To |
|------|-------------|-------------------------|---------------------------|-------------------|--------------|
| **Network Architect** | นายปฏิภาณ ปานทะเล (เจม) | • System-wide protocol design (TTP)<br>• Contextual Framing logic<br>• Project documentation | • Latency simulation<br>• Technical debt tracking<br>• Integration testing | • Protocol specifications<br>• Final architecture structure<br>• Network technology stack | Instructor |
| **BCI Engineer** | นายณัฐชา อรรคฮาต (บี) | • BCI Data acquisition<br>• ML Classifier for Neural Dictionary<br>• Hardware management | • Signal noise filtering<br>• Data struct optimization<br>• End-to-end integration | • Hardware selection<br>• ML algorithm approach<br>• Dictionary symbol rules | Network Architect |
| **Security Specialist**| นายอาณัฐ อารีย์ (รักบี้) | • Brain Firewall implementation<br>• Consensual Handshake logic<br>• Semantic Injection prevention | • Network simulator security checks<br>• Connection teardown logic<br>• Penetration testing (Mock) | • Firewall rule definitions<br>• Connection rejection bounds<br>• Security tech stack | Network Architect |
| **Neuroethics Lead** | นายรัชชานนท์ ประดับแก้ว (โอเล่) | • Cognitive Liberty framework<br>• Subconscious consent bounds<br>• Ethical compliance audit | • Incident/Leak investigation<br>• Privacy guidelines doc<br>• E2E User safety verification | • Final say on Privacy/Ethics<br>• Definition of "Private Thought"<br>• Audit approval/fail | Network Architect |
| **Quantum Specialist** | นายดรัณภพ สุริเตอร์ (โยรุ) | • Post-Quantum encryption design<br>• Classical-AI Fallback pipeline<br>• Quantum threat modeling | • Encryption latency profiling<br>• Key exchange simulation<br>• Mathematics documentation | • Encryption model choice<br>• Cryptographic fallback standard<br>• QKD simulation parameters | Network Architect |

*(Note: เนื่องจากทุกบทบาทเป็น Specialist ในส่วนที่แตกต่างกันอย่างสิ้นเชิง การตัดสินใจจึงขึ้นอยู่กับผู้เชี่ยวชาญใน Domain ของตนเองเป็นหลัก)*

---

## 2. Detailed Responsibility Matrix By Project Phase

| Phase | Network Architect | BCI Engineer | Security Specialist | Neuroethics Lead | Quantum Specialist |
|-------|-------------------|--------------|---------------------|------------------|--------------------|
| **Week 1: Foundation** | วิเคราะห์ข้อจำกัด TCP/IP<br>ประเมินโครงสร้างเครือข่าย | เลือก Hardware BCI<br>เตรียม Environment (Python) | ร่างสถาปัตยกรรม Brain Firewall<br>วิเคราะห์ Threat Model | สร้างกฎ Cognitive Liberty<br>นิยามพรมแดนความคิดส่วนตัว | ร่าง Post-Quantum Roadmap<br>เสนอ Classical Fallback |
| **Week 2: Implementation** | ร่าง TTP Header / Framing<br>จัดคู่มือ Architecture | เขียนสคริปต์เก็บข้อมูลคลื่นสมอง<br>จัดการ Noise (Artifacts) | โค้ด Inbound/Outbound Rules<br>ดีไซน์ Consensual Handshake | ตรวจทานโครงสร้างโปรโตคอล<br>ไม่ให้ละเมิดความเป็นส่วนตัว | พัฒนา Encryption Pipeline<br>สร้าง Mock Key Exchange |
| **Week 3: Integration** | สร้าง Network Simulator<br>เตรียมทดสอบการส่งข้อมูล TTP | Train AI สร้าง Neural Dictionary<br>ทดสอบความแม่นยำ (Acc) | ประสาน Firewall เข้าซิมูเลเตอร์<br>ทดสอบตัดเซสชันเมื่อเครียด | รับรอง Neural Dictionary<br>(ไม่เก็บข้อมูลเกินจำเป็น) | ผสานระบบเข้ารหัสลงใน TTP<br>ทดสอบ Encryption Latency |
| **Week 4: Delivery** | ประกอบร่าง End-to-End<br>Sign-off สถาปัตยกรรม | ปรับจูน ML ให้เร็วที่สุด<br>ทดสอบนำเข้า-ส่งออกคลื่นสมอง | รับรองระบบความปลอดภัยสมบูรณ์<br>ไม่มีข้อมูลรั่วไหลระหว่างรับส่ง | นำเสนอรายงาน Ethical Audit<br>Sign-off โปรเจกต์ด้านจริยธรรม | สรุปผลความหน่วงของการเข้ารหัส<br>นำเสนอแผนสู่อนาคต (QKD แท้) |

---

## 3. Responsibility Area Matrix By Component

| Component | Design Owner | Implementation Owner | Testing/Validation Owner | Ethics/Privacy Audit |
|-----------|--------------|----------------------|--------------------------|----------------------|
| **TTP (Thought Protocol)** | Architect | Architect | Architect + Security | Neuroethics Lead |
| **Neural Dictionary (ML)** | Engineer | Engineer | Engineer | Neuroethics Lead |
| **Brain Firewall** | Security | Security | Architect + Security | Neuroethics Lead |
| **Consensual Handshake** | Security | Security | Security + Engineer | Neuroethics Lead |
| **Contextual Framing (CFL)** | Architect | Architect + Engineer | Engineer | Neuroethics Lead |
| **Quantum Encryption Sim** | Quantum Spec. | Quantum Spec. | Quantum Spec. + Security | Network Architect |
| **Cognitive Liberty Rules**| Neuroethics Lead| (All Team Adheres) | Neuroethics Lead | Instructor |

---

## 4. Decision Authority Matrix

| Decision Type | Network Architect | BCI Engineer | Security Specialist | Neuroethics Lead | Quantum Spec. | Instructor |
|---------------|-------------------|--------------|---------------------|------------------|---------------|------------|
| Architecture / TTP changes| **Approve** | Consult | Consult | Consult | Consult | Final |
| BCI / ML Tech Selection | Consult | **Approve** | Consult | Consult | Consult | Review |
| Firewall / Reject Rules | Consult | Consult | **Approve** | Review | Consult | Review |
| Privacy Constraint Bounds | Review | Consult | Consult | **Approve** | Consult | Review |
| Cryptography Standards | Consult | Consult | Request | Consult | **Approve** | Review |
| Release Readiness (E2E) | **Propose** | Consult | Consult | **Approve** | Consult | **Final** |

---

## 5. Communication Boundaries (Internal Matrix)

| From \ To | Network Architect | BCI Engineer | Security Specialist | Neuroethics Lead | Quantum Spec. |
|-----------|-------------------|--------------|---------------------|------------------|---------------|
| **Architect** | - | ขอทราบ Payload Size จาก BCI<br>อัปเดตช่อง TTP | อัปเดตโครงสร้าง Header เพื่อประกอบ Firewall | ขอทราบข้อจำกัดทางจริยธรรมของ Metadata | หารือเรื่องตำแหน่งแทรง Encryption Payload |
| **Engineer** | ดีเลย์ของการแปลรหัส ML<br>ขอปรับโครงสร้างเฟรม | - | สอบถามจุดเชื่อมโยง (Handshake) ก่อนส่งข้อมูล ML | ขอตรวจสอบกรอบการจำแนกคลื่นสมอง | แจ้งปัญหา Latency หากเข้ารหัสหนักเกินไป |
| **Security** | แจ้งขอปรับโปรโตคอลถ้ามีช่องโหว่ | ขอทดสอบยิงสัญญาณที่เครียดจัด (Stress Test) | - | ขอเงื่อนไขและค่าน้ำหนักอารมณ์สำหรับบล็อก (Block) | ปรึกษาข้อจำกัดของการแทรกแซงกุญแจเข้ารหัส |
| **Ethics Lead** | สั่งปรับลดการส่งข้อมูล (ถ้าเกินจำเป็น) | สุ่มตรวจโมเดล AI ป้องกันละเมิดตัวตน | ขอรายงาน Audit Log การบล็อกของ Firewall | - | ตรวจสอบว่าระบบไม่เข้ารหัสซ่อนข้อมูลที่ผิดจริยธรรม |
| **Quantum** | ขอขนาด Packet เพื่อรับประกัน 50ms | ประชุมวิธีใส่รหัสในโมเดล ML ก่อนรวบ Packet | เสนอวิธีการเข้ารหัสแบบ Mock QKD | ชี้แจงขอบเขตการเข้ารหัสไม่ให้กระทบผู้ใช้ | - |

---

## 6. Escalation Path & Conflict Resolution

**Conflict Types and Resolution Limits:**
- *Accuracy vs. Privacy* (เช่น ML ขอเก็บยิบย่อย แต่ผิดจริยธรรม): ➡️ **Neuroethics Lead** มีอำนาจ VETO เด็ดขาด
- *Security vs. Latency* (เช่น เข้ารหัสหนาไปจนกระตุก): ➡️ **Network Architect** ชี้ขาดเพื่อรักษา <50ms

**Standard Escalation Flow:**
1. **Issue Discovery** (พบปัญหา/ความขัดแย้ง)
   ↓ *กรอบเวลาแก้ไขด้วยตัวเอง: 4 ชั่วโมง*
2. **Consult Associated Roles** (ปรึกษาบทบาทที่เกี่ยวข้องโดยตรง เช่น BCI คุยกับ Quantum)
   ↓ *กรอบเวลาหาข้อสรุป: 12 ชั่วโมง*
3. **Escalate to Network Architect** (ให้สถาปนิกหลักพิจารณาผลกระทบภาพรวม)
   ↓ *กรอบเวลาหาข้อสรุป: 1 วัน*
4. **Team Discussion / Ethics Revote** (โหวตทั้งทีม หรือเรียกใช้อำนาจ VETO ของ Ethics Lead)
   ↓ *กรอบเวลา: ทันทีในการประชุม*
5. **Escalate to Instructor** (หากไม่สามารถตกลงได้ โดยเฉพาะประเด็นความปลอดภัยของผู้ทดลอง)

---

## 7. Boundaries of Responsibility (In-Scope / Out-of-Scope)

### Network Architect (เจม)
- **In Scope:** จัดการ Flow โปรโตคอล TTP, จัดการ Contextual Framing, ประเมิน Latency, โครงสร้างระบบหลัก
- **Out of Scope:** เขียน ML Classifier, ออกแบบการเข้ารหัสวงใน, ตัดสินใจประเด็นจริยธรรมเด็ดขาด

### BCI Engineer (บี)
- **In Scope:** โค้ดดิ้ง ML/AI, นำเข้า Hardware ชุดตรวจจับ, ปรับแต่ง Neural Dictionary, สคริปต์รับคลื่นสมอง
- **Out of Scope:** กำหนดการเข้า-ออกของ Firewall, วางสถาปัตยกรรมเครือข่าย

### Security Specialist (รักบี้)
- **In Scope:** โค้ดดิ้ง Brain Firewall, สร้างกฎ Inbound/Outbound, ระบบ Handshake ระดับจิตใต้สำนึก
- **Out of Scope:** กำหนดหลักการเสรีภาพ (Liberty) เริ่มต้นวิจัยเรื่อง Quantum Encryption เชิงลึก

### Neuroethics Lead (โอเล่)
- **In Scope:** ระบุพรมแดนความคิดส่วนตัว, ออก Rule จริยธรรม, ร่างสมการประเมิน Consent, ออกใบ Audit Pass
- **Out of Scope:** เขียนโค้ดโปรโตคอลเครือข่าย, แก้บั๊กฮาร์ดแวร์/ML (เว้นแต่เป็นการแก้บั๊กละเมิดสิทธิ์)

### Quantum Specialist (โยรุ)
- **In Scope:** จัดสถาปัตยกรรมเข้ารหัส, Classical Fallback Pipeline, Threat pattern ในอนาคต
- **Out of Scope:** ยุ่งเกี่ยวกับ ML Neural Dictionary, โค้ดส่วนดักจับฮาร์ดแวร์

---

## 8. Overlap & Handoff Boundaries

| Handoff | From | To | Deliverable | Acceptance Criteria |
|---------|------|----|-------------|---------------------|
| **Ethics Policies → Ruleset** | Neuroethics | Security | Cognitive Liberty Rules v1 | กฎสามารถเขียนเป็น If-Else Logic ใน Firewall ได้ |
| **Neural Signals → Network** | BCI Engineer | Architect | Neural Dictionary DataFrame | ML โยนรหัสสัญลักษณ์ (Symbol ID) ได้ภายใน 10ms |
| **Protocol → Encryption** | Architect | Quantum Spec. | TTP Packets | Quantum Pipeline หุ้ม Packet และคืนค่า < 15ms |
| **Data Stream → Firewall** | Architect | Security | Inbound TTP Stream | Firewall อ่านค่า Consent / Arousal นำไป Drop ได้จริง |
| **Full Local Node → E2E Test**| All Team | E2E Simulator | Integrated Source Code | ไม่มี Crash เมื่อจำลอง Node A -> Node B แบบ Loop |

---

## 9. RACI Matrix (Brain-Net Implementation)

*(R = Responsible (ทำ), A = Accountable (มีอำนาจตัดสินใจเด็ดขาด), C = Consulted (ที่ปรึกษา), I = Informed (รับทราบ))*

| Activity | Architect | BCI Engineer | Security Spec. | Neuroethics Lead | Quantum Spec. |
|----------|-----------|--------------|----------------|------------------|---------------|
| Architecture/TTP Design | **R/A** | C | C | C | I |
| ML Neural Dictionary | I | **R/A** | I | C | I |
| Brain Firewall Logic | C | I | **R/A** | C | C |
| Cognitive Liberty Bounds| I | C | C | **R/A** | I |
| Encryption Fallback | C | I | C | I | **R/A** |
| Network Simulator Setup | **R** | C | C | I | C |
| End-to-End Latency Test | **R/A** | **R** | C | I | C |
| Ethical Compliance Audit| I | I | C | **R/A** | I |

---

## 10. Time Allocation Boundaries

| Role | Core Coding<br>(ML/TTP) | System Design<br>(Arch/Sim) | Rule/Doc Crafting<br>(Rules/Ethics) | Testing &<br>Validation | Sync &<br>Meeting |
|------|-------------|-------------|---------------------|-------------|----------|
| **Architect** | 25% | **45%** | 10% | 10% | 10% |
| **BCI Engineer**| **60%** | 10% | 5% | 20% | 5% |
| **Security** | **50%** | 15% | 10% | 15% | 10% |
| **Neuroethics** | 5% | 10% | **50%** | 25% | 10% |
| **Quantum Sec.**| **40%** | 20% | 20% | 10% | 10% |

*(เป้าหมายการทำงานเฉลี่ย: 8-10 ชั่วโมง / สัปดาห์)*

---

## 11. Sign-off Matrix

| Deliverable | Owner / Author | Reviewers | Final Approver (Accountable) |
|-------------|----------------|-----------|------------------------------|
| **Architecture Specification** | Network Architect | All Team | Instructor |
| **Implementation Plan** | Network Architect | All Team | Instructor / Team Consensus |
| **Cognitive Liberty framework**| Neuroethics Lead | Architect + Security| Neuroethics Lead |
| **Neural Dictionary & ML** | BCI Engineer | Neuroethics Lead | BCI Engineer |
| **Brain Firewall Rules** | Security Specialist | Ethics Lead + Architect| Security Specialist |
| **Post-Quantum Crypto Pipeline**| Quantum Specialist | Security Specialist | Quantum Specialist |
| **Final E2E Demo & Report** | All Team | All Team | Instructor |

---

## 12. Role Boundaries Quick Reference Card (Cheat Sheet)

```text
┌─────────────────────────────────────────────────────────────┐
│                 BRAIN-NET BOUNDARIES CHEAT SHEET              │
├─────────────┬───────────────────────┬───────────────────────┤
│ ROLE        │ PRIMARY ZONE          │ STAY OUT OF ZONE      │
├─────────────┼───────────────────────┼───────────────────────┤
│ Architect   │ Routing, Struct, TTP  │ ML Training, Ethics   │
├─────────────┼───────────────────────┼───────────────────────┤
│ BCI Eng.    │ ML Classif., Hardware │ Routing Protocols     │
├─────────────┼───────────────────────┼───────────────────────┤
│ Security    │ Firewall, Handshake   │ Encryption algos      │
├─────────────┼───────────────────────┼───────────────────────┤
│ Ethics Lead │ Rules, Bounds, Audit  │ Line-by-line coding   │
├─────────────┼───────────────────────┼───────────────────────┤
│ Quantum Exp.│ Encryption, Fallback  │ Firewall blocking     │
└─────────────┴───────────────────────┴───────────────────────┘
```

เอกสารฉบับนี้จัดทำขึ้นเพื่อรักษาขอบเขตการทำงานร่วมกันอย่างมีประสิทธิภาพ ลดความซิกแซกในการโยนงาน และเสริมกระบวนการตัดสินใจ (Accountability) ในโปรเจกต์ Brain-Net ที่มีความอ่อนไหวสูงได้อย่างมืออาชีพ