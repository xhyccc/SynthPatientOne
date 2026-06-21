# Patient Profile Output Specification

## Output Folder Structure

Given a patient identifier `{patient_id}`, the pipeline produces:

```
{patient_id}_profile/
├── raw/                              # Converted source materials (Phase 1)
│   ├── combined_records.md           # All extracted text merged chronologically
│   ├── {doc_1}.md                    # Per-document markdown
│   ├── {doc_2}_page_0001.png         # Rendered pages from scanned PDFs
│   └── manifest.json                 # File manifest
├── status_tables/                    # Time-window snapshot tables — HTML (Phase 2a)
│   ├── 1.1_cardiology.html
│   ├── 1.2_pulmonology.html
│   ├── ...
│   └── 7.5_rehabilitation_medicine.html
├── history_tables/                   # Pre-window disease-course events — HTML (Phase 2b)
│   ├── 1.1_cardiology_2025-06-20.html
│   └── ... (only where history exists)
├── logs/                             # Audit trail (Phase 2+3)
│   ├── translation.txt               # Multilingual → English translation log
│   ├── form_filling.txt              # Per-row table filling audit
│   └── profile_gen.txt               # Profile.html generation reasoning
└── profile.html                      # Rich HTML narrative with citations (Phase 3)
```

### Folder Purpose

| Folder | Filled by | Content |
|---|---|---|
| `raw/` | `scripts/ingest_documents.py` | Converted markdown + PNG from original records. Read-only reference. |
| `status_tables/` | LLM (audit step) | **HTML files.** Time-window snapshot per department. One file per secondary department (all 36). |
| `history_tables/` | LLM (audit step) | **HTML files.** Pre-window disease course. Only for departments WITH history. Filename: `{dept}_{YYYY-MM-DD}.html`. |
| `logs/` | LLM (audit + synthesis) | **Plain text audit trail.** Three files documenting every clinical decision. |
| `profile.html` | LLM (synthesis step) | Self-contained, print-friendly HTML narrative. |

---

## HTML Table Format

All `status_tables/` and `history_tables/` output files are **self-contained HTML documents** with inline CSS. Templates are provided in `references/templates/status_tables_html/` and `references/templates/history_tables_html/`.

### Markdown → HTML Conversion Rules

When the LLM fills an HTML template, markdown-style formatting in cell values MUST be converted:

| Markdown | HTML |
|---|---|
| `**bold**` | `<strong>bold</strong>` |
| `*italic*` | `<em>italic</em>` |
| `` `code` `` | `<code>code</code>` |
| `[text](url)` | `<a href="url">text</a>` |
| `—` (em dash) | `—` or `&mdash;` |
| `✅ / ⚠️ / 📅 / ❌` | Keep as Unicode; wrap in `<span class="status-*">` |

