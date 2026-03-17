"""
tests/unit/test_context_frame.py — Unit tests for ContextFrame
"""

import time
import pytest
from src.protocol.context_frame import ContextFrame, _symbol_id_to_name
from src.protocol.ttp_packet import TTPPacket

def test_context_frame_assembly():
    frame = ContextFrame(
        neural_symbol_id=0,
        valence=0.5,
        arousal=0.3,
        intensity=0.8,
        timestamp_us=int(time.time() * 1e6),
        cognitive_anchor="SUBJ_1"
    )
    
    packet = frame.assemble_with_ttp(
        source_id="NODE_A",
        dest_id="NODE_B",
        consent_score=0.9,
        domain="neuro"
    )
    
    assert isinstance(packet, TTPPacket)
    assert packet.header.source_id == "NODE_A"
    assert packet.header.dest_id == "NODE_B"
    assert packet.header.symbol_id == 0
    assert packet.symbol == "focus"
    assert packet.valence == 0.5
    assert packet.arousal == 0.3
    assert packet.intensity == 0.8
    assert packet.consent_score == 0.9
    assert packet.domain == "neuro"

def test_symbol_id_to_name():
    assert _symbol_id_to_name(0) == "focus"
    assert _symbol_id_to_name(1) == "relax"
    assert _symbol_id_to_name(2) == "reject"
    assert _symbol_id_to_name(3) == "neutral"
    assert _symbol_id_to_name(99) == "unknown_99"
