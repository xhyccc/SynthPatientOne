---
name: PatientProfileBuilder
description: >
  Given a folder of health records for one patient (any format, any language), produce a complete
  patient profile organized by the standard international hospital department hierarchy. The pipeline:
  (1) converts all records to markdown/PNG via markitdown + OCR, (2) translates non-English content
  to English for reasoning, (3) uses LLM/multimodal models to fill 36 secondary-department HTML
  status tables (time-window snapshot) and history tables (pre-window disease course, with timestamped
  filenames), (4) synthesizes a rich, self-contained profile.html with color-coded badges, clickable
  citations, and a dedicated Unknown Factors Audit. Every step produces medical-audit-grade logs
  (translation.txt, form_filling.txt, profile_gen.txt) for traceability.
---

# Patient Profile Builder

## Overview

Given a folder `{patient_id}/` containing all health records for one patient (in any language),
this skill runs a pipeline that produces `{patient_id}_profile/` — a complete, auditable,
department-organized clinical profile.

### What the Pipeline Produces

```
{patient_id}_profile/
├── raw/                    ← Converted source materials (scripts)
├── status_tables/          ← 36 HTML tables: time-window snapshot per department (LLM)
├── history_tables/         ← Pre-window HTML tables, filename with generation date (LLM)
├── logs/                   ← Medical-audit-grade logs (LLM)
│   ├── translation.txt     ← Every non-English→English translation documented
│   ├── form_filling.txt    ← Every table cell fill decision documented
│   └── profile_gen.txt     ← Synthesis rationale documented
└── profile.html            ← Rich HTML: color badges, clickable citations, collapsible sections (LLM)
```

### Core Principles

1. **Time-window separation:** status_tables = most recent encounter / 6 months. Older values → history_tables, flagged 📅 Deprecated.
2. **Every factual claim in profile.html is a clickable link** to a supporting status or history table.
3. **Nothing fabricated.** ❌ Not Known / 📅 Deprecated / ⚠️ Uncertain all explicit.
4. **Medical-audit-grade logs.** Every translation, every table cell, every Unknown Factors classification is documented in `logs/`.
5. **Multilingual first.** Non-English records are translated to English for reasoning; original text preserved in translation.txt.

## When to Use This Skill

- A clinician needs a complete, structured, auditable overview of a patient with non-English records.
- A referral requires department-by-department known/unknown/deprecated audit.
- Medical audit requires full traceability from record → extracted value → classification → profile.
- Clinical trial eligibility or registry population with multilingual sources.
- Downstream AI/analytics need normalized patient data.

## Department Hierarchy

36 secondary departments across 7 first-tier clinical areas. Full details in `references/department_hierarchy.md`.

| # | First-Tier | Secondary Departments |
|---|---|---|
| 1 | Internal Medicine | Cardiology, Pulmonology, Gastroenterology, Endocrinology, Nephrology, Neurology, Rheumatology, Hematology, Oncology, Infectious Diseases |
| 2 | Surgery | General Surgery, Orthopedic Surgery, Neurosurgery, Cardiothoracic Surgery, Urology, Plastic & Reconstructive, Vascular Surgery |
| 3 | OB/GYN | Obstetrics, Gynecology, Reproductive Endocrinology, Gynecologic Oncology |
| 4 | Pediatrics | General Pediatrics, Neonatology, Pediatric Sub-specialties |
| 5 | Emergency Medicine | Trauma, Toxicology, Pre-hospital Care / EMS |
| 6 | Specialized Clinical | Psychiatry, Ophthalmology, Otolaryngology (ENT), Dermatology |
| 7 | Medical Technology & Ancillary | Radiology/Imaging, Pathology, Laboratory Medicine, Anesthesiology, Rehabilitation/Physical Medicine |

---

## Status Definitions

| Status | Icon | Meaning |
|---|---|---|
| Known | ✅ | Value found within time window, clearly documented |
| Uncertain | ⚠️ | Ambiguous, conflicting, or qualified data within window |
| Deprecated | 📅 | Value exists but is too old — outside time window (see history) |
| Not Known | ❌ | Never mentioned in any available record |

---


---

## Ingest → Audit Handoff Contract

After Phase 1 (ingest), the LLM MUST verify these before beginning Phase 2 audit:

