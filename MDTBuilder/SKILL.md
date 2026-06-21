---
name: MDTBuilder
description: >
  Given a patient profile folder ({patient_id}_profile/) from PatientProfileBuilder, execute a full
  Multidisciplinary Team (MDT) review following a standardized 5-phase protocol and produce a single
  comprehensive mdt_solution.html. The pipeline: (1) Team Formation — scope, roles, department selection;
  (2) Pre-Meeting — independent departmental reviews with evidence citations from status tables;
  (3) Meeting — case presentation, objective data review, departmental positions, conflict resolution
  via guideline consultation + risk comparison + chair decision, formal consensus outcome;
  (4) Post-Meeting — implementation plan, patient communication, outcome tracking;
  (5) Continuous Improvement — quality audit against 8 indicators. All reasoning is documented in
  per-phase markdown files under reasoning/. Output goes to {patient_id}_MDT/.
---

# MDT Builder

## Overview

Given a patient profile `{patient_id}_profile/` (produced by `PatientProfileBuilder`),
this skill runs a full Multidisciplinary Team review. The LLM acts as the MDT Coordinator,
simulating each department's independent review, facilitating the meeting discussion,
resolving inter-departmental conflicts, and producing a single comprehensive output:
`{patient_id}_MDT/mdt_solution.html`.

### What the Pipeline Produces

```
{patient_id}_MDT/
├── mdt_solution.html                # ★ Single comprehensive HTML — all 5 phases
├── reasoning/                       # Per-phase reasoning documents
│   ├── phase1_team_formation.md
│   ├── phase2_pre_meeting/
│   │   ├── departmental_reviews/    # Independent review per department
│   │   │   ├── 1.1_cardiology.md
│   │   │   └── ...
│   │   └── evidence_summary.md
│   ├── phase3_meeting.md
│   │   └── conflicts_resolution.md  # Only if conflicts arose
│   ├── phase4_post_meeting.md
│   │   └── patient_summary.md       # Plain-language for patient/family
│   └── phase5_improvement.md
├── logs/
│   ├── mdt_audit.log                # Decision audit trail
│   └── reasoning_trace.log          # Cross-phase continuity
└── mdt_manifest.json
```

### Core Principle

**The MDT does not re-extract data.** It reads the audited status tables, history tables,
and profile.html from `PatientProfileBuilder`. Every recommendation cites these as evidence.
The MDT's role is to interpret, synthesize, and decide — not to re-audit raw records.

---

## When to Use This Skill

- Complex patient requires coordinated input from multiple specialties.
- Treatment decisions involve conflicting departmental recommendations.
- Formal MDT consensus report needed for the medical record.
- Clinical governance requires documented multidisciplinary decision-making.
- Tumor board, complex trauma board, transplant evaluation.

---

## Five Phases

| Phase | Goal | Key Output |
|---|---|---|
| **1. Team Formation** | Define scope, appoint roles, select participating departments | `phase1_team_formation.md` |
| **2. Pre-Meeting** | Independent departmental reviews with evidence citations | `phase2_pre_meeting/` — reviews + evidence summary |
| **3. Meeting** | Case presentation, objective data, positions, conflict resolution, consensus | `phase3_meeting.md` |
| **4. Post-Meeting** | Implementation plan, patient communication, outcome tracking | `phase4_post_meeting.md` |
| **5. Improvement** | Quality audit, process assessment | `phase5_improvement.md` |

All five phases are rendered into a single `mdt_solution.html` with collapsible sections,
color-coded consensus badges, evidence citation links, and a patient-facing summary.

---

## Workflow

### Phase 0 — Setup

1. Read `{patient_id}_profile/` — status_tables, history_tables, profile.html.
2. Create `{patient_id}_MDT/` folder with all subdirectories.
3. Read `references/templates/reasoning_phase1.md` through `reasoning_phase5.md` for detailed prompts.


### Department Selection Algorithm

The LLM MUST use this algorithm to select participating departments:


### Phase 1 — Team Formation

Using `references/templates/reasoning_phase1.md`:
1. Determine MDT scope from key diagnoses and critical unknowns.
2. Formulate the core clinical question.
3. Select participating departments with rationale.
4. Assign Chair and Coordinator roles.

Write: `reasoning/phase1_team_formation.md`

### Phase 2 — Pre-Meeting

Using `references/templates/reasoning_phase2.md`:
1. For each participating department, write an independent review:
   - Findings summary (from status/history tables)
   - Clinical assessment
   - Recommendations (specific, actionable, evidence-cited)
   - Concerns / Contraindications
   - Data gaps
2. Aggregate all objective evidence into `evidence_summary.md`.
3. Write the agenda.

Write: `reasoning/phase2_pre_meeting/`


### Dissenting Opinion Protocol

If a department disagrees with the consensus, the LLM MUST:

1. **Record the dissent explicitly** in phase3_meeting.md and mdt_solution.html Section 3.4:
   - Which department dissents
   - What their recommendation was
   - Why they were overruled (evidence, risk comparison, patient factors)
   - Whether the dissenting department accepts the chair's decision or maintains their objection

