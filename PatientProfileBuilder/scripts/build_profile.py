#!/usr/bin/env python3
"""
build_profile.py — Assemble the final patient profile from extracted clinical data.

Input: JSON containing all extracted variables organized by department.
Output: Markdown Patient Profile document following the output_template.md spec.

Can also output JSON, HTML, or Excel formats.
"""

import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Department hierarchy — mirrors references/department_hierarchy.md
# ---------------------------------------------------------------------------

DEPARTMENT_HIERARCHY = {
    "1. Internal Medicine": {
        "1.1 Cardiology": "Heart and blood vessels",
        "1.2 Pulmonology": "Lungs and respiratory tract",
        "1.3 Gastroenterology": "Digestive system and intestines",
        "1.4 Endocrinology": "Hormones and metabolic disorders",
        "1.5 Nephrology": "Kidneys",
        "1.6 Neurology": "Brain, spinal cord, and nervous system",
        "1.7 Rheumatology": "Joints, muscles, and autoimmune diseases",
        "1.8 Hematology": "Blood and blood-producing organs",
        "1.9 Oncology": "Cancer diagnosis and treatment",
        "1.10 Infectious Diseases": "Contagious and communicable diseases",
    },
    "2. Surgery": {
        "2.1 General Surgery": "Abdominal organs",
        "2.2 Orthopedic Surgery": "Bones, joints, ligaments, tendons",
        "2.3 Neurosurgery": "Brain and nervous system (operative)",
        "2.4 Cardiothoracic Surgery": "Heart, lungs, chest cavity",
        "2.5 Urology": "Urinary tract and male reproductive organs",
        "2.6 Plastic & Reconstructive": "Restoration and reconstruction",
        "2.7 Vascular Surgery": "Arteries and veins",
    },
    "3. Obstetrics and Gynecology (OB/GYN)": {
        "3.1 Obstetrics": "Pregnancy, childbirth, postpartum",
        "3.2 Gynecology": "Female reproductive health",
        "3.3 Reproductive Endocrinology": "Infertility and hormonal issues",
        "3.4 Gynecologic Oncology": "Reproductive system cancers",
    },
    "4. Pediatrics": {
        "4.1 General Pediatrics": "Routine care, childhood illnesses",
        "4.2 Neonatology": "Newborn infants",
        "4.3 Pediatric Sub-specialties": "Cardiology/Oncology/Neurology for children",
    },
    "5. Emergency Medicine": {
        "5.1 Trauma": "Severe physical injuries",
        "5.2 Toxicology": "Poisoning and drug overdoses",
        "5.3 Pre-hospital Care / EMS": "Paramedic and ambulance services",
    },
    "6. Specialized Clinical Departments": {
        "6.1 Psychiatry": "Mental health, mood, psychotic disorders",
        "6.2 Ophthalmology": "Eye and vision care",
        "6.3 Otolaryngology (ENT)": "Ear, nose, and throat",
        "6.4 Dermatology": "Skin, hair, and nails",
    },
    "7. Medical Technology & Ancillary": {
        "7.1 Radiology / Imaging": "X-rays, MRIs, CTs, ultrasounds",
        "7.2 Pathology": "Tissues and cells examination",
        "7.3 Laboratory Medicine": "Blood work, urinalysis, microbiology",
        "7.4 Anesthesiology": "Pain relief, vital function maintenance",
        "7.5 Rehabilitation / Physical Medicine": "PT, OT, speech therapy",
    },
}

STATUS_ICONS = {"Known": "✅", "Uncertain": "⚠️", "Unknown": "❌", "N/A": "N/A"}


def build_profile(patient_data: dict, output_format: str = "markdown") -> str:
    """Main entry point: assemble the complete patient profile."""
    if output_format == "markdown":
        return build_markdown_profile(patient_data)
    elif output_format == "json":
        return json.dumps(patient_data, indent=2, default=str)
    elif output_format == "html":
        return build_html_profile(patient_data)
    else:
        raise ValueError(f"Unsupported output format: {output_format}")


