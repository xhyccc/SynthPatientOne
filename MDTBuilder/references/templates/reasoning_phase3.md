# Phase 3 Reasoning — MDT Meeting

## Case Presentation Template

```
# Case Presentation — {patient_id}
**Presented by:** {referring physician / chair}
**Date/Time:** YYYY-MM-DD HH:MM

## Patient Summary
{3-5 sentences: demographics, key diagnoses, recent clinical course,
the event that triggered MDT referral, current status.}

## Core Clinical Question
{The question the MDT must answer.}

## Relevant History
{Timeline of key events from history tables and status tables.}
```

## Objective Data Review Template

```
# Objective Data Review

## Imaging Presented
{For each imaging study:}
- **{Study Type} ({date}):** {key finding}. Displayed to team. Consensus on interpretation: {yes/no/qualified}.
- Source: status_tables/7.1_radiology_imaging.html

## Pathology Presented
{For each pathology specimen:}
- **{Specimen} ({date}):** {diagnosis, grade, stage}. Reviewed by Pathology. Consensus: {yes/no/qualified}.
- Source: status_tables/7.2_pathology.html

## Key Lab Values Confirmed
| Test | Value | Date | Clinical Significance |
|---|---|---|---|
| {test} | {value} | {date} | {significance} |

## Undisputed Facts Established
{List facts that ALL departments agree on. These are the foundation
for the discussion. No department may dispute these without new evidence.}
```

## Departmental Position Template

For each participating department:

```
### {Department Name} Position
**Assessment:**
{This department's clinical assessment of the patient. What is the
patient's status from this specialty's perspective?}

**Recommendation:**
{What does this department recommend? Be specific:
- Intervention (what, when, how)
- Further diagnostics (which tests, why)
- Contraindications (what should NOT be done)}

**Evidence Basis:**
{List specific sources:
- status_tables/{dept}.html — row {N}: {variable} = {value}
- Guideline: {e.g., GOLD 2024, ADA 2025, ACC/AHA 2019}
- Clinical reasoning: {logic chain}}

**Confidence in Recommendation:** High / Medium / Low
**Reason for Confidence Level:** {explanation}
```

## Conflict Resolution Template

```
# Conflict Resolution Log

## Conflict #{N}: {Topic}

### Departments in Disagreement
- **{Dept A}** position: {summary}
- **{Dept B}** position: {summary}

### Point of Disagreement
{Exactly what do they disagree on? Be specific.}

### Guideline Consultation
{Guideline cited: NCCN / ESC / AHA / GOLD / ADA / etc.}
{Guideline recommendation for this scenario:}
{Guideline source: {URL or reference}}

### Risk Comparison
| Option | Dept A Recommendation | Dept B Recommendation |
|---|---|---|
| **Morbidity Risk** | {estimate} | {estimate} |
| **Mortality Risk** | {estimate} | {estimate} |
| **Quality of Life Impact** | {estimate} | {estimate} |
| **Evidence Strength** | {level} | {level} |

### Patient Factors Considered
- ECOG / Performance Status: {score}
- Comorbidities affecting decision: {list}
- Patient stated preferences (if documented): {preferences}
- Age / Frailty: {assessment}

### Chair Decision
**Decision:** {which recommendation is adopted, or a compromise}
**Rationale:** {full explanation of why this decision was made}
**Dissenting Opinion Recorded by:** {dept name, or "None — consensus reached"}
```

## Consensus Outcome Template

```
# Consensus Outcome

**Outcome Type:** {one of the five standard outcomes}

## Selected Outcome: {type}

### Decision Detail
{Full description of what will happen. Who does what, by when.}

### Responsible Department
{Primary department responsible for execution.}

### Timeline
- Immediate (within 24h): {actions}
- Short-term (within 7 days): {actions}
- Medium-term (within 30 days): {actions}

### Success Criteria
{How will we know the intervention worked? Measurable endpoints.}

### Contingency Plan
{If the primary plan fails or is delayed, what is Plan B?}

## Five Standard Outcomes

| # | Outcome | When to Choose |
|---|---|---|
| 1 | Therapeutic Intervention (Medical) | Clear diagnosis, evidence-based pharmacotherapy available |
| 2 | Therapeutic Intervention (Surgical) | Surgical candidate, risk/benefit favorable |
| 3 | Further Diagnostics Required | Critical data missing; decision deferred pending results |
| 4 | Active Surveillance / Monitoring | Low-risk condition; intervention not yet indicated |
| 5 | Referral to External Specialist | Expertise not available within this MDT |
| 6 | Palliative / Supportive Care | Curative options exhausted or patient preference |
```
