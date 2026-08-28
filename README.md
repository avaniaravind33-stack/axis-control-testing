# Axis Bank Control Testing & Compliance Dashboard

**Professional Internal Audit & Control Testing Simulation**

A comprehensive control testing framework demonstrating design and operating effectiveness assessment for banking operations.

## 🎯 Project Overview

This project showcases **internal audit and compliance control testing** through a realistic Axis Bank scenario with 15,000 simulated transactions and professional control testing workpapers.

### What It Demonstrates

✅ **Control Design Effectiveness** — Does the control, as designed, address the identified risk?  
✅ **Operating Effectiveness** — Did the control actually operate consistently during the test period?  
✅ **Control Testing Framework** — Sample selection, test procedures, evidence gathering, exception identification  
✅ **Audit Vocabulary** — Deficiency classification (Critical/Major/Minor), control ownership, risk ratings  
✅ **Professional Compliance** — Realistic failure rates, regulatory considerations, SLA compliance  

## 🔄 Control Testing Methodology

This project demonstrates a **complete control testing lifecycle**, not just exception detection:

```
┌─────────────────┐
│ Risk Identified │
└────────┬────────┘
         ↓
┌──────────────────────┐
│ Control Objective    │ (What risk does this control address?)
└────────┬─────────────┘
         ↓
┌──────────────────────────────┐
│ Design Effectiveness         │ (Is the control design adequate?)
│ Assessment                   │
└────────┬─────────────────────┘
         ↓
┌──────────────────────────────┐
│ Test Procedure Developed     │ (How will we test it?)
└────────┬─────────────────────┘
         ↓
┌──────────────────────────────┐
│ Sample Selection             │ (What transactions to test?)
└────────┬─────────────────────┘
         ↓
┌──────────────────────────────┐
│ Evidence Review              │ (Did control operate correctly?)
└────────┬─────────────────────┘
         ↓
┌──────────────────────────────┐
│ Operating Effectiveness      │ (Did it work consistently?)
│ Assessment (15,000 txns)     │
└────────┬─────────────────────┘
         ↓
┌──────────────────────────────┐
│ Exceptions Identified        │ (What failed? How many?)
└────────┬─────────────────────┘
         ↓
┌──────────────────────────────┐
│ Deficiency Classification    │ (Critical/Major/Minor?)
└────────┬─────────────────────┘
         ↓
┌──────────────────────────────┐
│ Risk Rating & Root Cause     │ (Why did it fail?)
└────────┬─────────────────────┘
         ↓
┌──────────────────────────────┐
│ Remediation Actions          │ (How to fix it?)
│ & Management Reporting       │
└──────────────────────────────┘
```

**This is different from "finding bad transactions."** We're assessing whether controls, as designed, adequately address risks (design effectiveness) AND whether they actually operated consistently (operating effectiveness).

---

## 📊 Controls Tested

### Five Core Controls

| Control ID | Control Name | Risk Addressed | Control Type |
|-----------|------------|-----------------|------------|
| **C001** | Maker/Checker Approval | Unauthorized transactions | Preventive |
| **C002** | Authorization Limit Compliance | Excess authorization | Preventive |
| **C003** | Segregation of Duties | Fraud/Override | Preventive |
| **C004** | 4-Eyes Principle | Unauthorized high-value txns | Preventive |
| **C005** | Duplicate Detection | Duplicate processing | Detective |

### Testing Results Summary

- **Total Transactions Tested**: 15,000
- **Overall Compliance Rate**: 98.45%
- **Exception Rate**: 1.55%
- **Critical Deficiencies**: 73 (0.49%)
- **Major Deficiencies**: 111 (0.74%)
- **Minor Deficiencies**: 48 (0.32%)

## 📁 Deliverables

### 1. Synthetic Dataset (`data/control_testing_transactions.csv`)
- 15,000 transactions with embedded control testing attributes
- Realistic transaction types: Fund Transfer, Cheque Processing, Remittance, Standing Order, Sweep
- Multiple channels: Branch, ATM, Online, Mobile, SWIFT
- Officer hierarchy with role-based authorization limits
- Built-in control failure scenarios (2-3% realistic failure rates)

### 2. Excel Control Testing Workpapers (`excel/Axis_Control_Testing_Workpapers.xlsx`)

**4 Professional Worksheets:**

1. **Control Summary**
   - Control definitions and ownership
   - Risk addressed by each control
   - Testing statistics and compliance metrics

2. **Test Results**
   - Sample of 100 transactions with detailed test results
   - Control-wise pass/fail indicators
   - Exception tracking

3. **Exceptions & Deficiencies**
   - Exception analysis by control
   - Deficiency breakdown
   - Root cause identification

4. **Effectiveness Assessment**
   - Design Effectiveness evaluation
   - Operating Effectiveness testing results
   - Control ratings and recommendations

### 3. Professional Web Dashboard (`website/index.html`)

**Live Analytics with:**
- 6 KPI cards: Transactions tested, compliance rate, deficiency breakdown
- 6 Interactive Plotly charts:
  - Deficiency Classification Breakdown
  - Control Operating Effectiveness (%)
  - Risk Heat Map (Control vs Deficiency)
  - Daily Transaction Volume Trend
  - Daily Exception Trend
  - Exceptions by Transaction Type
- Modern dark theme with Axis Bank branding
- Responsive design (mobile-friendly)
- Professional audit-grade styling

