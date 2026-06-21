# SynthPatientOne

A four-skill pipeline for synthetic patient profiling, multidisciplinary team simulation,
patient data simulation, and MDT evaluation.

## Overview

SynthPatientOne takes real or mock patient health records and produces:

1. A complete, auditable **patient profile** organized by 36 clinical departments
2. A simulated **multidisciplinary team (MDT) review** with consensus decision
3. **N simulated patient completions** where unknown data is clinically predicted
4. An **MDT evaluation** testing the MDT's decisions against all N simulated realities

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SynthPatientOne Pipeline                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  patient_001/  (raw records)                                     │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────────────┐                                        │
│  │ PatientProfileBuilder │  Phase 1: markitdown + OCR → raw/     │
│  │                      │  Phase 2-3: LLM fills 36 HTML tables   │
│  └──────────┬───────────┘                                        │
│             │                                                    │
│             ▼                                                    │
│  patient_001_profile/                                            │
│  ├── status_tables/ (36 HTML, time-window snapshot)              │
│  ├── history_tables/ (pre-window events)                         │
│  ├── logs/ (translation, form_filling, profile_gen)              │
│  └── profile.html                                                │
│       │                    │                                     │
│       ▼                    ▼                                     │
│  ┌────────────┐    ┌──────────────────┐                          │
│  │ MDTBuilder  │    │ PatientSimulator  │                         │
│  │ (5-phase    │    │ (N independent    │                         │
│  │  MDT review)│    │  predictions)     │                         │
│  └─────┬──────┘    └────────┬─────────┘                          │
│        │                    │                                     │
│        ▼                    ▼                                     │
│  patient_001_profile/   patient_001_simulation/                   │
│  └── mdt/               ├── simulation_tables_1..N/               │
│      ├── consensus.html ├── profile_simulation_1..N.html          │
│      └── ...            └── logs/                                 │
│        │                    │                                     │
│        └────────┬───────────┘                                     │
│                 ▼                                                 │
│          ┌──────────────┐                                         │
│          │   MDTEval     │  Evaluate MDT against N simulations    │
│          └──────┬───────┘                                         │
│                 ▼                                                 │
│          patient_001_MDT_eval/                                    │
│          ├── per_simulation/                                      │
│          ├── aggregate_report.html                                │
│          └── score_matrix.json                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Skills

| # | Skill | Type | Input | Output |
|---|---|---|---|---|
| 1 | `PatientProfileBuilder` | Script + LLM | Raw records folder | `{id}_profile/` |
| 2 | `MDTBuilder` | Pure LLM | `{id}_profile/` | `{id}_profile/mdt/` |
| 3 | `PatientSimulator` | Pure LLM | `{id}_profile/` | `{id}_simulation/` |
| 4 | `MDTEval` | Pure LLM | `{id}_simulation/` + `{id}_profile/mdt/` | `{id}_MDT_eval/` |

## Quick Start

### Prerequisites

```bash
pip install markitdown pdfplumber PyMuPDF pillow pytesseract python-docx pandas openpyxl
brew install tesseract  # macOS
```

### Smoke Test

```bash
# Phase 1: Convert mock records to markdown
python PatientProfileBuilder/scripts/run_pipeline.py patient_smoke_test --phase 1

# Phase 2: Set up HTML templates and logs
python PatientProfileBuilder/scripts/run_pipeline.py patient_smoke_test --phase 2

# Verify output
ls patient_smoke_test_profile/
# → raw/  status_tables/  history_tables/  logs/
```

### Full Pipeline (LLM required for Phases 2-3)

```
1. @PatientProfileBuilder on patient_001/
   → produces patient_001_profile/

2. @MDTBuilder on patient_001_profile/
   → produces patient_001_profile/mdt/

3. @PatientSimulator on patient_001_profile/ --N 20
   → produces patient_001_simulation/

4. @MDTEval on patient_001_simulation/ + patient_001_profile/mdt/
   → produces patient_001_MDT_eval/
```

## Mock Patient Data

`patient_smoke_test/` contains a realistic mock patient with:
- Discharge summary (COPD exacerbation, hypertension, diabetes)
- Lab results (HbA1c, lipids, troponins, CBC, metabolic panel)
- Referral letter (pulmonology)

## Department Coverage

36 secondary departments across 7 first-tier clinical areas:
Internal Medicine (10), Surgery (7), OB/GYN (4), Pediatrics (3),
Emergency Medicine (3), Specialized Clinical (4), Medical Technology & Ancillary (5).

Each department contributes ~10-25 pre-defined clinical variables with expected ranges.

## Status Badges

| Badge | Meaning |
|---|---|
| ✅ Known | Confirmed value within time window |
| ⚠️ Uncertain | Ambiguous or conflicting data |
| 📅 Deprecated | Value exists but too old |
| ❌ Not Known | Never documented |
| 🔮 Simulated | Predicted by PatientSimulator |

## Key Design Principles

1. **Time-window separation:** status_tables = recent clinical episode; history_tables = everything before.
2. **Audit trails everywhere:** translation.txt, form_filling.txt, profile_gen.txt, simulation logs, eval logs.
3. **Reproducibility:** every simulation and evaluation has a unique seed.
4. **Pure LLM reasoning where possible:** MDTBuilder, PatientSimulator, and MDTEval have zero scripts — the LLM reads, reasons, and writes directly.
5. **Relative path citations:** every claim links to its source file.
6. **Multilingual support:** non-English records are detected (CJK, Cyrillic, Arabic, Latin-ext) and translated to English for reasoning, with full translation audit logs.

## File Count

| Skill | Files |
|---|---|
| PatientProfileBuilder | 5 Python scripts + 72 HTML templates + 4 docs |
| MDTBuilder | 3 docs + 1 HTML template |
| PatientSimulator | 3 docs + 1 HTML template |
| MDTEval | 3 docs + 1 HTML template |
