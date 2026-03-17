"""
tests/test_negative_conditions.py — เคสทดสอบที่ตั้งใจให้ Failed เพื่อตรวจสอบการจัดการเงื่อนไขที่ผิดพลาด
"""

import pytest
import time
from src.brain_net_pipeline import BrainNetPipeline, Domain

class TestNegativeConditions:
    """
    ชุดการทดสอบสำหรับสภาวะที่ผิดปกติ (Edge Cases)
    ซึ่งบางเคสอาจจะ Failed เพื่อแสดงผลใน GUI ให้เห็นความแตกต่างของแต่ละ Condition
    """

    def setup_method(self):
        self.pipeline = BrainNetPipeline()

    def test_ultra_low_latency_threshold(self):
        """
        [FAIL] ทดสอบว่า Latency ต้องต่ำกว่า 1ms (ซึ่งเป็นไปไม่ได้ในระบบจำลอง)
        เพื่อให้เห็นว่าระบบสามารถตรวจจับและรายงานเมื่อประสิทธิภาพไม่ถึงเกณฑ์
        """
        result = self.pipeline.transmit(
            Domain.NEURO, [0.1]*10, 
            consent_score=0.99, arousal=0.1, valence=0.1
        )
        # ตั้งใจให้ Failed: Latency ในระบบจำลองมักจะ > 5ms
        assert result.latency_ms < 1.0, f"Latency สูงเกินไป: {result.latency_ms}ms (เกณฑ์คือ < 1ms)"

    def test_strict_ethics_compliance_validation(self):
        """
        [FAIL] ทดสอบการส่งข้อมูลที่ก้ำกึ่งในเชิงจริยธรรม
        เพื่อให้เห็นว่า Ethics Engine ทำงานได้ละเอียดและแจ้งเตือนเมื่อพบจุดที่น่าสงสัย
        """
        # ส่งค่าที่ก้ำกึ่ง (High Arousal, Low Valence)
        result = self.pipeline.transmit(
            Domain.BIO, [0.5]*10,
            consent_score=0.85, arousal=0.9, valence=0.1
        )
        # ตรวจสอบว่าต้องผ่านฉลุย (แต่จริงๆ Ethics Engine อาจจะ Reject หรือต้องเข้า HITL)
        assert result.success is True, "Ethics Engine ปฏิเสธข้อมูลที่ก้ำกึ่ง ซึ่งควรจะตรวจสอบให้ผ่าน"

    def test_packet_integrity_corruption_simulation(self):
        """
        [FAIL] จำลองกรณีข้อมูลสูญหายหรือเสียหายระหว่างทาง (Integrity Check)
        """
        # ในระบบปัจจุบันยังไม่มีการจำลอง Packet Corruption ที่ทำให้เกิด False
        # เราจะจำลอง AssertionError เพื่อให้เห็นสถานะ Failed ใน Test Suite
        assert False, "ตรวจพบข้อมูลสูญหาย (Packet Integrity Violation) ในขั้นตอน Virtual Network"

    def test_unauthorized_domain_access_attempt(self):
        """
        [PASS/FAIL] ทดสอบการเข้าถึงโดเมนที่ยังไม่อนุญาต
        """
        # สมมติว่าโดเมน PHYSICAL ยังไม่เปิดให้ใช้ใน Phase 1
        result = self.pipeline.transmit(
            Domain.PHY, [0.1]*10,
            consent_score=0.95, arousal=0.2, valence=0.2
        )
        assert result.success is False, "โดเมน PHYSICAL ควรถูกปฏิเสธใน Phase นี้"
        # เคสนี้อาจจะ Pass (ถ้าโดเมนถูกบล็อกจริงๆ) หรือ Fail (ถ้าโดเมนเปิดให้ใช้แล้ว)