### Status Table HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Department — Status Table</title>
<style>
  /* Inline CSS for consistent rendering */
  .status-known { color: #1a7a1a; background: #e6ffe6; }
  .status-uncertain { color: #b8860b; background: #fff8e1; }
  .status-deprecated { color: #666; background: #f0f0f0; }
  .status-notknown { color: #c00; background: #ffe6e6; }
  .fill-me { background: #ffffcc; }  /* ← LLM removes this class after filling */
  table { border-collapse: collapse; width: 100%; }
  th, td { border: 1px solid #ddd; padding: 6px; text-align: left; }
  th { background: #f5f5f5; }
</style></head>
<body>
  <h1>1.1 Cardiology</h1>
  <p><strong>First-Tier Department:</strong> 1. Internal Medicine</p>
  <p><strong>Scope:</strong> Heart and blood vessels.</p>
  <!-- LLM filling instructions block -->
  <!-- FILL_ME comments in every data cell -->
  <table>...</table>
</body></html>
```

### FILL_ME Markers

Each data cell that the LLM must fill contains an HTML comment:
```html
<td class="fill-me"><!-- FILL_ME: Latest Value (with units) -->—</td>
<td class="fill-me"><!-- FILL_ME: Status: Known/Uncertain/Deprecated/NotKnown -->❌ Not Known</td>
```

After filling, the LLM MUST:
1. Replace the placeholder value with the extracted data.
2. Remove the `<!-- FILL_ME: ... -->` comment.
3. Change `class="fill-me"` to a context-appropriate class (or remove it).
4. For Status column: replace with `<td class="status-known">✅ Known</td>` etc.

---

## logs/ — Audit Trail

Three plain-text files providing a complete, auditable record of every clinical decision made during profile generation. Written by the LLM.

### logs/translation.txt

Documents all non-English content found in raw files and how it was translated.

**Format:**
```
======================================================================
TRANSLATION LOG — {patient_id}_profile
Generated: YYYY-MM-DD HH:MM
Source language(s) detected: [list]
======================================================================

--- Document: {filename} ---
Original language: {lang} (detected via: {method — explicit lang tag, LLM detection, etc.})
Translation method: LLM (model: {model_name})

[For each translated segment:]
Line/Region: {location in source}
Original ({lang}): "{original text}"
English: "{translated text}"
Confidence: High/Medium/Low
Note: {any ambiguity, alternative translations considered, clinical terminology verification}
```

**Rules:**
1. Log EVERY non-English clinical term/sentence translated.
2. If markitdown already produced English output but the source was non-English, note the detection and verify critical terms.
3. Flag any terms with uncertain translations that could affect clinical interpretation.
4. If all sources are already in English, write a single line: "All source documents are in English. No translation performed."

### logs/form_filling.txt

Row-by-row audit of every status table and history table filled.

**Format:**
```
======================================================================
FORM FILLING LOG — {patient_id}_profile
Generated: YYYY-MM-DD HH:MM
Tables filled: {N} status, {M} history
======================================================================

=== STATUS TABLE: 1.1 Cardiology ===
Time window determined: {start_date} to {end_date}
Rationale: {why this window — e.g., "Most recent encounter 2025-06-15; extended to 6 months for lab continuity"}

Row 1 — Blood Pressure:
  Sources consulted: raw/visit_note_2025-06-15.md
  Value extracted: "138/86 mmHg" (documented in vital signs section)
  Value Age calculation: 5 days before profile date → "5 days ago"
  Unit conversion: none needed (already mmHg)
  Status decision: ✅ Known (within window, clearly recorded, single source)
  Comment rationale: "Pre-hypertensive range per AHA 2017 guidelines"

Row 2 — Lipid Panel — LDL:
  Sources consulted: all raw/*.md files searched for "LDL", "lipid", "cholesterol"
  Value extracted: NOT FOUND in any source
  Status decision: ❌ Not Known (never documented)
  Comment rationale: "Essential for ASCVD risk stratification. Age >40 indicates screening."

Row 3 — HbA1c (example of deprecated):
  Sources consulted: raw/labs_2023-01.md, raw/labs_2025-03.md
  In-window value: 6.8% (2025-03) ← used
  Out-of-window value: 8.2% (2023-01) ← noted in history
  Value Age: 3 months before profile date → "3 months ago"
  Status decision: ✅ Known (in-window)
  Also flagged: deprecated value 8.2% from 2023-01 added to history_tables/1.4_endocrinology_2025-06-20.html

======================================================================
=== HISTORY TABLE: 1.4 Endocrinology ===
... (same row-by-row detail)
```

**Rules:**
1. Every filled row in every table gets an audit entry.
2. Document: which sources were consulted, what value was found, how Value Age was calculated, why the status was chosen, and the rationale for the comment.
3. For ❌ Not Known rows: list which sources were searched and confirm the variable is absent.
4. For 📅 Deprecated rows: note the old value, its age, and why it was excluded from the status window.
5. For unit conversions: show original value, conversion factor, and result.

### logs/profile_gen.txt

Documents the synthesis reasoning for `profile.html`.

**Format:**
```
======================================================================
PROFILE GENERATION LOG — {patient_id}_profile
Generated: YYYY-MM-DD HH:MM
======================================================================

=== OVERALL COMPLETENESS ===
Total variables across 36 departments: {N}
✅ Known: {X} ({X/N*100:.1f}%)
⚠️ Uncertain: {Y} ({Y/N*100:.1f}%)
📅 Deprecated: {Z} ({Z/N*100:.1f}%)
❌ Not Known: {W} ({W/N*100:.1f}%)

=== UNKNOWN FACTORS AUDIT — CLASSIFICATION RATIONALE ===

Critical Unknowns:
  1. 1.1 Cardiology — Lipid Panel
     Why critical: Age >40 + family history of early CAD + current hypertension.
     Without lipids, ASCVD risk cannot be calculated → cannot initiate statin therapy per guidelines.
     Source: status_tables/1.1_cardiology.html

  2. ...

High-Priority Unknowns:
  1. ...

Routine Unknowns:
  1. ...

Deprecated Values:
  1. 1.4 Endocrinology — HbA1c 8.2% (2023-01)
     Age: 29 months. Clinical guideline: HbA1c >6 months old should be re-measured
     before making treatment decisions. Moved to history table.
     Action: Re-measure HbA1c within 2 weeks.

Uncertainties Requiring Clarification:
  1. ...

=== CLINICAL HISTORY — NARRATIVE DECISIONS ===
- Key timeline events selected: {list with rationale for inclusion}
- Events omitted: {list with rationale for omission}

=== CROSS-DEPARTMENT SYNTHESIS ===
- 1.4 Endocrinology + 1.5 Nephrology: Diabetic nephropathy link identified because...
- ...

=== PRIORITY ACTION ITEMS — RANKING RATIONALE ===
1. Urgent: ... because {clinical urgency}
2. High: ...
3. Routine: ...
```

**Rules:**
1. Document the reasoning behind EVERY Unknown Factors classification.
2. Explain timeline event selection: which events made it into the narrative and why.
3. Justify every cross-department link.
4. Rank Priority Action Items with explicit clinical rationale.

---

## Time-Window Rule (status vs history)

- **status_tables**: most recent contiguous clinical episode. Default window = last encounter or last 6 months, whichever yields more data. Active hospitalization = entire admission.
- **history_tables**: everything before that window. A value outside the window is flagged as **📅 Deprecated** in the status table.
- **Rationale**: prevents stale data from masquerading as "current state".

## Status Definitions

| Status | Icon | Meaning |
|---|---|---|
| Known | ✅ | Value found within time window, clearly documented |
| Uncertain | ⚠️ | Ambiguous, conflicting, or qualified within window |
| Deprecated | 📅 | Value exists but is too old — outside time window |
| Not Known | ❌ | Never mentioned in any available record |

## Citation Format (in profile.html)

Every claim in `profile.html` becomes a clickable link:
```html
<a href="status_tables/1.1_cardiology.html">Cardiology Status</a>
<a href="history_tables/1.1_cardiology_2025-06-20.html">Cardiology History</a>
<a href="raw/discharge_summary.md">Discharge Summary</a>
```

All paths relative to `profile.html`'s location.

## Multilingual Handling

Raw documents may be in any language (Chinese, Japanese, Spanish, French, German, Korean, etc.).

1. **Detection:** `scripts/ingest_documents.py` flags non-English content in `raw/manifest.json` with a `"language"` field and confidence score.
2. **Translation:** The LLM translates all non-English clinical content to English for reasoning. Every translation decision is logged in `logs/translation.txt`.
3. **Audit requirement:** The original non-English text, the English translation, confidence level, and any ambiguous clinical terms MUST be recorded in the translation log.
4. **Critical terms:** Drug names, dosages, units, and diagnosis names must be verified against standard terminologies (RxNorm, ICD, LOINC) when translated.

## References

- `references/templates/status_tables_html/` — 36 blank HTML status-table templates
- `references/templates/history_tables_html/` — 36 blank HTML history-table templates
- `references/output_template.md` — Original profile layout template (legacy)
