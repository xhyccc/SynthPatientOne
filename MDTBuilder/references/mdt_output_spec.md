# MDT Output Specification

## Output Folder Structure

Given a patient profile at `{patient_id}_profile/`, the MDT produces:

```
{patient_id}_MDT/
├── mdt_solution.html              # Single comprehensive HTML — all 5 phases
├── reasoning/                     # Per-phase reasoning documents
│   ├── phase1_team_formation.md
│   ├── phase2_pre_meeting.md
│   │   ├── department_reviews/    # Independent review per participating dept
│   │   │   ├── 1.1_cardiology.md
│   │   │   └── ...
│   │   └── evidence_summary.md
│   ├── phase3_meeting.md
│   │   └── conflicts_resolution.md  # Only if conflicts arose
│   ├── phase4_post_meeting.md
│   │   └── patient_summary.md       # Plain-language patient communication
│   └── phase5_improvement.md
├── logs/
│   ├── mdt_audit.log                # Decision audit trail
│   └── reasoning_trace.log          # Cross-phase reasoning continuity
└── mdt_manifest.json
```

### Folder Purpose

| Path | Content |
|---|---|
| `mdt_solution.html` | **Primary output.** Self-contained HTML. All 5 phases in collapsible sections. Color-coded badges, evidence citations, patient summary. |
| `reasoning/` | Per-phase markdown documents. Detailed reasoning that feeds into `mdt_solution.html`. |
| `reasoning/phase2_pre_meeting/department_reviews/` | One file per participating department. Independent specialty review with evidence citations. |
| `logs/` | Audit trail and cross-phase reasoning continuity. |

---

## mdt_solution.html — Structure

Single self-contained HTML with these collapsible `<details>` sections:

### Section 1: Header & Executive Summary
- Patient ID, MDT date, scope, chair, coordinator
- Consensus outcome badge (color-coded)
- One-paragraph executive summary
- Completeness indicator: what % of needed data was available at MDT time

### Section 2: Phase 1 — Team Formation
- MDT scope definition with rationale
- Participating departments table (dept, role, reason for inclusion)
- Core clinical question
- Roles: Chair, Coordinator, Core Specialists

### Section 3: Phase 2 — Pre-Meeting
- **3a. Agenda:** Meeting schedule, time allocation per section
- **3b. Departmental Reviews:** Collapsible per-department panels, each containing:
  - Findings summary (from status tables, with citations)
  - Assessment (clinical interpretation)
  - Recommendations (specific, actionable)
  - Concerns / Contraindications
  - Data gaps
- **3c. Evidence Summary:** Aggregate table of all objective data (imaging, pathology, labs, exams)

### Section 4: Phase 3 — Meeting
- **4a. Case Presentation:** Presenter, patient summary, core question
- **4b. Objective Data Review:** Imaging and pathology presented, undisputed facts established
- **4c. Departmental Positions:** Each department's formal position (assessment + recommendation + evidence basis + confidence level)
- **4d. Conflict Resolution:** If applicable — disagreement identification, guideline consultation, risk comparison table, patient factors, chair decision, dissenting opinions
- **4e. Consensus Outcome:** Selected outcome type with detail, responsible department, timeline, success criteria, contingency plan

### Section 5: Phase 4 — Post-Meeting
- **5a. Implementation Plan:** Table of actions with responsible dept and deadlines
- **5b. Patient Communication:** Plain-language summary (no medical jargon)
- **5c. Outcome Tracking:** Metrics, baselines, targets, assessment dates
- **5d. MDT Re-Evaluation:** Scheduled date, early triggers

### Section 6: Phase 5 — Continuous Improvement
- Quality indicators table (8 metrics, target vs actual, met?)
- Process assessment (strengths, weaknesses)
- Action items for next MDT
- Guideline alignment audit

---

## CSS Color Scheme

| Element | Color |
|---|---|
| Header / Phase dividers | `#1a5276` (dark blue) |
| Executive summary | `#d5f5e3` background, `#27ae60` left border |
| Consensus outcome — Therapeutic | `#27ae60` (green) |
| Consensus outcome — Diagnostics | `#f39c12` (amber) |
| Consensus outcome — Surveillance | `#3498db` (blue) |
| Consensus outcome — Referral | `#8e44ad` (purple) |
| Consensus outcome — Palliative | `#e74c3c` (red) |
| Department position — agree | `#d4edda` (light green) |
| Concern / Contraindication | `#fdedec` (light red) |
| Dissenting opinion | `#f5eef8` (light purple) |
| Evidence citation links | `#1a5276` (blue, underlined) |
| Data gap flag | `#fff3cd` (amber) |

---

## logs/mdt_audit.log Format

```
======================================================================
MDT AUDIT LOG — {patient_id}
MDT Date: YYYY-MM-DD | Scope: {scope}
Chair: {chair} | Coordinator: {coordinator}
======================================================================

=== DECISION TIMELINE ===
[timestamp] Phase 1 started: Team formation
[timestamp] Phase 1 complete: {N} departments identified
[timestamp] Phase 2 started: Pre-meeting reviews
[timestamp] Phase 2 complete: {N} departmental reviews written
[timestamp] Phase 3 started: MDT meeting
[timestamp] Phase 3 — Case presented by {dept}
[timestamp] Phase 3 — {N} departmental positions recorded
[timestamp] Phase 3 — Conflict identified: {topic} (or "No conflicts")
[timestamp] Phase 3 — Consensus reached: {outcome type}
[timestamp] Phase 4 started: Post-meeting
[timestamp] Phase 4 complete: Implementation plan, patient summary written
[timestamp] Phase 5 started: Quality audit
[timestamp] Phase 5 complete

=== DECISION RATIONALE ===
{Why this outcome was chosen. The chain of clinical logic from
evidence → interpretation → recommendation → decision.}

=== EVIDENCE CITED ===
{List of every source cited during the MDT, with what claim it supported.}

=== CONFLICT RESOLUTION ===
{If applicable: what the conflict was, how it was resolved, who dissented.}
Or: "No inter-departmental conflicts identified."

=== QUALITY SELF-ASSESSMENT ===
{Completed quality indicators table.}
```

---

## logs/reasoning_trace.log Format

```
======================================================================
REASONING TRACE — {patient_id}
Cross-phase continuity verification
======================================================================

=== PHASE 1 → PHASE 2: Department Selection ===
Why these departments were chosen and not others.
Which departments were excluded and why.

=== PHASE 2 → PHASE 3: From Review to Position ===
How each departmental review evolved into the formal position stated in the meeting.
Any changes between pre-meeting assessment and meeting position.

=== PHASE 3 → PHASE 4: From Consensus to Plan ===
How the consensus decision was translated into specific, timed, accountable actions.
Any modifications or refinements during the translation.

=== PHASE 4 → PHASE 5: Self-Assessment Integrity ===
Honest assessment of whether the quality audit reflects reality.
Any concerns about the MDT process that should be escalated.
```

---

## mdt_manifest.json Format

```json
{
  "patient_id": "patient_smoke_test",
  "mdt_date": "2025-06-21",
  "scope": "Complex COPD + Cardiovascular Risk Management",
  "chair": "Pulmonology",
  "coordinator": "Internal Medicine",
  "consensus_outcome": "Further Diagnostics Required + Therapeutic Intervention",
  "participating_departments": ["1.2_pulmonology", "1.1_cardiology", "1.4_endocrinology", "1.5_nephrology", "7.1_radiology"],
  "files": {
    "solution_html": "mdt_solution.html",
    "reasoning_dir": "reasoning/",
    "logs_dir": "logs/"
  }
}
```