### Checklist
1. **raw/combined_records.md exists** and contains merged text from all source documents.
2. **Language detection is complete** — each document in combined_records.md has a `<language>` tag.
3. **All 36 HTML templates are copied** into status_tables/ (with <!-- FILL_ME --> markers).
4. **All 36 HTML templates are copied** into history_tables/.
5. **logs/ folder exists** with empty translation.txt, form_filling.txt, and profile_gen.txt.

### Handoff Data Structure
The LLM reads raw/combined_records.md as the primary input. Each document section begins with:

```
<document file="{original_filename}" language="{detected_language}" confidence="{0-100}">
{full extracted text}
</document>
```

If language is not English, the LLM MUST translate before filling tables and log the translation in `logs/translation.txt`.

### Failure Modes
- If combined_records.md is empty: re-run Phase 1 with --ocr flag.
- If languages tag shows non-English: translation to English is REQUIRED before audit. Log all translations to logs/translation.txt.
- If status_tables/ has fewer than 36 files: re-run Phase 2.

## Pipeline Phases

### Phase 1 — INGEST (scripts)

Convert all original records in `{patient_id}/` into normalized markdown and PNG under `{patient_id}_profile/raw/`. Non-English text is preserved as-is; translation occurs in Phase 2.

| Input Format | Conversion Method |
|---|---|
| PDF (text-based) | markitdown (primary) → pdfplumber (fallback) → PyMuPDF (fallback) |
| PDF (scanned/image) | PyMuPDF render pages → PNG → Tesseract OCR |
| Word (.docx) | markitdown (primary) → python-docx (fallback) |
| Excel (.xlsx/.csv) | markitdown or pandas |
| Images (JPG/PNG/TIFF) | Pillow → PNG; Tesseract OCR |
| EHR/FHIR/HL7 | Structured parsing → markdown; markitdown fallback |

### Phase 2 — AUDIT (LLM-driven)

Fill the 36 department HTML tables using ONLY what is found in `raw/`. LLM-only phase with mandatory audit logging.

#### 2a. Translation (→ `logs/translation.txt`)

1. Detect non-English content in `raw/` — Chinese (中文), Japanese (日本語), French, German, Spanish, Korean, etc.
2. Translate ALL non-English clinical text to English for reasoning.
3. Log every translation: `[source_file] [line] [language] → original → English (confidence%)`.
4. Medical terminology preserved with high fidelity.

#### 2b. Status Tables (→ `status_tables/*.html` + `logs/form_filling.txt`)

Fill the 36 HTML templates (pre-built with `<!-- FILL_ME: ... -->` markers):

1. Determine time window (latest encounter / admission / 6 months).
2. Fill ONLY in-window values into the HTML templates.
3. Values outside window → 📅 Deprecated, cross-reference history.
4. Not mentioned → ❌ Not Known. Conflict → ⚠️ Uncertain.
5. **For every filled cell, log to form_filling.txt**: table, row, variable, extracted value, unit conversion, Value Age calculation, status reasoning, source citation.
6. Remove `<!-- FILL_ME: ... -->` comments after filling.

#### 2c. History Tables (→ `history_tables/*_{date}.html` + `logs/form_filling.txt`)

For departments with temporal history:

1. Document pre-window events in reverse chronological order.
2. Use `value_deprecated` event type for stale values.
3. Log each row to form_filling.txt.
4. Rename file: `{department}_{YYYY-MM-DD}.html`.
5. Delete templates for departments with no history.

### Phase 3 — SYNTHESIS (LLM-driven)

