---
name: MDTEval
description: >
  Evaluate Multidisciplinary Team (MDT) decisions against N simulated patient profiles.
  Given a simulation folder ({patient_id}_simulation/) and MDT result folder
  ({patient_id}_MDT/), evaluate the MDT's performance across four core dimensions:
  (1) Clinical Outcomes & Efficacy — diagnostic concordance, guideline adherence, predicted
  morbidity/mortality across simulations; (2) Process & Operational Efficiency — time-to-treatment,
  implementation feasibility, data completeness, quorum quality; (3) Patient Experience & Quality
  of Life — predicted functional outcomes, shared decision-making, psychosocial support;
  (4) Team Dynamics & Governance — psychological safety, meeting efficiency, documentation quality.
  Produces per-simulation evaluation reports, cross-simulation aggregate analysis, sensitivity
  analysis identifying which variables most influenced outcomes, and a score matrix for statistical
  use. All evaluations are reproducible via seeds and fully documented in audit logs.
---

# MDT Evaluator

## Overview

Given the output of `PatientSimulator` (N simulated patient profiles) and the output of
`MDTBuilder` (the MDT consensus report), this skill evaluates **how well the MDT's decisions
hold up** across N different clinically plausible versions of the same patient.

For each simulation, the LLM asks: *"If the patient actually had these simulated values,
would the MDT's recommendation still be correct? What would the outcomes be?"*

The result is a comprehensive evaluation with per-simulation scores, cross-simulation
aggregate statistics, sensitivity analysis, and actionable recommendations for MDT improvement.

### What the Pipeline Produces

```
{patient_id}_MDT_eval/
├── per_simulation/
│   ├── eval_sim_01.html              # Full evaluation per simulation
│   └── ... (N files)
├── logs/
│   ├── eval_sim_01.log               # Per-sim audit log
│   └── eval_summary.log              # Aggregate log
├── aggregate_report.html             # Cross-simulation visual report
├── score_matrix.json                 # N×M numerical scores
├── sensitivity_analysis.md           # Variable influence analysis
└── eval_manifest.json                # Metadata index
```

### Core Principle

**The MDT is evaluated against clinical ground truth.** The N simulated profiles provide
N different "what-if" realities. The MDT's single decision is tested against all N realities.
A good MDT decision is robust — it performs well across most simulations. A poor MDT
decision collapses when key assumptions turn out differently.

---

## When to Use This Skill

- Audit MDT decision quality against a range of plausible patient presentations.
- Identify which missing clinical data (unknown factors) most critically affect MDT decisions.
- Quantify the risk that an MDT recommendation is wrong due to incomplete patient data.
- Compare MDT performance across different patient cohorts or time periods.
- Generate evidence for quality improvement initiatives.
- Train MDT members on decision robustness using simulated scenarios.

---

## Four Evaluation Dimensions

Full framework in `references/eval_framework.md`.

### Dimension 1: Clinical Outcomes & Efficacy (weight: 40%)

| Metric | How Evaluated |
|---|---|
| **Diagnostic Concordance** | Does MDT diagnosis match the simulated patient's actual (simulated) pathology? |
| **Guideline Concordance** | Does MDT treatment plan follow NCCN/ESC/AHA/etc. guidelines given simulated values? |
| **Predicted Morbidity** | What complication risk does the MDT-chosen intervention carry for this simulated patient? |
| **Predicted Mortality** | What is the estimated mortality risk of the MDT plan for this simulated patient? |

### Dimension 2: Process & Operational Efficiency (weight: 25%)

