# 📖 คู่มือการรันโปรแกรม Brain-Net (Phase 1 MVP)

คู่มือนี้สำหรับผู้ใช้งาน Windows ที่ต้องการรันระบบจำลองการรับส่งข้อมูลผ่านคลื่นสมอง และเจอปัญหาเรื่องคำสั่ง `pip` หรือ `python` ใน Terminal

---

## 🛠️ ขั้นตอนที่ 1: ติดตั้งห้องสมุด (Dependencies)
หากพิมพ์ `pip` แล้ว Error ให้ใช้คำสั่ง "ตัวเรียกใช้งานหลัก" แทนครับ:

```powershell
# ใช้คำสั่งนี้เพื่อติดตั้ง Library ทั้งหมด
python -m pip install -r requirements.txt
```
*หากคำสั่งบนไม่ได้ ให้ลองเปลี่ยนจาก `python` เป็น `py` ครับ*

---

## 📊 ขั้นตอนที่ 2: สร้างข้อมูลคลื่นสมองจำลอง (Generate Data)
เราต้องมีข้อมูลดิบเพื่อใช้ในการวิจัยและฝึก AI ก่อนรันคำสั่งนี้:

```powershell
python data/generate_mock_dataset.py --n 600 --verify
```
*ระบบจะสร้างไฟล์ `.csv` ในโฟลเดอร์ `data/` และตรวจสอบว่า AI สามารถแยกแยะข้อมูลได้หรือไม่*

---

## 🧠 ขั้นตอนที่ 3: ฝึก AI ให้จำแนกสถานะ (Train AI)
นำข้อมูลที่สร้างไว้มาฝึกโมเดลเพื่อให้ระบบรู้จัก "คำสั่งทางจิต":

```powershell
python -m src.bci.neural_classifier
```
*ผลลัพธ์จะถูกบันทึกเป็นไฟล์โมเดลในโฟลเดอร์ `models/` (จะถูกสร้างขึ้นอัตโนมัติ)*

---

## 🚀 ขั้นตอนที่ 4: รันระบบจำลองการสื่อสาร (Full Demo)
ขั้นตอนนี้คือการเชื่อมต่อทุกอย่างเข้าด้วยกัน (Pipeline):

```powershell
python -m src.brain_net_pipeline
```
**คุณจะเห็นหน้าจอแสดงผล:**
- การส่งแพ็กเก็ต `TTP Packet`
- การตรวจสอบความหน่วง (`Latency`)
- การดักกรองโดย `Firewall`
- การเข้ารหัสข้อมูลแบบจำลอง `Quantum`

---

## 🖥️ ขั้นตอนที่ 5: การรัน Interactive GUI Dashboard (แนะนำ)
หากต้องการเห็นกราฟ แดชบอร์ด และปุ่มควบคุมแบบเห็นภาพจริง ให้ใช้คำสั่งนี้:

```powershell
python -m src.gui_app
```
**ฟีเจอร์เด่นใน GUI:**
- **Consensual Handshake:** ปุ่มเปิด Session เพื่อตรวจสอบจริยธรรม
- **Live Stream:** แสดงแพ็กเก็ตที่วิ่งอยู่แบบ Real-time
- **Real-time Metrics:** อัปเดต Latency และ Success Rate ทุกวินาที
- **E-STOP:** ปุ่มหยุดขุกเฉินสีแดงขนาดใหญ่เพื่อความปลอดภัย

---

## 🧪 ขั้นตอนที่ 6: การทดสอบระบบ (Running Tests)
หากต้องการตรวจสอบความถูกต้องของโค้ดทั้งหมด:

```powershell
python -m pytest tests/ -v
```

---

## ❓ ปัญหาที่พบบ่อย (Troubleshooting)

**1. พิมพ์ `python` แล้วขึ้น Error ว่าไม่รู้จัก?**
- ให้ลองเปลี่ยน `python` เป็น `py` ในทุกคำสั่งครับ (เช่น `py -m pip ...`)

**2. ModuleNotFoundError: No module named 'sklearn'?**
- แสดงว่าการติดตั้งในขั้นตอนที่ 1 ไม่สำเร็จ ให้รัน:
  `python -m pip install scikit-learn numpy pandas mne cryptography pytest matplotlib scipy`

**3. หน้าจอขึ้น WARNING สีเหลืองตอนติดตั้ง?**
- ไม่ต้องตกใจครับ เป็นแค่คำเตือนเรื่องตำแหน่งไฟล์ระบบ โปรแกรมยังทำงานได้ปกติครับ

---
*จัดทำโดย: ทีมพัฒนา Brain-Net Phase 1*