Write `profile.html` — self-contained HTML with:
1. Demographics & completeness bar.
2. Current Clinical Status (collapsible per department, color-coded badges).
3. **Unknown Factors Audit**: 📅 Deprecated | ❌ Critical Unknowns | ⚠️ Uncertainties | ❌ Routine Unknowns | By-Department Completeness table.
4. **🔍 Potential Missing Diagnoses**: Conditions not formally documented but strongly suggested by the clinical picture — list each with estimated probability, the evidence pattern supporting it (e.g., constellation of symptoms, lab abnormalities, risk factors), the diagnostic pathway to confirm or exclude it, and the clinical impact if the diagnosis is present and missed.
5. **📈 Disease Progression Trajectories**: For each active condition, project the expected evolution over 3, 6, and 12 months — classify as Stable / Likely Progressive / High Risk of Acute Decompensation. For each trajectory, specify: what would trigger re-escalation, what early warning signs to monitor, and what preventive interventions could alter the trajectory.
6. **⚠️ Diagnostic Reliability Flags**: Identify tests or diagnoses in the profile that carry a material risk of measurement error, misclassification, or pre-analytical confounding in this specific clinical context. For each flag: state the known limitation, estimate the false-positive/negative risk, and recommend the confirmatory step before major clinical decisions are made.
7. Clinical History (timeline + per-department).
8. Cross-Department Synthesis.
9. Priority Action Items.

**Log to `logs/profile_gen.txt`**: Unknown Factors classification rationale, deprecated value decisions, critical-vs-routine judgments, cross-department linking, completeness calculations. Also document the reasoning for every entry in sections 4–6: why a potential missing diagnosis was raised (evidence trail), the basis for each progression trajectory estimate (natural history data, risk scores, current severity), and every diagnostic reliability flag with the specific test limitation cited.

---

## Output Folder Contract

```
{patient_id}_profile/
├── raw/                              # Phase 1 (scripts)
├── status_tables/                    # Phase 2a (LLM) — HTML, time-window snapshot
├── history_tables/                   # Phase 2b (LLM) — HTML, date-stamped
├── logs/                             # Phase 2+3 (LLM) — audit trail
│   ├── translation.txt
│   ├── form_filling.txt
│   └── profile_gen.txt
└── profile.html                      # Phase 3 (LLM) — rich HTML synthesis
```

---

## Quick Start

```bash
# Phase 1
python scripts/run_pipeline.py {patient_id} --phase 1 --ocr

# Phases 2 & 3: LLM agent fills tables, writes logs, produces profile.html
```

---

## References

| Reference | Content |
|---|---|
| `references/department_hierarchy.md` | Full 36-department hierarchy with expected clinical variables |
| `references/output_spec.md` | Output folder structure, HTML table format, status definitions, time-window rules, logs specification, multilingual handling |
| `references/output_template.md` | Legacy profile layout template |
| `references/templates/status_tables_html/` | 36 HTML status-table templates with `<!-- FILL_ME -->` markers |
| `references/templates/history_tables_html/` | 36 HTML history-table templates |

## Scripts

| Script | Purpose |
|---|---|
| `scripts/run_pipeline.py` | Orchestrator. Phase 1 ingest, copies HTML templates, creates logs/, prints LLM instructions |
| `scripts/ingest_documents.py` | Convert PDF/Word/Excel/Images to markdown via markitdown + fallbacks |
| `scripts/ocr_images.py` | Screenshot→PNG + Tesseract OCR |
| `scripts/multimodal_analyze.py` | Claude Vision / GPT-4o medical image analysis |
| `scripts/build_profile.py` | Assemble profile from JSON (markdown/JSON/HTML) |

## Assets

| Asset | Content |
|---|---|
| `assets/profile_template.md` | Reusable markdown template |

## Dependencies

```bash
pip install markitdown pdfplumber PyMuPDF pillow pytesseract python-docx pandas openpyxl
# Optional for multimodal:
pip install anthropic openai
```

System: [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (`brew install tesseract`).

## Best Practices

1. **Time-window discipline.** status_tables = current episode; history_tables = backstory.
2. **Never fabricate.** ❌ / 📅 / ⚠️ used explicitly.
3. **Every claim links to a source.** profile.html has zero orphan statements.
4. **All links relative.**
5. **Audit everything.** translation.txt, form_filling.txt, profile_gen.txt must be comprehensive.
6. **Multilingual → English.** Translate for reasoning; log originals.
7. **Preserve units and reference ranges.**
8. **Deprecated values include old value + date + re-measurement recommendation.**
9. **Handle conflicts transparently.**
10. **No department skipped.**
11. **Medical images flagged for human review.**
12. **History files only when there IS history.**

## Limitations

- OCR quality depends on scan resolution.
- Translation quality depends on LLM capability for medical terminology.
- Medical images are flagged for human review.
- Multimodal analysis requires API keys and incurs cost.
- Department naming follows international standard.
