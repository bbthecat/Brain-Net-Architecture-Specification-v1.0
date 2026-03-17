# 📁 Brain-Net GitHub Repository Setup Guide
**คู่มือการ Push ไฟล์ทั้งหมดขึ้น GitHub**

---

## 🗂️ โครงสร้างไฟล์ทั้งหมดที่ต้อง Push ขึ้น GitHub

```
brain-net/                                      ← Root (Repository Name)
│
├── 📄 README.md                               ✅ สร้างแล้ว
├── 📄 CHANGELOG.md                            ✅ สร้างแล้ว
├── 📄 .gitignore                              → สร้างเพิ่ม (Python standard)
├── 📄 requirements.txt                        → สร้างเพิ่ม
│
├── 📁 docs/
│   ├── 📁 architecture/
│   │   └── 📄 ARCHITECTURE.md                ✅ (จากไฟล์เดิม)
│   │
│   ├── 📁 planning/
│   │   ├── 📄 RESPONSIBILITIES.md            ✅ (จากไฟล์เดิม)
│   │   ├── 📄 IMPLEMENTATION_PLAN.md         ✅ (จากไฟล์เดิม)
│   │   ├── 📄 SPRINT-1-FIRST-WHISPER.md      ✅ (จากไฟล์เดิม)
│   │   ├── 📄 SPRINT-2-SIGNAL-BRIDGE.md      → สร้างเพิ่ม (ถ้ามี)
│   │   ├── 📄 SPRINT-3-DEEP-CALIBRATION.md   ✅ สร้างแล้ว (ใหม่)
│   │   └── 📄 SPRINT-4-MVP-FINAL.md          ✅ สร้างแล้ว (ใหม่)
│   │
│   ├── 📁 ethics/
│   │   ├── 📄 COGNITIVE_LIBERTY.md           ✅ สร้างแล้ว
│   │   ├── 📄 COMPLIANCE_MATRIX.md           → สร้างใน Sprint 3
│   │   └── 📄 DATA_GOVERNANCE.md             → สร้างใน Sprint 4
│   │
│   └── 📁 metrics/
│       ├── 📄 QUALITY_METRICS.md             ✅ สร้างแล้ว
│       └── 📄 FINAL_BENCHMARK_REPORT.md      → สร้างใน Sprint 4
│
├── 📁 src/
│   ├── 📁 bci/
│   │   ├── connect_bci.py                    → Sprint 1
│   │   ├── clean_eeg_data.py                 → Sprint 1
│   │   └── neural_classifier.py              → Sprint 1–3
│   │
│   ├── 📁 protocol/
│   │   ├── ttp_packet.py                     → Sprint 1
│   │   ├── ttp_router.py                     → Sprint 1
│   │   ├── context_frame.py                  → Sprint 1
│   │   └── virtual_network.py                → Sprint 2
│   │
│   ├── 📁 security/
│   │   ├── brain_firewall.py                 → Sprint 1
│   │   ├── consensual_handshake.py           → Sprint 2
│   │   ├── ethics_rule_engine.py             → Sprint 3
│   │   ├── hitl_checkpoint.py                → Sprint 3
│   │   └── audit_log.py                      → Sprint 3
│   │
│   ├── 📁 crypto/
│   │   └── mock_qkd_aes.py                   → Sprint 1
│   │
│   ├── 📁 daft/                              → Sprint 3 (ใหม่)
│   │   ├── domain_interface.py
│   │   ├── math_symbol.py
│   │   └── daft_validator.py
│   │
│   ├── 📁 metrics/                           → Sprint 3 (ใหม่)
│   │   └── quality_metrics.py
│   │
│   ├── 📁 dashboard/                         → Sprint 3 (ใหม่)
│   │   └── hitl_cli.py
│   │
│   └── 📁 pipeline/                          → Sprint 4 (ใหม่)
│       └── brain_net_pipeline.py
│
├── 📁 models/
│   ├── neural_dict_v1.pkl                    → Sprint 1
│   └── neural_dict_v2.pkl                    → Sprint 3
│
├── 📁 data/
│   ├── clean_eeg_data.csv                    → Sprint 1
│   └── multi_domain_dataset.csv              → Sprint 3
│
├── 📁 tests/
│   ├── 📁 unit/
│   │   ├── test_ttp.py
│   │   ├── test_firewall.py
│   │   ├── test_daft.py
│   │   └── test_ml_classifier.py
│   ├── 📁 integration/
│   │   ├── test_pipeline_integration.py
│   │   └── test_ethics_engine.py
│   └── 📁 e2e/
│       └── test_e2e_transmission.py
│
└── 📁 .github/
    └── 📁 workflows/
        └── ci.yml                            → GitHub Actions CI/CD
```

---

## 🚀 ขั้นตอน Push ไฟล์ขึ้น GitHub

### Step 1: สร้าง Repository บน GitHub

