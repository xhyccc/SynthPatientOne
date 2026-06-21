#!/usr/bin/env python3
"""
run_pipeline.py — Full pipeline for building a patient profile.

Phases:
  1. INGEST: Convert all records in {patient_id}/ to markdown/PNG → {patient_id}_profile/raw/
  2. AUDIT (LLM): Fill status_tables and history_tables from raw/ files
  3. SYNTHESIS (LLM): Write profile.html with clickable citations

Usage:
  python run_pipeline.py /path/to/patient_id                       # Full pipeline
  python run_pipeline.py /path/to/patient_id --phase 1             # Ingest only
  python run_pipeline.py /path/to/patient_id --phase 2             # Audit only (requires raw/)
  python run_pipeline.py /path/to/patient_id --phase 3             # Synthesis only (requires tables)
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = SCRIPTS_DIR.parent / "references" / "templates"
STATUS_HTML_SRC = TEMPLATES_DIR / "status_tables_html"
HISTORY_HTML_SRC = TEMPLATES_DIR / "history_tables_html"


def _run(cmd, **kwargs):
    """Run a command and check return code."""
    result = subprocess.run(cmd, **kwargs)
    if result.returncode != 0:
        print(f"ERROR: Command failed (code {result.returncode}): {' '.join(cmd)}", file=sys.stderr)
        sys.exit(result.returncode)
    return result


# ---------------------------------------------------------------------------
# Phase 1: Ingest
# ---------------------------------------------------------------------------

def phase1_ingest(patient_dir: str, profile_dir: str, use_ocr: bool = True):
    """Convert all patient records to markdown/PNG into raw/."""
    raw_dir = Path(profile_dir) / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    ingest_script = SCRIPTS_DIR / "ingest_documents.py"
    if not ingest_script.exists():
        print(f"ERROR: {ingest_script} not found", file=sys.stderr)
        sys.exit(1)

    cmd = [
        sys.executable, str(ingest_script),
        patient_dir,
        "--output", str(raw_dir),
    ]
    if use_ocr:
        cmd.append("--ocr")

    print(f"[Phase 1] Ingesting records from {patient_dir} → {raw_dir}")
    _run(cmd)

    # Also generate a manifest of what was extracted
    manifest_path = raw_dir / "manifest.json"
    ingested = list(raw_dir.glob("*"))
    manifest = {
        "patient_dir": str(Path(patient_dir).resolve()),
        "profile_dir": str(Path(profile_dir).resolve()),
        "ingestion_date": datetime.now().isoformat(),
        "files": [f.name for f in ingested],
    }
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"[Phase 1] Manifest written to {manifest_path}")


# ---------------------------------------------------------------------------
# Phase 2: Audit (LLM fills status_tables and history_tables)
# ---------------------------------------------------------------------------

def phase2_audit(profile_dir: str):
    """
    Prepare for LLM audit by copying HTML templates to the profile directory
    and creating the logs/ audit trail. The actual filling is done by the LLM.
    """
    profile_path = Path(profile_dir)
    raw_dir = profile_path / "raw"
    if not raw_dir.exists():
        print(f"ERROR: raw/ directory not found in {profile_dir}. Run Phase 1 first.", file=sys.stderr)
        sys.exit(1)

    # Copy status HTML templates
    status_src = STATUS_HTML_SRC
    status_dst = profile_path / "status_tables"
    if not status_src.exists():
        print(f"ERROR: Template directory not found: {status_src}", file=sys.stderr)
        sys.exit(1)
    if status_dst.exists():
        shutil.rmtree(status_dst)
    shutil.copytree(status_src, status_dst)

    # Copy history HTML templates
    history_src = HISTORY_HTML_SRC
    history_dst = profile_path / "history_tables"
    if not history_src.exists():
        print(f"ERROR: Template directory not found: {history_src}", file=sys.stderr)
        sys.exit(1)
    if history_dst.exists():
        shutil.rmtree(history_dst)
    shutil.copytree(history_src, history_dst)

    # Create logs directory with empty audit files
    logs_dir = profile_path / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_headers = {
        "translation.txt": "# Translation Log\n# Documents any non-English → English translation performed during Phase 2 audit.\n# Format: [timestamp] [source_file] [source_language] → English: original_text → translated_text (confidence: X%)\n",
        "form_filling.txt": "# Form Filling Audit Log\n# Records every variable fill decision for every status/history table.\n# Format: [table_name] [row_number] [variable]: decision_rationale, unit_conversion, Value_Age_calculation, status_reasoning, source_citation\n",
        "profile_gen.txt": "# Profile Generation Log\n# Records the synthesis process for profile.html.\n# Covers: Unknown Factors classification rationale, deprecated value reasoning, critical-vs-routine judgments, cross-department linking decisions.\n",
    }
    for log_name, header in log_headers.items():
        log_path = logs_dir / log_name
        with open(log_path, "w") as f:
            f.write(header)
            f.write(f"\n# Profile: {profile_path.name}\n")
            f.write(f"# Started: {datetime.now().isoformat()}\n")
            f.write("=" * 70 + "\n\n")

    print(f"[Phase 2] HTML templates copied to {profile_dir}")
    print(f"  status_tables/  ← {status_dst}")
    print(f"  history_tables/ ← {history_dst}")
    print(f"  logs/           ← {logs_dir}")
    print()
    print("=" * 70)
    print("AUDIT PHASE — Instructions for the LLM:")
    print("=" * 70)
    print()
    print("★ CRITICAL: Write to logs/translation.txt, logs/form_filling.txt AS YOU WORK.")
    print("  These are medical-audit-grade logs. Every decision must be traceable.")
    print()
    print(f"1. TRANSLATION: Read all files in {raw_dir}/")
    print(f"   - Detect non-English content (Chinese, Japanese, French, German, Spanish, Korean, etc.)")
    print(f"   - Translate ALL non-English clinical text to English for reasoning.")
    print(f"   - Log EVERY translation to {logs_dir}/translation.txt:")
    print(f"     [source_file] [line] [language] → original → English (confidence%)")
    print()
    print(f"2. STATUS TABLES: For EACH of the 36 HTML files in {status_dst}/:")
    print("   ★ FIRST: Determine TIME WINDOW (latest encounter / admission / 6 months).")
    print("   a. Fill each <!-- FILL_ME: ... --> marker using ONLY in-window values.")
    print("   b. Values outside window → 📅 Deprecated, leave value blank, cross-ref history.")
    print("   c. Not mentioned → ❌ Not Known. Conflict → ⚠️ Uncertain.")
    print("   d. For EVERY filled cell, append to logs/form_filling.txt:")
    print("      [table] [row] [variable]: extracted_value, unit_conversion, Value_Age_calc, status_reason, source")
    print("   e. Remove <!-- FILL_ME: ... --> comments after filling.")
    print()
    print(f"3. HISTORY TABLES: For HTML files in {history_dst}/ where history EXISTS:")
    print("   a. Document pre-window events in reverse chronological order.")
    print("   b. Use value_deprecated for stale values. Mark In-Window? column.")
    print("   c. Log each row to logs/form_filling.txt.")
    print("   d. Rename filled files: {department}_YYYY-MM-DD.html")
    print("   e. Delete templates for departments with NO history.")
    print()
    print(f"4. After filling: verify every value cites a source in raw/; statuses correct;")
    print("   no fabricated values; translation.txt and form_filling.txt are complete.")
    print("=" * 70)

def phase3_synthesis(profile_dir: str):
    """Print instructions for the LLM to write profile.html."""
    profile_path = Path(profile_dir)
    print("=" * 70)
    print("SYNTHESIS PHASE — Instructions for the LLM:")
    print("=" * 70)
    print()
    print(f"1. Read all filled status tables in {profile_path}/status_tables/")
    print(f"2. Read all filled history tables in {profile_path}/history_tables/")
    print(f"3. Write {profile_path}/profile.html — a self-contained HTML document")
    print(f"   following the specification in references/output_spec.md.")
    print()
    print("★ AUDIT LOG: Write to logs/profile_gen.txt AS YOU GENERATE.")
    print("  Document: Unknown Factors classification rationale, why each variable")
    print("  was judged Critical/High/Routine/Uncertain, deprecated value decisions,")
    print("  cross-department linking logic, completeness calculations.")
    print()
    print("Key requirements:")
    print("  - Self-contained HTML. All CSS inline. Print-friendly.")
    print("  - Color-coded status badges: ✅ green, ⚠️ amber, 📅 grey, ❌ red.")
    print("  - Collapsible sections (details/summary) per first-tier department.")
    print("  - Every factual claim is a clickable <a href=\"...\"> link to the")
    print("    supporting status_tables/ or history_tables/ file.")
    print("  - Unknown Factors Audit section with four tiered tables:")
    print("    📅 Deprecated | ❌ Critical Unknowns | ⚠️ Uncertainties | ❌ Routine Unknowns")
    print("  - Completeness bar at the top (visual progress indicator).")
    print("  - Priority Action Items ranked by urgency.")
    print("  - File is at: " + str(profile_path / "profile.html"))
    print("=" * 70)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Build a complete patient profile from health records."
    )
    parser.add_argument(
        "patient_dir",
        help="Path to the folder containing the patient's health records (e.g., /path/to/patient_001/)",
    )
    parser.add_argument(
        "--phase", type=int, choices=[1, 2, 3],
        help="Run only a specific phase (1=ingest, 2=audit, 3=synthesis)",
    )
    parser.add_argument(
        "--output-dir", "-o",
        help="Override the output profile directory (default: {patient_dir}_profile)",
    )
    parser.add_argument(
        "--no-ocr", action="store_true",
        help="Skip OCR for image files in Phase 1",
    )
    args = parser.parse_args()

    patient_path = Path(args.patient_dir).resolve()
    if not patient_path.exists():
        print(f"ERROR: Patient directory not found: {patient_path}", file=sys.stderr)
        sys.exit(1)

    patient_id = patient_path.name
    profile_dir = args.output_dir or str(patient_path.parent / f"{patient_id}_profile")

    print(f"Patient ID: {patient_id}")
    print(f"Profile directory: {profile_dir}")
    print()

    if args.phase is None or args.phase == 1:
        phase1_ingest(str(patient_path), profile_dir, use_ocr=not args.no_ocr)
        print()

    if args.phase is None or args.phase == 2:
        phase2_audit(profile_dir)
        print()

    if args.phase is None or args.phase == 3:
        phase3_synthesis(profile_dir)
        print()

    if args.phase is None:
        print("=" * 70)
        print("Pipeline setup complete. The LLM must now complete Phases 2 & 3.")
        print(f"Profile location: {profile_dir}/")
        print("=" * 70)


if __name__ == "__main__":
    main()