### 3. Professional Web Dashboard (`website/index.html`)

**Live Analytics with:**
- 6 KPI cards: Transactions tested, compliance rate, deficiency breakdown
- 6 Interactive Plotly charts:
  - Deficiency Classification Breakdown
  - Control Operating Effectiveness (%)
  - Risk Heat Map (Control vs Deficiency)
  - Daily Transaction Volume Trend
  - Daily Exception Trend
  - Exceptions by Transaction Type
- Modern dark theme with Axis Bank branding
- Responsive design (mobile-friendly)
- Professional audit-grade styling

### 4. Control Testing Findings Report (`excel/Control_Testing_Findings_Report.xlsx`)

**Professional Management-Level Report with 3 Worksheets:**

1. **Management Summary** (One-Page Executive View)
   - Controls tested: 5
   - Transactions analyzed: 15,000
   - Exceptions identified: 232
   - Critical/High/Medium risk breakdown
   - Top 3 control weaknesses with exception counts
   - Recommended remediation actions with ownership
   - Risk assessment summary

2. **Findings Detail** (Complete Finding Records)
   - Finding ID, Control, Risk, Evidence
   - Deficiency classification (Critical/Major/Minor)
   - Severity-coded color highlighting
   - Root cause analysis for each finding
   - Specific recommendations for remediation
   - Owner assignment and status tracking
   - Days open / overdue tracking

3. **Exception Summary** (Control-by-Control Breakdown)
   - Pass/fail counts by control
   - Exception rate percentages
   - Top reason for each control failure
   - Remediation status for each control

## 🚀 Live Dashboard

**Visit**: https://avaniaravind33-stack.github.io/axis-control-testing/

## 💼 Why This Project?

### Direct JD Alignment

Your JD likely requires:
- ✅ Control Testing Experience
- ✅ Design & Operating Effectiveness Assessment
- ✅ Internal Audit Knowledge
- ✅ Compliance Monitoring
- ✅ Professional Audit Vocabulary

### What You Get

**Without false claims**, you can now discuss:

1. **Control Design**
   - "I've evaluated controls for design effectiveness, assessing whether they address identified risks..."

2. **Control Testing**
   - "I've developed test procedures, selected samples, and evaluated operating effectiveness..."

3. **Deficiency Classification**
   - "I've classified control deficiencies as Critical, Major, or Minor based on impact..."

4. **Professional Framework**
   - "I use a structured testing approach: Define control, Identify risks, Design tests, Execute tests, Report findings..."

## 📊 Realistic Failure Scenarios

The dataset includes realistic control failures:

- **C001 (Maker/Checker)**: 73 transactions missing independent approval (0.49%)
- **C002 (Auth Limits)**: 168 transactions exceeding officer limits (1.12%)
- **C003 (SOD)**: Ensures different makers and checkers
- **C004 (4-Eyes)**: 17 high-value txns without dual approval (0.11%)
- **C005 (Duplicates)**: 89 potential duplicates detected (0.59%)

## 🛠️ Technical Stack

- **Data Generation**: Python (numpy, pandas, faker)
- **Excel Workpapers**: openpyxl
- **Web Dashboard**: Plotly + HTML5/CSS3
- **Deployment**: GitHub Pages
- **CI/CD**: GitHub Actions (automated daily refresh)

## 📈 How to Use

### Generate All Artifacts

```bash
# Install dependencies
pip install -r requirements.txt

# Generate control testing data
python scripts/generate_control_data.py

# Create Excel workpapers
python scripts/generate_workpapers.py

# Build web dashboard
python scripts/generate_dashboard.py
```

### Outputs

- `data/control_testing_transactions.csv` — 15,000 test transactions
- `excel/Axis_Control_Testing_Workpapers.xlsx` — Professional audit workpapers
- `website/index.html` — Interactive dashboard (deploy to GitHub Pages)

## 📚 Audit Terminology Included

- ✅ Design Effectiveness
- ✅ Operating Effectiveness
- ✅ Test Procedures
- ✅ Sample Selection (Statistical)
- ✅ Control Exceptions
- ✅ Deficiency Classification
- ✅ Risk Ratings
- ✅ Control Ownership
- ✅ Evidence Gathering
- ✅ Audit Findings

## 🎓 Portfolio Impact

This project demonstrates:

**Technical Skills**:
- Full-stack data pipeline (generation → Excel → Web)
- Professional Excel workpaper development
- Interactive analytics dashboards
- Automated CI/CD deployment

**Domain Knowledge**:
- Internal audit methodology
- Control testing frameworks
- Compliance monitoring
- Financial risk assessment
- Banking operations

**Professional Skills**:
- Technical documentation
- Audit findings presentation
- Stakeholder communication
- Control design thinking

## 🔗 GitHub Repository

https://github.com/avaniaravind33-stack/axis-control-testing

## ✨ What Makes This Special

Instead of just showing "I tested a control," you're showing:

1. **A complete control testing framework**
2. **Professional audit workpapers**
3. **15,000 realistic transactions with embedded control scenarios**
4. **Quantified effectiveness metrics**
5. **Professional audit-grade dashboards**
6. **Correct terminology and methodology**

**This is what separates candidates who talk about audits from candidates who understand them.**

---

**Built for**: Axis Bank | Competitive Audit/Compliance Roles | Professional Portfolio  
**Status**: Production Ready | Deployed to GitHub Pages | Automated Daily Refresh

