# MDT Evaluation Output Specification

## Output Folder Structure

Given simulation folder `{patient_id}_simulation/` and MDT result folder `{patient_id}_profile/mdt/`:

```
{patient_id}_MDT_eval/
├── per_simulation/
│   ├── eval_sim_01.html              # Full evaluation for simulation #1
│   ├── eval_sim_02.html              # Full evaluation for simulation #2
│   ├── ...
│   └── eval_sim_N.html
├── logs/
│   ├── eval_sim_01.log               # Evaluation audit log — sim #1
│   ├── eval_sim_02.log
│   ├── ...
│   └── eval_summary.log              # Cross-simulation aggregate log
├── aggregate_report.html             # Aggregate report across all N simulations
├── score_matrix.json                 # N×M score matrix (N simulations × M metrics)
├── sensitivity_analysis.md           # Which variables most influenced outcomes
└── eval_manifest.json                # Index with metadata
```

---

## per_simulation/eval_sim_{i}.html Format

Self-contained HTML with collapsible sections. Template: `assets/eval_report_template.html`.

### Sections

1. **Evaluation Header:** Simulation ID, seed, scenario label, MDT decision, eval date.
2. **Dimension 1 — Clinical Outcomes:** Diagnostic concordance, guideline adherence, predicted morbidity/mortality, complication risk assessment.
3. **Dimension 2 — Process Efficiency:** Time-to-treatment estimate, implementation feasibility, data completeness for the case, quorum assessment.
4. **Dimension 3 — Patient Experience:** Predicted functional outcome, shared decision-making quality, psychosocial support adequacy.
5. **Dimension 4 — Team Dynamics:** Psychological safety indicators, meeting efficiency, documentation quality.
6. **Overall Score:** Weighted aggregate with dimension breakdown.
7. **Sensitivity Note:** Which simulated variables most influenced the evaluation score.

### Scoring Format

Each metric is scored on a 0-100 scale with color coding:

| Score Range | Color | Label |
|---|---|---|
| 90-100 | Green | Excellent |
| 75-89 | Light green | Good |
| 60-74 | Yellow | Adequate |
| 40-59 | Orange | Needs Improvement |
| 0-39 | Red | Poor |

Each score must include:
- **Observed value:** What the evaluation found.
- **Benchmark:** What the standard/guideline expects.
- **Rationale:** Why this score was assigned.
- **Sensitivity:** How this score varies across the N simulations.

---

## logs/eval_sim_{i}.log Format

```
======================================================================
EVALUATION LOG — sim_{i} / {N}
Seed: {seed_id}
Scenario: {scenario_label}
MDT Decision: {outcome_type}
Evaluated: YYYY-MM-DD HH:MM:SS
======================================================================

=== DIMENSION 1: CLINICAL OUTCOMES ===

Metric 1.1 — Diagnostic Concordance:
  MDT diagnosis: {from consensus_report.html}
  Simulated ground truth: {from simulation_tables_i}
  Concordance: {match / partial / mismatch}
  Score: {0-100}
  Rationale: {explanation}

Metric 1.2 — Guideline Concordance:
  MDT recommendation: {treatment plan}
  Applicable guideline: {NCCN/ESC/AHA citation}
  Concordance: {conformant / deviation with justification / deviation without justification}
  Score: {0-100}
  Rationale: {explanation}

Metric 1.3 — Predicted Morbidity Risk:
  Intervention: {from MDT plan}
  Simulated patient factors: {from simulation_tables_i}
  Predicted complication risk: {low / moderate / high}
  Score: {0-100}
  Rationale: {comparing simulated patient status to procedure risk profile}

Metric 1.4 — Predicted Mortality Risk:
  ... (same structure)

=== DIMENSION 2: PROCESS EFFICIENCY ===
... (same per-metric structure)

=== DIMENSION 3: PATIENT EXPERIENCE ===
... (same per-metric structure)

=== DIMENSION 4: TEAM DYNAMICS ===
... (same per-metric structure)

=== OVERALL SCORE ===
Dimension 1: {weighted_score}
Dimension 2: {weighted_score}
Dimension 3: {weighted_score}
Dimension 4: {weighted_score}
Overall: {aggregate_score}

=== SENSITIVITY ANALYSIS ===
Top 5 variables influencing outcome:
  1. {variable} — {impact_description}
  ...
```

---

## aggregate_report.html

Aggregates results across all N simulations:

1. **Executive Summary:** Overall MDT quality score with confidence interval.
2. **Dimension Score Distribution:** Box plots / histograms per dimension across N simulations.
3. **Simulation-by-Simulation Heatmap:** N rows × metrics columns, color-coded.
4. **Outcome Concordance Rate:** How often MDT decision would be correct across simulations.
5. **Key Sensitivity Drivers:** Which variables most influenced variability.
6. **Recommendations:** What the MDT should improve based on simulation evaluation.

---

## score_matrix.json

```json
{
  "patient_id": "...",
  "N_simulations": 20,
  "metrics": [
    "diagnostic_concordance",
    "guideline_concordance",
    "predicted_morbidity",
    "predicted_mortality",
    "time_to_treatment",
    "implementation_rate",
    "data_completeness",
    "quorum_quality",
    "proms_prediction",
    "shared_decision_making",
    "psychosocial_support",
    "psychological_safety",
    "meeting_efficiency",
    "documentation_quality"
  ],
  "scores": [
    {
      "sim_id": "sim_01",
      "seed": "sim_01_20250621_x7k",
      "scenario": "Stable, Well-Controlled",
      "dimension_1": { "diagnostic_concordance": 92, "guideline_concordance": 88, ... },
      "dimension_2": { ... },
      "dimension_3": { ... },
      "dimension_4": { ... },
      "overall": 84.5
    },
    ...
  ],
  "aggregate": {
    "mean_overall": 82.3,
    "std_overall": 6.7,
    "min_overall": 68,
    "max_overall": 95,
    "per_dimension_means": { "1": 85.1, "2": 78.3, "3": 80.2, "4": 85.7 }
  }
}
```

---

## sensitivity_analysis.md

Identifies which simulated variables most influenced the evaluation:

```markdown
# Sensitivity Analysis — {patient_id}

## Most Influential Variables
| Rank | Variable | Dept | Variance in Outcome | Explanation |
|---|---|---|---|---|
| 1 | HbA1c | 1.4 Endocrinology | High | When simulated HbA1c > 8%, surgical risk score drops by 15+ points |
| 2 | Ejection Fraction | 1.1 Cardiology | Medium | When EF < 40%, mortality risk doubles |

## Robustness Assessment
- MDT decision is **robust** to variations in: {list of variables where outcome doesn't change}
- MDT decision is **sensitive** to variations in: {list of variables where outcome changes significantly}

## Scenario Clusters
- Simulations in cluster "Aggressive Disease" (sims 3,7,12,18): mean eval score 72
- Simulations in cluster "Stable Disease" (sims 1,5,9,14,20): mean eval score 91
```

---

## Reproducibility

| Element | Mechanism |
|---|---|
| Evaluation seed | `eval_{patient_id}_{YYYYMMDD}_{random4}` |
| Simulation seeds | Read from simulation_manifest.json |
| MDT decision | Read from consensus_report.html |
| All scores | Documented with rationale in logs/ |
| Aggregate stats | Computed deterministically from score_matrix.json |
