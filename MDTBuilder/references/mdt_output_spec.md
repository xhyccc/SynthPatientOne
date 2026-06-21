# MDT Output Specification

## Output Folder Structure

Given a patient profile at `{patient_id}_profile/`, the MDT pipeline produces:

```
{patient_id}_profile/mdt/
├── pre_meeting/
│   ├── agenda.md                        # Which departments, core question, case summary
│   ├── departmental_reviews/            # One per participating department
│   │   ├── 1.1_cardiology.md
│   │   ├── 1.3_gastroenterology.md
│   │   ├── 7.1_radiology.md
│   │   └── ... (only departments with MDT-relevant findings)
│   └── evidence_summary.md              # Aggregate of all objective evidence
├── meeting/
│   ├── minutes.md                       # Verbatim-style meeting record
│   └── conflicts_resolution.md          # Any conflicts and how they were resolved
├── consensus_report.html                # Final MDT consensus — self-contained HTML
├── patient_summary.md                   # Plain-language patient-facing summary
├── follow_up_plan.md                    # Timeline, triggers, responsible departments
└── quality_audit.md                     # Process quality self-assessment
```

---

## Pre-Meeting Templates

### pre_meeting/agenda.md

```markdown
# MDT Agenda — {patient_id}

**Meeting Date:** YYYY-MM-DD
**MDT Scope:** {e.g., Oncology — GI, Complex Cardiology, Trauma}
**Lead Clinician (Chair):** {designated}
**MDT Coordinator:** {designated}

## Core Clinical Question
{The single most important question this MDT must answer. E.g., "Is this patient a surgical candidate given comorbidities?"}

## Case Summary
{2-3 sentence summary from profile.html}

## Participating Departments
| Department | Representative | Reason for Inclusion |
|---|---|---|
| 1.1 Cardiology | — | Hypertension, incomplete cardiac workup |
| 7.1 Radiology | — | Pending CT interpretation |
| ... | | |

## Key Unknowns Requiring MDT Input
{List the critical missing pieces that the MDT must address}
```

### pre_meeting/departmental_reviews/{dept}.md

```markdown
# Departmental Review — {Department Name}

**Reviewer:** {Department Representative}
**Date:** YYYY-MM-DD
**Sources Reviewed:** {list of status/history tables consulted}

## Findings Summary
{What this department knows from the patient's records}

## Assessment
{Clinical interpretation — what do these findings mean?}

## Recommendations
1. {Specific recommendation}
2. ...

## Evidence Cited
| Source | Finding | Implication |
|---|---|---|
| status_tables/1.1_cardiology.html | BP 138/86 | Pre-hypertension; no contraindication to surgery |
| status_tables/1.2_pulmonology.html | FEV1 55% predicted | Moderate COPD — increased surgical risk |

## Concerns / Contraindications
{Any reason this department would advise AGAINST a particular intervention}

## Data Gaps
{What's missing that this department needs to make a confident recommendation}
```

### pre_meeting/evidence_summary.md

```markdown
# Objective Evidence Summary

## Imaging Findings
| Study | Date | Key Finding | Source |
|---|---|---|---|
| | | | |

## Pathology Findings
| Specimen | Date | Diagnosis | Source |
|---|---|---|---|
| | | | |

## Laboratory Findings
| Test | Value | Date | Reference Range | Source |
|---|---|---|---|
| | | | | |

## Clinical Exam Findings
| System | Finding | Date | Source |
|---|---|---|---|
| | | | |

## Known Diagnoses
| Diagnosis | Date | Status | Source |
|---|---|---|---|
| | | | |
```

---

## Meeting Templates

### meeting/minutes.md

```markdown
# MDT Meeting Minutes — {patient_id}

**Date/Time:** YYYY-MM-DD HH:MM
**Duration:** {estimated}
**Attendees:** {list of departments represented}

## 1. Case Presentation
{Presented by: referring physician / chair}
{Summary of presentation}

## 2. Objective Data Review
{Imaging reviewed: list}
{Pathology reviewed: list}
{Undisputed facts established}

## 3. Departmental Positions

### {Department 1} Position
- Assessment: ...
- Recommendation: ...
- Evidence basis: ...

### {Department 2} Position
- Assessment: ...
- Recommendation: ...
- Evidence basis: ...

## 4. Conflicts Identified

### Conflict #{N}: {Topic}
- Dept A position: ...
- Dept B position: ...
- Resolution framework applied:
  1. Guidelines consulted: {citation}
  2. Risk comparison: {summary}
  3. Patient factors: {summary}
  4. Chair decision: {decision with rationale}

## 5. Consensus Outcome
**Outcome Type:** {Therapeutic Intervention / Further Diagnostics / Surveillance / Referral / Palliative Care}
**Decision:** {detailed plan}
**Responsible Department:** {who executes}
**Timeline:** {when}

## 6. Dissenting Opinions
{Any recorded dissents with rationale}

## 7. Action Items
| # | Action | Responsible | Deadline |
|---|---|---|---|
| 1 | | | |
```

### meeting/conflicts_resolution.md

```markdown
# Conflict Resolution Log — {patient_id}

{Only present if conflicts were identified}

## Conflict 1: {Topic}
- **Departments involved:** {list}
- **Nature of disagreement:** {description}
- **Guideline reference:** {citation}
- **Risk comparison:**
  | Option | Morbidity Risk | Mortality Risk | Quality of Life Impact |
  |---|---|---|---|
  | A | | | |
  | B | | | |
- **Patient factors considered:** ECOG {score}, comorbidities, stated preferences
- **Resolution:** {chair's decision with full rationale}
- **Dissenting opinion recorded by:** {if any}
```

---

## Consensus Report (consensus_report.html)

Self-contained HTML with:
1. Header: patient ID, MDT date, scope, chair
2. Executive Summary: the decision in one paragraph
3. Case Background: from profile
4. Evidence Review: imaging, pathology, labs summary tables
5. Departmental Positions: each department's assessment
6. Conflict Resolution: if applicable
7. Consensus Decision: outcome type, detailed plan, timeline, responsible departments
8. Implementation Plan: orders, referrals, follow-up
9. Patient Communication Summary: plain language version
10. Signatures block: for chair and coordinator

---

## Follow-Up Plan (follow_up_plan.md)

```markdown
# Follow-Up Plan — {patient_id}

## Immediate Actions (within 7 days)
| Action | Department | Deadline |
|---|---|---|
| | | |

## Short-Term Follow-Up (within 30 days)
| Assessment | Department | Date |
|---|---|---|
| | | |

## MDT Re-Evaluation
**Scheduled:** YYYY-MM-DD
**Triggers for earlier re-evaluation:**
- {clinical trigger 1}
- {clinical trigger 2}

## Outcome Tracking
| Metric | Baseline | Target | Assessment Date |
|---|---|---|---|
| | | | |
```

---

## Quality Audit (quality_audit.md)

```markdown
# MDT Quality Self-Audit — {patient_id}

| Indicator | Status | Notes |
|---|---|---|
| Complete pre-meeting data available | Yes/No | |
| All required departments represented | Yes/No | |
| Consensus reached without deferral | Yes/No | |
| Evidence cited for all recommendations | Yes/No | |
| Documentation completed within timeline | Yes/No | |
| Patient communication plan documented | Yes/No | |
| Follow-up scheduled | Yes/No | |

## Process Improvements Identified
{Any lessons learned for future MDT sessions}
```
