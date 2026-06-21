# Phase 1 Reasoning — Team Formation

## MDT Scope Determination

**Prompt for LLM:** Based on the patient profile, determine the MDT scope.

```
Patient Profile Summary:
{patient demographics from profile.html}
{key diagnoses from status_tables}
{critical unknowns from Unknown Factors Audit}

Reasoning:
1. What is the dominant clinical problem requiring multidisciplinary input?
2. Which organ systems are involved?
3. What is the urgency level?

MDT Scope: {e.g., Complex COPD + Cardiovascular Risk Management}
```

## Core Clinical Question

**Prompt for LLM:** Formulate the single most important question this MDT must answer.

```
Given:
- Key diagnoses: {list}
- Critical unknowns: {list}
- MDT scope: {scope}

Core Clinical Question: {one sentence that defines what the MDT must decide}
```

## Participating Departments

**Prompt for LLM:** Identify which departments must participate and why.

```
For each of the 36 secondary departments, assess:
1. Does this department have ✅ Known findings relevant to the MDT scope?
2. Does this department have ❌ Critical Unknowns that affect MDT decisions?
3. Would this department's opinion change the treatment plan?

Mandatory departments (must attend):
- {dept}: {rationale}

Optional departments (attend if available):
- {dept}: {rationale}

Not needed:
- {dept}: {rationale}
```

## Role Assignment

**Prompt for LLM:** Designate the Lead Clinician (Chair) and MDT Coordinator.

```
Lead Clinician (Chair): {typically the referring physician's department}
Rationale: {why this department leads}

MDT Coordinator: {typically Internal Medicine or the department managing the most comorbidities}
Rationale: {why this department coordinates}
```