def build_markdown_profile(data: dict) -> str:
    """Build the full markdown profile."""
    lines = []
    demographics = data.get("patient_demographics", {})
    departments_data = data.get("departments", {})
    sources = data.get("sources", [])
    cross_dept = data.get("cross_departmental", [])
    actions = data.get("priority_actions", [])

    # --- Header ---
    patient_label = demographics.get("name", "[Patient Name / ID]")
    lines.append(f"# Patient Profile: {patient_label}")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Sources Reviewed:** {len(sources)} document(s)")
    total_known = sum(len(d.get("known", [])) for d in departments_data.values())
    total_expected = sum(
        len(d.get("known", [])) + len(d.get("unknown", []))
        for d in departments_data.values()
    )
    completeness = f"{total_known / total_expected * 100:.0f}%" if total_expected > 0 else "0%"
    lines.append(f"**Overall Completeness:** {completeness} of expected variables are known")
    lines.append("")

    # --- Demographics Table ---
    lines.append("## Patient Demographics & Summary")
    lines.append("")
    if demographics:
        lines.append("| Field | Value |")
        lines.append("|---|---|")
        for key in ["age", "sex", "chief_complaint", "key_diagnoses", "allergies", "current_medications"]:
            val = demographics.get(key, "Not documented")
            if isinstance(val, list):
                val = "; ".join(val)
            lines.append(f"| {key.replace('_', ' ').title()} | {val} |")
    else:
        lines.append("*No demographic information available.*")
    lines.append("")

    # --- Department Profiles ---
    for first_tier, secondary_depts in DEPARTMENT_HIERARCHY.items():
        dept_has_content = any(
            departments_data.get(sec_name, {}).get("known") or
            departments_data.get(sec_name, {}).get("unknown")
            for sec_name in secondary_depts
        )
        if not dept_has_content:
            continue

        lines.append(f"## {first_tier}")
        lines.append("")

        for sec_name, scope in secondary_depts.items():
            dept = departments_data.get(sec_name, {})
            known = dept.get("known", [])
            unknown = dept.get("unknown", [])
            commentary = dept.get("commentary", "")

            lines.append(f"### {sec_name}")
            lines.append("")
            lines.append(f"**Department Scope:** {scope}")
            lines.append("")

            # Known table
            lines.append("#### Factors Known")
            lines.append("")
            if known:
                lines.append("| # | Variable | Value | Date | Source | Comment |")
                lines.append("|---|---|---|---|---|---|")
                for i, var in enumerate(known, 1):
                    lines.append(
                        f"| {i} | {var.get('variable','')} | {var.get('value','')} | "
                        f"{var.get('date','')} | {var.get('source','')} | {var.get('comment','')} |"
                    )
            else:
                lines.append("*No confirmed findings in the available records.*")
            lines.append("")

            # Unknown / Uncertain table
            lines.append("#### Factors Not Yet Known / Uncertain")
            lines.append("")
            if unknown:
                lines.append("| # | Variable | Status | Expected Because | Comment |")
                lines.append("|---|---|---|---|---|")
                for i, var in enumerate(unknown, 1):
                    status = STATUS_ICONS.get(var.get("status", "Unknown"), "❌")
                    lines.append(
                        f"| {i} | {var.get('variable','')} | {status} {var.get('status','Unknown')} | "
                        f"{var.get('expected_because','')} | {var.get('comment','')} |"
                    )
            else:
                lines.append("*All expected variables are documented.*")
            lines.append("")

            # Commentary
            if commentary:
                lines.append("#### Department Commentary")
                lines.append("")
                lines.append(commentary)
                lines.append("")
            lines.append("---")
            lines.append("")

    # --- Cross-Departmental Synthesis ---
    if cross_dept:
        lines.append("## Cross-Departmental Synthesis")
        lines.append("")
        lines.append("| Link | Departments Involved | Description |")
        lines.append("|---|---|---|")
        for link in cross_dept:
            lines.append(f"| {link.get('link','')} | {link.get('departments','')} | {link.get('description','')} |")
        lines.append("")

    # --- Priority Actions ---
    if actions:
        lines.append("## Priority Action Items")
        lines.append("")
        lines.append("| Priority | Department | Missing Variable | Rationale |")
        lines.append("|---|---|---|---|")
        for act in actions:
            lines.append(
                f"| {act.get('priority','')} | {act.get('department','')} | "
                f"{act.get('variable','')} | {act.get('rationale','')} |"
            )
        lines.append("")
    else:
        lines.append("## Priority Action Items")
        lines.append("")
        lines.append("*No urgent missing variables identified.*")
        lines.append("")

    # --- Source Manifest ---
    lines.append("## Source Manifest")
    lines.append("")
    if sources:
        lines.append("| # | File | Format | Pages | Extraction Method | Date Extracted |")
        lines.append("|---|---|---|---|---|---|")
        for i, src in enumerate(sources, 1):
            lines.append(
                f"| {i} | {src.get('file','')} | {src.get('format','')} | "
                f"{src.get('pages','?')} | {src.get('method','')} | {src.get('date_extracted','')} |"
            )
    else:
        lines.append("*No source information available.*")
    lines.append("")

    return "\n".join(lines)


def build_html_profile(data: dict) -> str:
    """Build an HTML version of the profile (self-contained, printable)."""
    md = build_markdown_profile(data)
    try:
        import markdown
        html = markdown.markdown(md, extensions=["tables", "fenced_code"])
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Patient Profile</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; line-height: 1.6; }}
table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; font-size: 14px; }}
th {{ background-color: #f5f5f5; }}
h1 {{ border-bottom: 2px solid #333; padding-bottom: 8px; }}
h2 {{ border-bottom: 1px solid #999; padding-bottom: 4px; }}
</style>
</head>
<body>
{html}
</body>
</html>"""
    except ImportError:
        return f"<pre>{md}</pre>"


def compute_completeness(departments_data: dict) -> dict:
    """Compute completeness stats per department and overall."""
    stats = {}
    total_known = 0
    total_expected = 0

    for first_tier, secondary_depts in DEPARTMENT_HIERARCHY.items():
        for sec_name in secondary_depts:
            dept = departments_data.get(sec_name, {})
            k = len(dept.get("known", []))
            u = len(dept.get("unknown", []))
            expected = k + u
            total_known += k
            total_expected += expected
            stats[sec_name] = {
                "known": k,
                "expected": expected,
                "completeness": f"{k / expected * 100:.0f}%" if expected > 0 else "N/A"
            }

    stats["overall"] = {
        "known": total_known,
        "expected": total_expected,
        "completeness": f"{total_known / total_expected * 100:.0f}%" if total_expected > 0 else "0%"
    }

    return stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build patient profile from extracted data")
    parser.add_argument("input", help="Input JSON file with patient data")
    parser.add_argument("--format", "-f", choices=["markdown", "json", "html"],
                        default="markdown", help="Output format (default: markdown)")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--completeness", action="store_true",
                        help="Print only completeness statistics")

    args = parser.parse_args()

    with open(args.input, "r") as f:
        data = json.load(f)

    if args.completeness:
        stats = compute_completeness(data.get("departments", {}))
        print(json.dumps(stats, indent=2))
    else:
        output = build_profile(data, output_format=args.format)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"Profile written to {args.output}")
        else:
            print(output)