| Metric | How Evaluated |
|---|---|
| **Time-to-Treatment** | Would the MDT plan be executable within benchmark timeframes given simulated patient status? |
| **Implementation Feasibility** | Can the recommended intervention actually be performed given simulated contraindications? |
| **Data Completeness** | Were all necessary data points available at MDT time? (from profile's Unknown Factors Audit) |
| **Quorum Quality** | Were all required departments represented? (from MDT minutes) |

### Dimension 3: Patient Experience & Quality of Life (weight: 20%)

| Metric | How Evaluated |
|---|---|
| **Predicted Functional Outcome** | Based on simulated patient factors, what functional status is expected post-intervention? |
| **Shared Decision-Making** | Is there documented evidence of patient communication? (from MDT patient_summary.md) |
| **Psychosocial Support** | Did the MDT plan include mental health, social work, or palliative referrals when indicated? |

### Dimension 4: Team Dynamics & Governance (weight: 15%)

| Metric | How Evaluated |
|---|---|
| **Psychological Safety** | Are dissenting opinions recorded? Is there evidence of open discussion? |
| **Meeting Efficiency** | Was the case discussed efficiently? (assess from minutes structure) |
| **Documentation Quality** | Are MDT notes clear, legally sound, and actionable? |

---

## Workflow

### Phase 0 — Setup

1. Read `{patient_id}_MDT/consensus_report.html` — extract the MDT decision.
2. Read `{patient_id}_simulation/simulation_manifest.json` — get all N simulation seeds and scenarios.
3. Create `{patient_id}_MDT_eval/` with all subdirectories.


### Scenario-to-Score Mapping Rationale

For each simulation scenario, the LLM MUST explain WHY the assigned score differs from the baseline:

1. **Baseline score** = evaluation on the original profile (sim_01 or the scenario closest to the original data).
2. **Delta analysis** for each subsequent simulation:
   - Which simulated variables changed from baseline?
   - How did each changed variable affect each dimension score?
   - Was the effect linear (small change → small score delta) or threshold (variable crosses a clinical threshold → large score drop)?

Example: If sim_02 simulates LDL=145 (vs baseline LDL=88), and sim_02's D1 score drops by 10 points:
  → "LDL increase from 88→145 crosses the <100 guideline threshold, reducing Guideline Concordance from 95→80 and driving a 10-point D1 drop. This is a threshold effect, not linear."

### Evaluation Sensitivity Table

| Variable | Baseline | Worst-Case Simulated | Score Delta | Threshold? |
|---|---|---|---|---|
| LDL | 88 | 145 | -10 D1 | Yes (<100 threshold) |
| HbA1c | 6.8% | 8.5% | -8 D1 | Yes (<7.0% target) |
### Phase 1 — Per-Simulation Evaluation

For each simulation `i` (1 to N):

1. Read `simulation_tables_{i}/` — this is the "ground truth" patient for this simulation.
2. Read the MDT decision from `consensus_report.html`.
3. For each of the 14 metrics across 4 dimensions, evaluate:
   - Compare MDT decision against simulated patient values.
   - Score 0-100 with rationale.
   - Document in `logs/eval_sim_{i}.log`.
4. Write `per_simulation/eval_sim_{i}.html` using the template at `assets/eval_report_template.html`.

### Phase 2 — Cross-Simulation Analysis

1. Compile `score_matrix.json` — N×14 numerical matrix.
2. Compute aggregate statistics: mean, std, min, max per metric and per dimension.
3. Identify **sensitivity drivers**: which simulated variables most influenced evaluation scores.
4. Write `sensitivity_analysis.md`.

### Phase 3 — Aggregate Report

Write `aggregate_report.html`:
1. Executive summary with overall MDT quality score and confidence interval.
2. Dimension score distributions across N simulations.
3. Simulation-by-simulation heatmap.
4. Key sensitivity drivers and recommendations.

### Phase 4 — Audit Logs

Write `logs/eval_summary.log` with aggregate statistics and evaluation methodology notes.

---

## Scoring

| Score Range | Color | Label |
|---|---|---|
| 90-100 | Green | Excellent |
| 75-89 | Light green | Good |
| 60-74 | Yellow | Adequate |
| 40-59 | Orange | Needs Improvement |
| 0-39 | Red | Poor |


### Dimension Weight Justification

The overall MDT score is a weighted average: **0.40×D1 + 0.25×D2 + 0.20×D3 + 0.15×D4**

**Rationale for weights:**

| Dimension | Weight | Why |
|---|---|---|
| D1: Clinical Outcomes | 40% | Patient health outcomes are the primary purpose of MDT. Diagnostic accuracy and treatment appropriateness directly affect morbidity and mortality. |
| D2: Process Efficiency | 25% | Timely, feasible care delivery affects real-world outcomes. An excellent clinical plan that takes 6 months to execute is a failed plan. |
| D3: Patient Experience | 20% | Patient-centered care is a core quality domain. Shared decision-making and psychosocial support affect adherence and satisfaction. |
| D4: Team Dynamics | 15% | Team function is an enabler of D1-D3, not an end in itself. A well-functioning team that makes wrong clinical decisions still harms patients. |

If the MDT context is PURELY DIAGNOSTIC (no treatment decision), adjust to: 0.50×D1 + 0.20×D2 + 0.15×D3 + 0.15×D4.
**Weighted Overall:** `0.40×D1 + 0.25×D2 + 0.20×D3 + 0.15×D4`

---

## Reproducibility

| Element | Mechanism |
|---|---|
| Evaluation seed | `eval_{patient_id}_{YYYYMMDD}_{random4}` |
| All simulation seeds | From `simulation_manifest.json` |
| MDT decision | From `consensus_report.html` |
| Scores | Rationale documented in per-sim logs |
| Aggregate stats | Deterministic from `score_matrix.json` |

---

## Quick Start

Pure LLM reasoning. Activate with:

```
@MDTEval using simulation at /path/to/patient_001_simulation/
         and MDT at /path/to/patient_001_profile/mdt/
```

---

## References

| Reference | Content |
|---|---|
| `references/eval_framework.md` | Full 4-dimension framework, 14 metrics, scoring rubrics, cross-simulation analysis |
| `references/eval_output_spec.md` | Output folder structure, report templates, log formats, score matrix spec |

## Assets

| Asset | Content |
|---|---|
| `assets/eval_report_template.html` | HTML template for per-simulation evaluation — 4 dimensions with color-coded scoring, 46 LLM-fillable placeholders |

---

## Integration

| Skill | Output Used by MDTEval |
|---|---|
| `PatientProfileBuilder` | Unknown Factors Audit → identifies which data was missing at MDT time |
| `MDTBuilder` | consensus_report.html, minutes.md, patient_summary.md → the MDT decision being evaluated |
| `PatientSimulator` | simulation_tables_{i}/, simulation_manifest.json → N "ground truth" realities |

---

## Best Practices

1. **Evaluate against the simulation, not the profile.** The simulation is the ground truth for this eval run.
2. **Score with rationale.** Every 0-100 score must explain WHY.
3. **Sensitivity matters more than averages.** A mean score of 85 with range 40-95 is worse than a mean of 80 with range 75-85.
4. **Document confounders.** If a simulation scenario is extreme, note it — don't let one outlier drive conclusions.
5. **Actionable recommendations.** The aggregate report must tell the MDT what to improve.
6. **Reproducibility.** Every run has a seed. Same seed + same inputs = same scores.

## Limitations

- Evaluation is LLM-simulated, not based on real patient outcomes.
- Predicted morbidity/mortality are estimates, not actuarial data.
- Psychological safety and team dynamics are inferred from documentation — not directly measured.
- The evaluation is only as good as the simulation quality from PatientSimulator.
- This skill provides MDT quality assessment; it does not replace formal clinical audit.
