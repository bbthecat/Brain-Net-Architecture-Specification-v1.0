"""
conftest.py — Shared pytest fixtures for Brain-Net test suite
"""

import numpy as np
import pytest

from src.bci.connect_bci import BCIConnection
from src.bci.clean_eeg_data import EEGPreprocessor
from src.daft.domain_interface import Domain, DomainInterface
from src.daft.daft_validator import DAFTValidator
from src.protocol.ttp_packet import TTPHeader, TTPPacket
from src.protocol.virtual_network import VirtualNetwork
from src.security.brain_firewall import BrainFirewall
from src.security.consensual_handshake import ConsensualHandshake
from src.security.ethics_rule_engine import EthicsRuleEngine
from src.security.hitl_checkpoint import HITLCheckpoint
from src.security.audit_log import AuditLog
from src.crypto.mock_qkd_aes import MockQKD
from src.metrics.quality_metrics import QualityMetrics


# ── Packet Helpers ────────────────────────────────────────────────────────────

@pytest.fixture
def valid_packet() -> TTPPacket:
    """A standard valid TTPPacket for use in tests."""
    header = TTPHeader(source_id="NODE_A", dest_id="NODE_B", symbol_id=0)
    return TTPPacket(
        header=header, symbol="focus",
        valence=0.2, arousal=0.3, intensity=0.7,
        consent_score=0.85, domain="neuro",
    )


@pytest.fixture
def blocked_packet() -> TTPPacket:
    """A packet that should be blocked by all security layers."""
    header = TTPHeader(source_id="NODE_X", dest_id="NODE_Y", symbol_id=2)
    return TTPPacket(
        header=header, symbol="reject",
        valence=-0.8, arousal=0.95, intensity=0.9,
        consent_score=0.3, domain="neuro",
    )


@pytest.fixture
def private_packet() -> TTPPacket:
    """A packet with a private thought symbol — should be blocked by Ethics E-002."""
    header = TTPHeader(source_id="NODE_A", dest_id="NODE_B", symbol_id=99)
    return TTPPacket(
        header=header, symbol="private_thought",
        valence=0.2, arousal=0.3, intensity=0.7,
        consent_score=0.9, domain="neuro",
    )


# ── Component Fixtures ────────────────────────────────────────────────────────

@pytest.fixture
def bci_connection() -> BCIConnection:
    bci = BCIConnection("TEST_SUBJ", mode="mock")
    bci.connect()
    yield bci
    bci.disconnect()


@pytest.fixture
def preprocessor() -> EEGPreprocessor:
    return EEGPreprocessor()


@pytest.fixture
def domain_interface() -> DomainInterface:
    return DomainInterface()


@pytest.fixture
def daft_validator() -> DAFTValidator:
    return DAFTValidator()


@pytest.fixture
def brain_firewall() -> BrainFirewall:
    return BrainFirewall()


@pytest.fixture
def consensual_handshake() -> ConsensualHandshake:
    return ConsensualHandshake()


@pytest.fixture
def ethics_engine() -> EthicsRuleEngine:
    return EthicsRuleEngine()


@pytest.fixture
def hitl_checkpoint() -> HITLCheckpoint:
    alerts = []
    return HITLCheckpoint(alert_callback=lambda e: alerts.append(e))


@pytest.fixture
def audit_log() -> AuditLog:
    return AuditLog()


@pytest.fixture
def mock_qkd() -> MockQKD:
    return MockQKD(reuse_key=True)


@pytest.fixture
def quality_metrics() -> QualityMetrics:
    return QualityMetrics()


@pytest.fixture
def virtual_network() -> VirtualNetwork:
    net = VirtualNetwork(base_latency_ms=2.0, jitter_ms=1.0, packet_loss_pct=0.0)
    net.setup()
    return net


# ── Data Fixtures ─────────────────────────────────────────────────────────────

@pytest.fixture
def neuro_symbol(domain_interface):
    return domain_interface.map(Domain.NEURO, "focus", consent_score=0.9)


@pytest.fixture
def bio_symbol(domain_interface):
    return domain_interface.map(Domain.BIO, np.random.rand(64), consent_score=0.9)


@pytest.fixture
def phy_symbol(domain_interface):
    return domain_interface.map(Domain.PHY, np.random.rand(14, 32), consent_score=0.9)


@pytest.fixture
def quantum_symbol(domain_interface):
    state = np.random.randn(8) + 1j * np.random.randn(8)
    state /= np.linalg.norm(state)
    return domain_interface.map(Domain.QUANTUM, state, consent_score=0.9)
