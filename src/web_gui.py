import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import subprocess
import re
import random
import psutil
from datetime import datetime
import sys
import os

# Add project root to sys.path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.brain_net_pipeline import BrainNetPipeline, Domain
from src.daft.domain_interface import Domain

# --- Page Configuration ---
st.set_page_config(
    page_title="Brain-Net Protocol Dashboard — v1.0",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a more "High-Tech" look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3d4455;
    }
    .stSidebar {
        background-color: #161b22;
    }
    .stPlotlyChart {
        background-color: #1e2130;
        border-radius: 10px;
        border: 1px solid #3d4455;
        padding: 10px;
    }
    h1, h2, h3 {
        color: #00E676 !important;
    }
    .stStatusWidget {
        background-color: #1e2130 !important;
    }
    .log-container {
        background-color: #000000;
        color: #00E676;
        font-family: 'Courier New', Courier, monospace;
        padding: 15px;
        border-radius: 5px;
        height: 500px;
        overflow-y: scroll;
        border: 1px solid #3d4455;
        font-size: 0.9em;
    }
    .test-log-container {
        background-color: #1a1a1a;
        color: #cccccc;
        font-family: 'Consolas', 'Monaco', monospace;
        padding: 15px;
        border-radius: 5px;
        height: 500px;
        overflow-y: scroll;
        border: 1px solid #444;
        white-space: pre-wrap;
    }
    .log-entry {
        margin-bottom: 5px;
    }
    .log-system { color: #64B5F6; }
    .log-security { color: #00E676; }
    .log-error { color: #F44336; }
    .log-success { color: #00E676; }
    .log-info { color: #FFD54F; }
    .status-active { color: #00E676; font-weight: bold; }
    .status-standby { color: #FFD54F; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- Initialize Session State ---
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = BrainNetPipeline()
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=[
        'timestamp', 'success', 'latency_ms', 'ethics_decision', 'hitl_triggered', 'domain', 'reason'
    ])
if 'last_stage_times' not in st.session_state:
    st.session_state.last_stage_times = {}
if 'session_active' not in st.session_state:
    st.session_state.session_active = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'test_output' not in st.session_state:
    st.session_state.test_output = ""
if 'test_stats' not in st.session_state:
    st.session_state.test_stats = {"total": "-", "pass": "-", "fail": "-", "cov": "-"}
if 'estop_triggered' not in st.session_state:
    st.session_state.estop_triggered = False
if 'streaming' not in st.session_state:
    st.session_state.streaming = False
if 'last_consent' not in st.session_state:
    st.session_state.last_consent = 0.0

def add_log(msg, level="system"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append({"time": timestamp, "msg": msg, "level": level})
    if len(st.session_state.logs) > 200:
        st.session_state.logs = st.session_state.logs[-200:]

# --- Sidebar: Control Panel ---
st.sidebar.title("🧠 Brain-Net Control")

# EMERGENCY STOP (E-STOP)
if st.sidebar.button("🛑 EMERGENCY STOP (E-STOP)", type="primary", use_container_width=True):
    st.session_state.estop_triggered = True
    st.session_state.session_active = False
    st.session_state.streaming = False
    add_log("[CRITICAL] EMERGENCY STOP TRIGGERED BY HUMAN OPERATOR", "error")
    st.sidebar.error("E-STOP ACTIVATED! 🛑")

if st.session_state.estop_triggered:
    if st.sidebar.button("Reset E-STOP", type="secondary"):
        st.session_state.estop_triggered = False
        st.sidebar.success("E-STOP Reset.")

st.sidebar.markdown("---")
st.sidebar.subheader("System Health")
h_col1, h_col2 = st.sidebar.columns(2)
h_col1.markdown(f"Firewall: <span class='status-active'>ACTIVE</span>", unsafe_allow_html=True)
h_col1.markdown(f"Ethics Engine: <span class='status-active'>ACTIVE</span>", unsafe_allow_html=True)
h_col2.markdown(f"QKD Stack: <span class='status-active'>ACTIVE</span>", unsafe_allow_html=True)
h_col2.markdown(f"HITL Hub: <span class='status-standby'>STANDBY</span>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.subheader("Streaming Settings")
stream_speed = st.sidebar.slider("Stream Delay (ms)", 10, 1000, 100)
batch_size = st.sidebar.number_input("Batch Size (Manual)", 1, 100, 10)

st.sidebar.markdown("---")
domain_list = [d.name for d in Domain]
domain_choice = st.sidebar.selectbox("Target Domain", domain_list, index=domain_list.index("NEURO"))

auto_params = st.sidebar.checkbox("Auto-Randomize Parameters", value=True)

# Hide sliders if Auto-Randomize is enabled
if not auto_params:
    arousal = st.sidebar.slider("Arousal Level", 0.0, 1.0, 0.3)
    valence = st.sidebar.slider("Valence Level", 0.0, 1.0, 0.2)
    manual_consent = st.sidebar.slider("Consent Score", 0.0, 1.0, 0.85)
else:
    arousal, valence, manual_consent = 0.3, 0.2, 0.85

st.sidebar.markdown("---")
st.sidebar.subheader("Resource Monitor")
cpu_usage = psutil.cpu_percent()
mem_usage = psutil.virtual_memory().percent
st.sidebar.progress(cpu_usage / 100.0, text=f"CPU: {cpu_usage}%")
st.sidebar.progress(mem_usage / 100.0, text=f"RAM: {mem_usage}%")

# --- Main Dashboard Tabs ---
tab1, tab2 = st.tabs(["📊 Dashboard — Protocol Monitor", "🧪 Protocol Tests — Quality Assurance"])

with tab1:
    st.title("🧠 BRAIN-NET PROTOCOL CONTROL CENTER")
    
    # Row 1: Handshake and Streaming Controls
    col_hnd, col_stream, col_batch = st.columns(3)
    
    with col_hnd:
        if st.button("🤝 START CONSENSUAL HANDSHAKE", type="primary", use_container_width=True, disabled=st.session_state.estop_triggered):
            add_log("[SYSTEM] Requesting consensual handshake...", "system")
            with st.spinner("Handshaking..."):
                cs = manual_consent if not auto_params else random.uniform(0.75, 0.98)
                ar = arousal if not auto_params else random.uniform(0.1, 0.5)
                vl = valence if not auto_params else random.uniform(0.1, 0.4)
                
                success = st.session_state.pipeline.open_session(ar, vl, cs)
                if success:
                    st.session_state.session_active = True
                    st.session_state.last_consent = cs
                    add_log(f"[SECURITY] Consensual Session Established. Consent Score: {cs:.2f}. Neurorights Verified.", "security")
                else:
                    st.session_state.session_active = False
                    add_log("[SECURITY] Consensual Session Denied. Insufficient Consent.", "error")

    with col_stream:
        if not st.session_state.streaming:
            if st.button("▶️ START AUTO STREAM", type="primary", use_container_width=True, 
                         disabled=st.session_state.estop_triggered or not st.session_state.session_active):
                st.session_state.streaming = True
                st.rerun()
        else:
            if st.button("⏹️ STOP AUTO STREAM", type="secondary", use_container_width=True):
                st.session_state.streaming = False
                st.rerun()

    manual_batch_triggered = False
    with col_batch:
        if st.button("🚀 TRANSMIT BATCH (MANUAL)", type="primary", use_container_width=True,
                     disabled=st.session_state.estop_triggered or not st.session_state.session_active or st.session_state.streaming):
            manual_batch_triggered = True

    st.markdown("---")

    # Row 2: Metrics
    metrics_placeholder = st.empty()

    def update_metrics_display():
        m = st.session_state.pipeline._metrics
        p95 = m.latency_percentile(95)
        daft = m.daft_pass_rate() * 100
        eth = m.ethics_compliance_rate() * 100
        pmi = m.compute_pmi()["overall"]
        succ = (st.session_state.history['success'].sum() / len(st.session_state.history) * 100) if not st.session_state.history.empty else 0.0
        
        with metrics_placeholder.container():
            st.markdown("#### Quality Metrics")
            m1, m2, m3, m4, m5, m6 = st.columns(6)
            m1.metric("P95 Latency", f"{p95:.1f} ms")
            m2.metric("Consent Score", f"{st.session_state.last_consent:.2f}")
            m3.metric("Success Rate", f"{succ:.1f}%")
            m4.metric("DAFT Pass Rate", f"{daft:.1f}%")
            m5.metric("Ethics Compliance", f"{eth:.1f}%")
            m6.metric("PMI Score", f"{pmi:.1f}")

    update_metrics_display()
    st.markdown("---")
    
    # Row 3: Real-time Side-by-Side (Log Stream & Latency Graph)
    col_log, col_graph = st.columns([1, 1])
    
    with col_log:
        st.subheader("📟 REAL-TIME TTP DATA STREAM")
        log_placeholder = st.empty()

    with col_graph:
        st.subheader("📈 Real-time Latency Trend")
        graph_placeholder = st.empty()

    def render_logs():
        log_html = '<div class="log-container">'
        for log in reversed(st.session_state.logs):
            log_html += f'<div class="log-entry"><span class="log-{log["level"]}">[{log["time"]}] {log["msg"]}</span></div>'
        log_html += '</div>'
        log_placeholder.markdown(log_html, unsafe_allow_html=True)

    def render_graph():
        if not st.session_state.history.empty:
            fig = px.line(st.session_state.history, x='timestamp', y='latency_ms', 
                          template="plotly_dark", 
                          color_discrete_sequence=['#00E676'])
            fig.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                height=450,
                xaxis_title="Time (ms precision)",
                yaxis_title="Latency (ms)"
            )
            fig.update_xaxes(nticks=10)
            graph_placeholder.plotly_chart(fig, use_container_width=True, key=f"graph_{len(st.session_state.history)}")
        else:
            graph_placeholder.info("Start stream to see real-time data.")

    render_logs()
    render_graph()

    # --- TRANSMIT FUNCTION ---
    def run_transmission():
        cur_domain = Domain[domain_choice]
        cur_arousal = arousal if not auto_params else random.uniform(0.1, 0.5)
        cur_valence = valence if not auto_params else random.uniform(0.1, 0.4)
        cur_consent = manual_consent if not auto_params else random.uniform(0.75, 0.98)
        
        # Update consent display
        st.session_state.last_consent = cur_consent
        
        mock_raw_input = np.random.randn(10) 
        result = st.session_state.pipeline.transmit(
            cur_domain, mock_raw_input,
            consent_score=cur_consent, arousal=cur_arousal, valence=cur_valence
        )
        
        # Save last stage times for breakdown chart
        st.session_state.last_stage_times = result.stage_times
        
        new_row = {
            'timestamp': datetime.now().strftime("%H:%M:%S.%f")[:-3],
            'success': result.success,
            'latency_ms': result.latency_ms,
            'ethics_decision': result.ethics_decision,
            'hitl_triggered': result.hitl_triggered,
            'domain': cur_domain.name,
            'reason': result.error if result.error else ("Validated" if result.success else "Policy Block")
        }
        st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame([new_row])], ignore_index=True)
        if len(st.session_state.history) > 100:
            st.session_state.history = st.session_state.history.tail(100)
        
        status = "SENT" if result.success else f"BLOCKED ({result.ethics_decision})"
        log_msg = f"PKT {len(st.session_state.history):03d} | {result.symbol.upper():<8} | CS: {cur_consent:.2f} | Latency: {result.latency_ms:4.1f}ms | {status}"
        add_log(log_msg, "success" if result.success else "error")
        
        update_metrics_display()
        render_logs()
        render_graph()

    # --- AUTO STREAM LOOP ---
    if st.session_state.streaming and not st.session_state.estop_triggered:
        for _ in range(5):
            if not st.session_state.streaming or st.session_state.estop_triggered: break
            run_transmission()
            time.sleep(stream_speed / 1000.0)
        st.rerun()

    # --- MANUAL BATCH LOOP ---
    if manual_batch_triggered:
        progress_bar = st.progress(0)
        for i in range(batch_size):
            if st.session_state.estop_triggered: break
            run_transmission()
            progress = (i + 1) / batch_size
            progress_bar.progress(progress)
            time.sleep(stream_speed / 1000.0)
        st.success(f"Batch of {batch_size} packets delivered.")
        st.rerun()

    # Row 4: Analytics (Pie Chart & Stage Latency)
    st.markdown("---")
    col_pie, col_stage = st.columns([1, 1])
    
    with col_pie:
        st.subheader("Ethics Engine Decisions")
        if not st.session_state.history.empty:
            counts = st.session_state.history['ethics_decision'].value_counts().reset_index()
            fig = px.pie(counts, values='count', names='ethics_decision', hole=0.4, template="plotly_dark")
            fig.update_layout(height=350, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Waiting for data...")
            
    with col_stage:
        st.subheader("⚡ Last Packet: Stage Latency Breakdown")
        if st.session_state.last_stage_times:
            df_stages = pd.DataFrame(list(st.session_state.last_stage_times.items()), columns=['Stage', 'Time (ms)'])
            fig_stages = px.bar(df_stages, x='Stage', y='Time (ms)', template="plotly_dark", color='Time (ms)', color_continuous_scale='Greens')
            fig_stages.update_layout(height=350, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
            st.plotly_chart(fig_stages, use_container_width=True)
        else:
            st.info("Waiting for data...")

    # Row 5: Transaction History & Export
    st.markdown("---")
    st.subheader("📜 ประวัติการส่งข้อมูล (Transaction History)")
    
    if not st.session_state.history.empty:
        # Download Button
        csv = st.session_state.history.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Logs to CSV",
            data=csv,
            file_name=f'brain_net_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv',
        )
        
        display_df = st.session_state.history.copy()
        display_df.columns = [
            "เวลา (Timestamp)", "สถานะ (Success)", "ความหน่วง (Latency ms)", 
            "การตัดสินใจ (Ethics)", "HITL Triggered", "โดเมน (Domain)", "เหตุผล (Reason)"
        ]
        st.dataframe(display_df.sort_index(ascending=False), 
                     use_container_width=True, hide_index=True, height=350)

with tab2:
    st.title("🧪 BRAIN-NET TEST SUITE")
    
    # --- Educational Section ---
    with st.expander("ℹ️ รายละเอียดการทดสอบ (ใช้อะไรเทส? เทสทำไม? เงื่อนไขคืออะไร?)", expanded=True):
        col_ed1, col_ed2 = st.columns(2)
        with col_ed1:
            st.markdown("""
            ### 🛠️ เครื่องมือที่ใช้ (What?)
            - **Pytest**: ตัวรันการทดสอบมาตรฐาน
            - **Pytest-Cov**: วัด Code Coverage
            - **Integration Tests**: ทดสอบการทำงานร่วมกัน
            - **E2E Tests**: ทดสอบตั้งแต่ต้นจนจบ
            """)
        with col_ed2:
            st.markdown("""
            ### 🎯 ทำไมต้องเทส? (Why?)
            - **Safety First**: ป้องกันข้อมูลรั่วไหล
            - **Ethics Compliance**: ทำตามกฎจริยธรรม 100%
            - **Latency Check**: ประสิทธิภาพ Real-time (< 50ms)
            """)
        
        st.markdown("---")
        st.markdown("### ✅ เงื่อนไขการผ่าน/ไม่ผ่าน (Pass vs Fail)")
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            st.info("""
            **🟢 ผ่าน (PASS) เมื่อ:**
            - Latency อยู่ในเกณฑ์
            - ข้อมูลผ่าน DAFT และ Ethics
            - Handshake ถูกต้อง
            """)
        with p_col2:
            st.error("""
            **🔴 ไม่ผ่าน (FAIL) เมื่อ:**
            - พบความเสี่ยงเชิงจริยธรรม
            - Packet เสียหายหรือสูญหาย
            - ประมวลผลนานเกินมาตรฐาน
            """)

    st.markdown("---")
    ts1, ts2, ts3, ts4 = st.columns(4)
    ts1.metric("Total Tests", st.session_state.test_stats["total"])
    ts2.metric("Passed", st.session_state.test_stats["pass"])
    ts3.metric("Failed", st.session_state.test_stats["fail"])
    ts4.metric("Coverage", st.session_state.test_stats["cov"])
    
    if st.button("▶️ Run Full Test Suite (pytest)", type="primary"):
        st.session_state.test_output = ">>> Initiating python -m pytest tests/ --cov=src/ ...\n"
        with st.spinner("Running tests..."):
            cmd = [sys.executable, "-m", "pytest", "tests/", "--cov=src/", "--cov-report=term-missing"]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            full_out = ""
            if process.stdout:
                for line in process.stdout:
                    full_out += line
            process.wait()
            st.session_state.test_output = full_out
            
            pass_match = re.search(r"(\d+) passed", full_out)
            fail_match = re.search(r"(\d+) failed", full_out)
            err_match = re.search(r"(\d+) error", full_out)
            cov_match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+%)", full_out)
            
            n_pass = int(pass_match.group(1)) if pass_match else 0
            n_fail = (int(fail_match.group(1)) if fail_match else 0) + (int(err_match.group(1)) if err_match else 0)
            st.session_state.test_stats = {
                "total": str(n_pass + n_fail), "pass": str(n_pass), "fail": str(n_fail), "cov": cov_match.group(1) if cov_match else "N/A"
            }
            st.rerun()

    st.markdown(f'<div class="test-log-container">{st.session_state.test_output}</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Brain-Net Protocol Specification v1.0 | Real-time Auto Stream v1.4 | Developed by Senior Network Architect เจม")
