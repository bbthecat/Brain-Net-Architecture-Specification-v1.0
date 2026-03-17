import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import time
import random
import subprocess
import re
from datetime import datetime
from typing import Optional

# Import backend pipeline
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.brain_net_pipeline import BrainNetPipeline, Domain

class BrainNetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Brain-Net Protocol Dashboard — v1.0 MVP")
        self.root.geometry("1100x700")
        self.root.configure(bg="#121212")

        self.pipeline = BrainNetPipeline()
        self.log_queue = queue.Queue()
        self.is_running = False
        self.stop_requested = False
        
        # UI State Variables
        self.m_p95 = tk.StringVar(value="0.0 ms")
        self.m_consent = tk.StringVar(value="0.00")
        self.m_success = tk.StringVar(value="0.0%")
        self.m_daft = tk.StringVar(value="0.0%")
        self.m_ethics = tk.StringVar(value="0.0%")
        self.m_pmi = tk.StringVar(value="0.0")
        self.pkt_count_var = tk.StringVar(value="50")

        # UI Widgets (initialized in _build_ui)
        self.notebook: ttk.Notebook = None # type: ignore
        self.dash_tab: ttk.Frame = None # type: ignore
        self.test_tab: ttk.Frame = None # type: ignore
        self.estop_btn: ttk.Button = None # type: ignore
        self.session_status: ttk.Label = None # type: ignore
        self.start_btn: ttk.Button = None # type: ignore
        self.run_btn: ttk.Button = None # type: ignore
        self.log_area: scrolledtext.ScrolledText = None # type: ignore
        self.test_log_area: scrolledtext.ScrolledText = None # type: ignore
        self.test_btn: ttk.Button = None # type: ignore

        # Test Stats Variables
        self.test_total_var = tk.StringVar(value="-")
        self.test_pass_var = tk.StringVar(value="-")
        self.test_fail_var = tk.StringVar(value="-")
        self.test_cov_var = tk.StringVar(value="-")

        self._setup_styles()
        self._build_ui()
        
        # Start log consumer
        self.root.after(100, self._process_logs)

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Dark Theme Overrides
        style.configure("TFrame", background="#121212")
        style.configure("TLabel", background="#121212", foreground="#E0E0E0", font=("Inter", 10))
        style.configure("Header.TLabel", font=("Inter", 18, "bold"), foreground="#00E676")
        style.configure("Metric.TLabel", font=("JetBrains Mono", 12, "bold"), foreground="#64B5F6")
        
        style.configure("TButton", font=("Inter", 10, "bold"), padding=6)
        style.map("TButton", background=[("active", "#333333")], foreground=[("active", "white")])
        
        style.configure("ESTOP.TButton", background="#D32F2F", foreground="white")
        style.map("ESTOP.TButton", background=[("active", "#FF5252")])

    def _build_ui(self):
        # Create Notebook for Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # --- Tab 1: Dashboard ---
        self.dash_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dash_tab, text=" 📊 Dashboard ")

        # --- Top Header (Dashboard) ---
        header_frame = ttk.Frame(self.dash_tab)
        header_frame.pack(fill="x", padx=20, pady=15)
        
        ttk.Label(header_frame, text="🧠 BRAIN-NET PROTOCOL CONTROL CENTER", style="Header.TLabel").pack(side="left")
        
        self.estop_btn = ttk.Button(header_frame, text="🛑 EMERGENCY STOP (E-STOP)", 
                                   style="ESTOP.TButton", command=self._trigger_estop)
        self.estop_btn.pack(side="right")

        # --- Main Content (Panels) ---
        main_frame = ttk.Frame(self.dash_tab)
        main_frame.pack(fill="both", expand=True, padx=20)

        # Left Panel: Controls
        left_panel = ttk.Frame(main_frame, width=250)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        
        # Session Box
        session_box = ttk.LabelFrame(left_panel, text=" Session Management ", padding=10)
        session_box.pack(fill="x", pady=(0, 10))
        
        self.session_status = ttk.Label(session_box, text="STATUS: DISCONNECTED", foreground="#FF5252")
        self.session_status.pack(pady=5)
        
        self.start_btn = ttk.Button(session_box, text="Start Consensual Handshake", command=self._start_session)
        self.start_btn.pack(fill="x", pady=5)

        # Simulation Box
        sim_box = ttk.LabelFrame(left_panel, text=" Simulation Control ", padding=10)
        sim_box.pack(fill="x")
        
        ttk.Label(sim_box, text="Packet Count:").pack(anchor="w")
        self.pkt_count_var = tk.StringVar(value="50")
        ttk.Entry(sim_box, textvariable=self.pkt_count_var).pack(fill="x", pady=5)
        
        self.run_btn = ttk.Button(sim_box, text="▶ Run Pipeline Simulation", command=self._run_simulation)
        self.run_btn.pack(fill="x", pady=10)
        self.run_btn["state"] = "disabled"

        # Center Panel: Live Log
        center_panel = ttk.Frame(main_frame)
        center_panel.pack(side="left", fill="both", expand=True)
        
        ttk.Label(center_panel, text="REAL-TIME TTP DATA STREAM", font=("Inter", 10, "bold")).pack(anchor="w")
        self.log_area = scrolledtext.ScrolledText(center_panel, bg="#1E1E1E", fg="#A5D6A7", 
                                                 insertbackground="white", font=("JetBrains Mono", 9))
        self.log_area.pack(fill="both", expand=True, pady=5)

        # Right Panel: Metrics
        right_panel = ttk.Frame(main_frame, width=200)
        right_panel.pack(side="left", fill="y", padx=(10, 0))
        
        metrics_box = ttk.LabelFrame(right_panel, text=" Quality Metrics ", padding=10)
        metrics_box.pack(fill="x")

        self.m_p95 = self._add_metric(metrics_box, "P95 Latency:", "0.0 ms")
        self.m_consent = self._add_metric(metrics_box, "Consent Score:", "0.00")
        self.m_success = self._add_metric(metrics_box, "Success Rate:", "0.0%")
        self.m_daft = self._add_metric(metrics_box, "DAFT Pass Rate:", "0.0%")
        self.m_ethics = self._add_metric(metrics_box, "Ethics Compliance:", "0.0%")
        self.m_pmi = self._add_metric(metrics_box, "PMI Score:", "0.0")

        self.test_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.test_tab, text=" 🛡️ ศูนย์ทดสอบ (Test Center) ")
        self._build_test_tab()

    def _build_test_tab(self):
        # Top Controls
        ctrl_frame = ttk.Frame(self.test_tab, padding=20)
        ctrl_frame.pack(fill="x")
        
        ttk.Label(ctrl_frame, text="✅ ระบบตรวจสอบความถูกต้อง (Verification)", style="Header.TLabel").pack(side="left")
        self.test_btn = ttk.Button(ctrl_frame, text="🚀 รันชุดทดสอบอัตโนมัติทั้งหมด", command=self._run_pytest)
        self.test_btn.pack(side="right")

        # Summary Panel
        stats_frame = ttk.Frame(self.test_tab, padding=(20, 0))
        stats_frame.pack(fill="x")
        
        lbl_style = {"font": ("Inter", 10, "bold")}
        val_style = {"font": ("JetBrains Mono", 11, "bold"), "foreground": "#A5D6A7"}
        
        # Grid for Stats
        for lbl, var in [
            ("รวมทั้งหมด:", self.test_total_var),
            ("ผ่านแล้ว:", self.test_pass_var),
            ("ล้มเหลว:", self.test_fail_var),
            ("Coverage:", self.test_cov_var)
        ]:
            f = ttk.Frame(stats_frame)
            f.pack(side="left", padx=(0, 30))
            ttk.Label(f, text=lbl, font=("Inter", 10, "bold")).pack(side="left")
            ttk.Label(f, textvariable=var, font=("JetBrains Mono", 11, "bold"), foreground="#A5D6A7").pack(side="left", padx=5)

        # Split View
        split_frame = ttk.Frame(self.test_tab, padding=20)
        split_frame.pack(fill="both", expand=True)

        # Left: Explanations
        explain_frame = ttk.LabelFrame(split_frame, text=" คำอธิบายการทดสอบ ", padding=10)
        explain_frame.pack(side="left", fill="both", expand=True)
        
        explanations = [
            ("🧠 BCI & ML Classifier", "ทดสอบ: การแยกแยะคลื่นสมองจาก Numpy | ผลลัพธ์: ระบบต้องแปลความหมาย (Focus/Relax) ได้แม่นยำ > 60% เพื่อยืนยันว่า AI เข้าใจเจตนาผู้ใช้"),
            ("📐 DAFT Validation", "ทดสอบ: การส่งข้อมูล Bio/Phy | ผลลัพธ์: ตรวจสอบว่าสูตรคณิตศาสตร์ Universal Symbols ทำงานถูกต้อง ข้อมูลไม่เพี้ยนระหว่างเชื่อมต่อ"),
            ("⚖️ Ethics Engine (E-001)", "ทดสอบ: ความเป็นส่วนตัวของความคิด | ผลลัพธ์: ระบบต้อง 'บล็อก' สัญญาณที่ละเมิด Neurorights หรือระบุตัวตนผู้ใช้มากเกินไป"),
            ("🔥 Brain Firewall", "ทดสอบ: สภาวะอารมณ์และแรงบังคับ | ผลลัพธ์: ป้องกันความเสียหายโดยการตัดสัญญาณทันทีหากตรวจพบความเครียดรุนแรงหรือการแฮ็กสมอง"),
            ("🛑 HITL Checkpoint", "ทดสอบ: การทำงานร่วมกับมนุษย์ | ผลลัพธ์: ปุ่ม E-STOP ต้องตัดกระบวนการทั้งหมดภายใน 500ms เพื่อความปลอดภัยสูงสุดของผู้ใช้"),
            ("🌐 E2E Protocol", "ทดสอบ: ประสิทธิภาพเน็ตเวิร์กโดยรวม | ผลลัพธ์: Latency ต่ำกว่า 50ms และข้อมูลต้องถึงปลายทาง 100% โดยไม่มีการตกหล่น")
        ]
        
        for title, desc in explanations:
            lbl = ttk.Label(explain_frame, text=title, font=("Inter", 10, "bold"), foreground="#00E676")
            lbl.pack(anchor="w", pady=(5, 0))
            txt = tk.Text(explain_frame, height=2, wrap="word", bg="#121212", fg="#B0B0B0", 
                        font=("Inter", 9), bd=0, highlightthickness=0)
            txt.insert("1.0", desc)
            txt.config(state="disabled")
            txt.pack(fill="x", pady=(0, 5))

        # Right: Output
        output_frame = ttk.LabelFrame(split_frame, text=" Live Test Output ", padding=10)
        output_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        self.test_log_area = scrolledtext.ScrolledText(output_frame, bg="#000000", fg="#FFFFFF", 
                                                      font=("JetBrains Mono", 9))
        self.test_log_area.pack(fill="both", expand=True)

    def _add_metric(self, parent, label_text, value_text):
        ttk.Label(parent, text=label_text).pack(anchor="w", pady=(5,0))
        var = tk.StringVar(value=value_text)
        ttk.Label(parent, textvariable=var, style="Metric.TLabel").pack(anchor="w", pady=(0,5))
        return var

    # --- Actions ---

    def _start_session(self):
        self._write_log("System", "Requesting consensual handshake...")
        consent_val = 0.92
        success = self.pipeline.open_session(consent=consent_val)
        if success:
            self.session_status.config(text="STATUS: CONNECTED (ACTIVE)", foreground="#00E676")
            self.run_btn["state"] = "normal"
            self.start_btn["state"] = "disabled"
            self._write_log("Security", f"Consensual Session Established. Consent Score: {consent_val:.2f}. Neurorights Verified.")
        else:
            self._write_log("Security", "Handshake REJECTED. Consent score below threshold.")
            messagebox.showerror("Security Error", "Consensual Handshake Failed.")

    def _run_simulation(self):
        try:
            n = int(self.pkt_count_var.get())
        except:
            n = 50
            
        self.is_running = True
        self.stop_requested = False
        self.run_btn["state"] = "disabled"
        self._write_log("Pipeline", f"Initiating {n}-packet benchmark...")
        
        threading.Thread(target=self._worker_thread, args=(n,), daemon=True).start()

    def _trigger_estop(self):
        self.stop_requested = True
        self._write_log("CRITICAL", "[H-001] EMERGENCY STOP TRIGGERED BY HUMAN OPERATOR")
        self.root.configure(bg="#420000") # Red alert
        self.is_running = False
        messagebox.showwarning("E-STOP", "Human-in-the-Loop Emergency Stop has been activated.\nAll transmissions terminated.")
        self.root.configure(bg="#121212")

    def _worker_thread(self, n):
        import random
        domains = [Domain.NEURO, Domain.BIO, Domain.PHY]
        
        results = []
        for i in range(1, n + 1):
            if self.stop_requested:
                break
                
            domain = random.choice(domains)
            # Simulate a "focus" or "relax" thought for demo
            thought = random.choice(["focus", "relax", "neutral"]) if domain == Domain.NEURO else "sensor_data"
            
            # Run actual pipeline transmission
            cs = random.uniform(0.75, 0.98)
            res = self.pipeline.transmit(domain, thought, consent_score=cs)
            results.append((res, cs))
            
            # Push to UI queue
            status = "SENT" if res.success else f"BLOCKED ({res.ethics_decision})"
            log_msg = f"[{datetime.now().strftime('%H:%M:%S')}] PKT {i:03d} | {res.symbol.upper():<8} | CS: {cs:.2f} | Latency: {res.latency_ms:4.1f}ms | {status}"
            self.log_queue.put(("STREAM", log_msg))
            
            # Update Metrics calculation
            if i % 2 == 0: # Update metrics every 2 packets for performance
                self._update_metrics_live(results)
            
            time.sleep(0.05) # Mimic stream rate
            
        self.log_queue.put(("Pipeline", "Benchmark Completed."))
        self.root.after(0, lambda: self.run_btn.config(state="normal"))
        self.is_running = False

    def _run_pytest(self):
        self.test_btn["state"] = "disabled"
        self.test_total_var.set("...")
        self.test_pass_var.set("...")
        self.test_fail_var.set("...")
        self.test_cov_var.set("...")
        
        self.test_log_area.delete("1.0", tk.END)
        self.test_log_area.insert(tk.END, ">>> Initiating python -m pytest tests/ --cov=src/ ...\n\n")
        
        def run():
            cflags = 0x08000000 if os.name == 'nt' else 0 # CREATE_NO_WINDOW
            cmd = [sys.executable, "-m", "pytest", "tests/", "--cov=src/", "--cov-report=term-missing"]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     text=True, bufsize=1, universal_newlines=True,
                                     creationflags=cflags)
            
            full_out = ""
            if process.stdout:
                for line in process.stdout:
                    self.log_queue.put(("TEST_LOG", line))
                    full_out += line
            
            process.wait()
            
            # Parse results
            pass_match = re.search(r"(\d+) passed", full_out)
            fail_match = re.search(r"(\d+) failed", full_out)
            err_match = re.search(r"(\d+) error", full_out)
            cov_match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+%)", full_out) # Better cov regex for term-missing
            if not cov_match:
                cov_match = re.search(r"Total coverage: (\d+\.?\d*%)", full_out)

            n_pass = int(pass_match.group(1)) if pass_match else 0
            n_fail = (int(fail_match.group(1)) if fail_match else 0) + (int(err_match.group(1)) if err_match else 0)
            n_total = n_pass + n_fail
            cov_val = cov_match.group(1) if cov_match else "N/A"
            
            self.log_queue.put(("TEST_SUMMARY", (n_total, n_pass, n_fail, cov_val)))
            self.log_queue.put(("TEST_LOG", f"\n[INFO] Test suite exited with code {process.returncode}\n"))
            self.root.after(0, lambda: self.test_btn.config(state="normal"))

        threading.Thread(target=run, daemon=True).start()

    def _update_metrics_live(self, results):
        if not results: return
        
        latencies = [r.latency_ms for r, cs in results]
        latencies.sort()
        n = len(latencies)
        p95 = latencies[int(n*0.95)] if n > 0 else 0
        
        success_rate = (sum(1 for r, cs in results if r.success) / n) * 100
        ethics_rate = (sum(1 for r, cs in results if r.ethics_decision == 'ALLOW') / n) * 100
        avg_consent = sum(cs for r, cs in results) / n
        
        # Get DAFT pass rate and PMI from pipeline metrics
        daft_rate = self.pipeline.metrics.daft_pass_rate() * 100
        pmi_data = self.pipeline.metrics.compute_pmi()
        pmi_score = pmi_data["overall"]
        
        self.log_queue.put(("METRIC", (f"{p95:.1f} ms", f"{avg_consent:.2f}", f"{success_rate:.1f}%", f"{daft_rate:.1f}%", f"{ethics_rate:.1f}%", f"{pmi_score}")))

    def _write_log(self, category, msg):
        self.log_queue.put((category, msg))

    def _process_logs(self):
        try:
            while True:
                category, msg = self.log_queue.get_nowait()
                if category == "METRIC":
                    p95, consent, succ, daft, eth, pmi = msg
                    self.m_p95.set(p95)
                    self.m_consent.set(consent)
                    self.m_success.set(succ)
                    self.m_daft.set(daft)
                    self.m_ethics.set(eth)
                    self.m_pmi.set(pmi)
                elif category == "STREAM":
                    self.log_area.insert(tk.END, f"{msg}\n")
                    self.log_area.see(tk.END)
                elif category == "TEST_LOG":
                    self.test_log_area.insert(tk.END, msg)
                    self.test_log_area.see(tk.END)
                elif category == "TEST_SUMMARY":
                    total, passed, failed, cov = msg
                    self.test_total_var.set(str(total))
                    self.test_pass_var.set(str(passed))
                    self.test_fail_var.set(str(failed))
                    self.test_cov_var.set(str(cov))
                    
                    if int(failed) > 0:
                        self.test_log_area.insert(tk.END, f"\n❌ ตรวจพบข้อผิดพลาด {failed} จุด! กรุณาตรวจสอบรายละเอียดด้านบน\n")
                    else:
                        self.test_log_area.insert(tk.END, "\n✨ การทดสอบเสร็จสมบูรณ์: ผ่าน 100%\n")
                else:
                    self.log_area.insert(tk.END, f"\n[{category.upper()}] {msg}\n", "bold")
                    self.log_area.see(tk.END)
        except queue.Empty:
            pass
        self.root.after(50, self._process_logs)

if __name__ == "__main__":
    root = tk.Tk()
    app = BrainNetGUI(root)
    root.mainloop()
