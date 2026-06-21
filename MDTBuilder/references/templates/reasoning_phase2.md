# Phase 2 Reasoning — Pre-Meeting Workflow

## Departmental Review Template

For each participating department, produce a review following this structure:

```
# Departmental Review — {Department Name} ({dept_code})
**Reviewer:** {Department} Representative
**Date Reviewed:** YYYY-MM-DD
**Sources Consulted:** status_tables/{dept_code}.html, history_tables/{dept_code}.html

---

## Findings Summary

{What this department knows about the patient from the profile.
List key ✅ Known variables with values. Cite sources.}

## Assessment

{Clinical interpretation. What do these findings mean in the context of the MDT scope?
What is the patient's status from this department's perspective?}

## Recommendations

1. {Specific, actionable recommendation}
2. {Cited to guideline or evidence}
3. {Include timeline where applicable}

## Concerns / Contraindications

{Any reason this department would advise AGAINST a specific intervention.
E.g., "Recommend against surgical intervention due to severe COPD (FEV1 <50% predicted)."
Every concern MUST cite the evidence from the status table.}

## Data Gaps

{What missing data limits this department's ability to make a confident recommendation?
Reference: Unknown Factors Audit in profile.html.
For each gap: what test is needed, what decision it would inform, and how urgently.}
```

## Evidence Summary Template

```
# Objective Evidence Summary
**Compiled:** YYYY-MM-DD

## Imaging Findings
| Study | Date | Key Finding | Source |
|---|---|---|---|
| {study} | {date} | {finding} | status_tables/7.1_radiology_imaging.html |

## Pathology Findings
| Specimen | Date | Diagnosis | Source |
|---|---|---|---|
| {specimen} | {date} | {diagnosis} | status_tables/7.2_pathology.html |

## Key Laboratory Results
| Test | Value | Date | Reference | Source |
|---|---|---|---|
| {test} | {value} | {date} | {ref} | status_tables/7.3_laboratory_medicine.html |

## Clinical Findings (Physical Exam, Vitals)
| Finding | Value | Date | Source |
|---|---|---|---|
| {finding} | {value} | {date} | {source} |

## Known Diagnoses
| Diagnosis | Date | Status | Source |
|---|---|---|---|
| {diagnosis} | {date} | {status} | {source} |

## Key Unknown Factors (from profile Unknown Factors Audit)
| Dept | Variable | Status | Impact on MDT Decision |
|---|---|---|---|
| {dept} | {variable} | ❌/📅 | {how this gap affects decision-making} |
```

## Agenda Template

```
# MDT Agenda — {patient_id}
**MDT Date:** YYYY-MM-DD | **Scope:** {scope}
**Chair:** {chair_dept} | **Coordinator:** {coordinator_dept}

## Core Clinical Question
{the single question the MDT must answer}

## Case Summary
{2-3 sentence summary from profile.html}

## Participating Departments
| # | Department | Representative | Reason for Inclusion | Key Data to Present |
|---|---|---|---|---|
| 1 | {dept} | — | {rationale} | {what this dept will present} |

## Schedule
1. Case Presentation (5 min) — {presenter}
2. Objective Data Review — Radiology / Pathology (5 min)
3. Departmental Positions — each dept (3 min each)
4. Discussion & Conflict Resolution (10 min)
5. Consensus & Action Items (5 min)
```
