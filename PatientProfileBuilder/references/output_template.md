# Patient Profile Output Template

This document specifies the exact output format for the generated patient profile.

## Profile Structure

```
1. Patient Demographics & Summary
2. Department Profiles (one section per secondary department)
   2.1. Variable Table (split: Known / Not Yet Known or Uncertain)
   2.2. Department Commentary
3. Cross-Departmental Synthesis
4. Priority Action Items
5. Source Manifest
```

## Section Details

### 1. Patient Demographics & Summary

```markdown
# Patient Profile: [Patient Name / ID]

**Generated:** YYYY-MM-DD
**Sources Reviewed:** N documents (types)
**Overall Completeness:** XX% of expected variables are known

| Field | Value |
|---|---|
| Age | XX years |
| Sex | Male / Female / Other |
| Chief Complaint(s) | ... |
| Key Diagnoses | ... |
| Allergies | ... |
| Current Medications | Drug (dose, frequency, route) |
```

### 2. Department Profiles

For each secondary department:

```markdown
### [First-Tier Department Name]

#### [Secondary Department Name] (e.g., 1.1 Cardiology)

**Department Scope:** [One-line summary]

##### Factors Known

| # | Variable | Value | Date | Source | Comment |
|---|---|---|---|---|---|
| 1 | Blood Pressure | 138/86 mmHg | 2025-03-01 | Visit note | Pre-hypertensive range |

##### Factors Not Yet Known / Uncertain

| # | Variable | Status | Expected Because | Comment |
|---|---|---|---|---|
| 1 | Lipid Panel | ❌ Not Known | Age > 40, standard screening | Recommended |
| 2 | Chest Pain | ⚠️ Uncertain | "Occasional tightness" per ED note | No workup documented |

##### Department Commentary

*Concise narrative: known findings → implications → critical gaps → suggested next steps.*
```

### 3. Cross-Departmental Synthesis

```markdown
## Cross-Departmental Synthesis

| Link | Departments Involved | Description |
|---|---|---|
| Diabetic complications | 1.4 Endocrinology + 1.5 Nephrology + 6.2 Ophthalmology | ... |
| Surgical risk | 1.1 Cardiology + 7.4 Anesthesiology | ... |
```

### 4. Priority Action Items

```markdown
## Priority Action Items

| Priority | Department | Missing Variable | Rationale |
|---|---|---|---|
| Urgent | 1.1 Cardiology | Lipid Panel | ASCVD risk stratification needed |
| High | 1.2 Pulmonology | Chest X-Ray | Dyspnea + smoking history |
| Routine | 1.7 Rheumatology | ANA | Joint pain workup |
```

### 5. Source Manifest

```markdown
## Source Manifest

| # | File | Format | Pages | Extraction Method | Date Extracted |
|---|---|---|---|---|---|
| 1 | discharge_summary.pdf | PDF (text) | 3 | pdfplumber | 2025-06-20 |
| 2 | lab_results.xlsx | Excel | 1 sheet | pandas | 2025-06-20 |
| 3 | referral_letter.jpg | Image | 1 | Tesseract OCR | 2025-06-20 |
```

## Status Definitions

| Status | Icon | Meaning |
|---|---|---|
| Known | ✅ | Explicitly stated with clear value |
| Uncertain | ⚠️ | Mentioned but ambiguous, contradictory, or qualified |
| Not Known | ❌ | Not mentioned but clinically expected |
| Not Applicable | N/A | Not relevant for this patient (e.g., OB/GYN for male) |