2. **Classify the dissent severity:**
   - **Level 1 (Procedural):** Agrees with outcome but disagrees on method/timeline. No patient safety concern.
   - **Level 2 (Clinical):** Disagrees on treatment choice. Different risk/benefit calculus. Should be flagged for audit.
   - **Level 3 (Safety):** Dissenting department believes the chosen intervention poses patient harm. MUST be escalated to clinical governance.

3. **Escalation path for Level 3 dissents:** Document in mdt_audit.log with URGENT flag.
### Phase 3 — Meeting

Using `references/templates/reasoning_phase3.md`:
1. Case presentation.
2. Objective data review — establish undisputed facts.
3. Each department states formal position.
4. If conflicts: apply resolution framework (guidelines → risk comparison → patient factors → chair decision).
5. Select consensus outcome from 6 standard outcomes.

Write: `reasoning/phase3_meeting.md`

### Phase 4 — Post-Meeting

Using `references/templates/reasoning_phase4.md`:
1. Implementation plan with responsible departments and deadlines.
2. Patient communication summary in plain language.
3. Outcome tracking metrics.
4. MDT re-evaluation schedule.

Write: `reasoning/phase4_post_meeting.md`

### Phase 5 — Improvement

Using `references/templates/reasoning_phase5.md`:
1. Quality audit against 8 indicators.
2. Process assessment (strengths, weaknesses).
3. Guideline alignment audit.

Write: `reasoning/phase5_improvement.md`

### Phase 6 — Synthesis

1. Read all `reasoning/` files.
2. Fill `assets/mdt_solution_template.html` (62 placeholders) with content from the reasoning files.
3. Write `{patient_id}_MDT/mdt_solution.html`.
4. Write `logs/mdt_audit.log` and `logs/reasoning_trace.log`.
5. Write `mdt_manifest.json`.

---

## Consensus Outcomes

| # | Outcome | Badge Color |
|---|---|---|
| 1 | Therapeutic Intervention (Medical) | Green |
| 2 | Therapeutic Intervention (Surgical) | Green |
| 3 | Further Diagnostics Required | Amber |
| 4 | Active Surveillance / Monitoring | Blue |
| 5 | Referral to External Specialist | Purple |
| 6 | Palliative / Supportive Care | Red |

---

## Conflict Resolution Framework

```
1. IDENTIFY exact point of disagreement
2. EVIDENCE: What does each department cite?
3. GUIDELINE: Consult NCCN / ESC / AHA / GOLD / ADA
4. RISK COMPARISON: Morbidity, mortality, QoL impact
5. PATIENT FACTORS: ECOG, comorbidities, preferences
6. CHAIR DECISION: Recommendation with full rationale
7. DISSENT: Record any dissenting opinion
```

---

## Quick Start

Pure LLM reasoning. Activate with:

```
@MDTBuilder on patient_001_profile/
→ produces patient_001_MDT/mdt_solution.html
```

---

## References

| Reference | Content |
|---|---|
| `references/mdt_protocol.md` | Full 5-phase MDT protocol with conflict resolution framework, quality indicators |
| `references/mdt_output_spec.md` | Output folder structure, mdt_solution.html sections, log formats, manifest spec |
| `references/templates/reasoning_phase1.md` | Phase 1 reasoning prompts: scope, roles, department selection |
| `references/templates/reasoning_phase2.md` | Phase 2 reasoning prompts: departmental review, evidence summary, agenda |
| `references/templates/reasoning_phase3.md` | Phase 3 reasoning prompts: case presentation, positions, conflict resolution, consensus |
| `references/templates/reasoning_phase4.md` | Phase 4 reasoning prompts: implementation, patient communication, tracking |
| `references/templates/reasoning_phase5.md` | Phase 5 reasoning prompts: quality audit, process assessment |

## Assets

| Asset | Content |
|---|---|
| `assets/mdt_solution_template.html` | Comprehensive HTML template: 6 collapsible sections, 62 placeholders, color-coded badges |

---

## Integration

| Skill | Output Used by MDTBuilder |
|---|---|
| `PatientProfileBuilder` | status_tables/*.html, history_tables/*.html, profile.html, Unknown Factors Audit → inputs to departmental reviews |

---

## Best Practices

1. **Do not re-extract data.** Read the profile. Do not re-read raw records.
2. **Every recommendation cites evidence.** Use relative paths to status/history tables.
3. **Record dissenting opinions.** Consensus does not mean unanimity.
4. **Patient-centered.** When clinical evidence is equivocal, patient factors decide.
5. **Actionable outputs.** Every consensus decision includes WHO does WHAT by WHEN.
6. **Guideline-referenced.** Cite specific guidelines, not vague "standard of care."
7. **Complete the quality audit.** Self-assessment is mandatory.
8. **Reasoning in reasoning/ files, summary in mdt_solution.html.** Keep them in sync.

## Limitations

- MDT simulation is based on documented data only. Missing data = limited MDT.
- The LLM simulates department perspectives; it does not replace actual specialist consultation.
- Clinical guidelines cited should be verified by a human clinician.
- This skill organizes decision-making; it does not provide medical treatment.