1. ไปที่ [github.com](https://github.com) → New Repository
2. Repository Name: `Brain-Net-Architecture-Specification-v1.0`
3. Description: `Brain-Net: Mind-to-Mind Network Protocol — Phase 1: Synthetic Telepathy`
4. Visibility: **Private** (แนะนำ เพราะมีข้อมูล Ethics sensitive)
5. ✅ Add README file: **ไม่ต้อง** (มีแล้ว)
6. Click **Create Repository**

### Step 2: Clone และ Setup Local

```bash
# Clone repository ที่เพิ่งสร้าง
git clone https://github.com/bbthecat/Brain-Net-Architecture-Specification-v1.0.git
cd brain-net

# ตรวจสอบว่า Git ตั้งค่าถูกต้อง
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Step 3: วาง File Structure

```bash
# สร้างโครงสร้างโฟลเดอร์
mkdir -p docs/architecture docs/planning docs/ethics docs/metrics
mkdir -p src/bci src/protocol src/security src/crypto src/daft src/metrics src/dashboard src/pipeline
mkdir -p models data
mkdir -p tests/unit tests/integration tests/e2e
mkdir -p .github/workflows

# วางไฟล์ที่สร้างไว้ทั้งหมดลงในโครงสร้าง
# (copy ไฟล์จาก brain-net/ folder ที่ได้รับมา)
```

### Step 4: สร้าง .gitignore

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.eggs/

# Virtual environments
venv/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Data & Models (large files — ใช้ Git LFS หรือ exclude)
data/*.csv
models/*.pkl

# Secrets & Keys
*.key
*.pem
.env
secrets/

# OS
.DS_Store
Thumbs.db

# Test & Coverage
.coverage
htmlcov/
.pytest_cache/

# Logs
*.log
logs/
EOF
```

### Step 5: สร้าง requirements.txt

```bash
cat > requirements.txt << 'EOF'
scikit-learn>=1.3.0
numpy>=1.24.0
mne>=1.5.0
cryptography>=41.0.0
pytest>=7.4.0
pytest-cov>=4.1.0
pandas>=2.0.0
matplotlib>=3.7.0
EOF
```

### Step 6: สร้าง GitHub Actions CI/CD

```bash
cat > .github/workflows/ci.yml << 'EOF'
name: Brain-Net CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python 3.10
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests with coverage
      run: |
        pytest tests/ --cov=src/ --cov-report=xml --cov-fail-under=80
    
    - name: Ethics Rule Check
      run: |
        python src/security/ethics_rule_engine.py --verify-all
EOF
```

### Step 7: Git Add, Commit, Push

```bash
# Add ทุกไฟล์
git add .

# Commit ครั้งแรก
git commit -m "feat: Initial Brain-Net repository setup

- Add README.md with full project overview
- Add CHANGELOG.md with Sprint 1-4 history
- Add ARCHITECTURE.md (Brain-Net Protocol Stack v1.0)
- Add RESPONSIBILITIES.md (RACI Matrix & Role Boundaries)
- Add IMPLEMENTATION_PLAN.md
- Add Sprint 1 Execution Plan (First Whisper)
- Add Sprint 3 Execution Plan (Deep Calibration) - NEW
- Add Sprint 4 MVP Plan (Final Whisper) - NEW
- Add COGNITIVE_LIBERTY.md (Ethics Framework v1.0)
- Add QUALITY_METRICS.md (PMI Definition & Scoring)
- Add CI/CD GitHub Actions workflow"

# Push ขึ้น GitHub
git push origin main
```

### Step 8: สร้าง Branches สำหรับ Sprint 3

```bash
# สร้าง develop branch
git checkout -b develop
git push origin develop

# สร้าง feature branches สำหรับ Sprint 3
git checkout -b feat/BNET-501-domain-interface
git push origin feat/BNET-501-domain-interface

git checkout develop
git checkout -b feat/BNET-503-daft-validator
git push origin feat/BNET-503-daft-validator
```

### Step 9: ตั้งค่า Branch Protection Rules

ไปที่ GitHub Repository → Settings → Branches:

1. **main branch:**
   - ✅ Require pull request before merging
   - ✅ Require 2 approvals (Network Architect + Neuroethics Lead)
   - ✅ Require status checks (CI must pass)
   - ✅ Do not allow bypassing

2. **develop branch:**
   - ✅ Require 1 approval
   - ✅ Require CI to pass

---

## 📋 Git Commit Message Convention

```
<type>: <subject>

Types:
  feat     → Feature ใหม่
  fix      → แก้บั๊ก
  docs     → เอกสารเท่านั้น
  test     → เพิ่ม/แก้ Test
  refactor → Refactor โค้ด (ไม่ใช่ feature/fix)
  perf     → ปรับปรุง Performance
  ethics   → การเปลี่ยนแปลงที่เกี่ยวกับ Ethics Rules

ตัวอย่าง:
  feat(BNET-501): add DomainInterface class with 4 domain mappers
  fix(ISS-001): improve ML accuracy to 85% with multi-domain training
  docs: update Sprint 3 execution plan
  ethics(BNET-702): implement automated Ethics Rule Engine
  test(BNET-604): add regression test suite for DAFT module
```

---

## 🏷️ Release Tagging Strategy

```bash
# Sprint milestones
git tag -a v1.0 -m "Sprint 1 Delivery: First Whisper"
git tag -a v2.0 -m "Sprint 2 Delivery: Signal Bridge"
git tag -a v3.0 -m "Sprint 3 Delivery: Deep Calibration"
git tag -a v1.0-mvp -m "Sprint 4 MVP: Final Whisper — Brain-Net Phase 1 Complete"

# Push tags
git push origin --tags
```

---

*คู่มือ GitHub Setup | Brain-Net Project*
