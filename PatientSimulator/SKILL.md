---
name: PatientSimulator
description: >
  Given a patient profile ({patient_id}_profile/) from PatientProfileBuilder and a simulation count N
  (default 20), generate N independent, clinically plausible simulated completions of the patient's
  profile. For each simulation: predict all ❌ Not Known and 📅 Deprecated variables using clinical
  reasoning informed by demographics, diagnoses, history trends, and physiological correlations;
  produce simulation status tables, a rich profile_simulation_{i}.html (status + simulation + reasoning
  traces + combined history), and medical-audit-grade simulation logs. All N simulations are independent
  with unique seeds, scenario labels, and varied clinical trajectories for reproducibility.
---

# Patient Simulator

## Overview

Given a patient profile `{patient_id}_profile/` (output of `PatientProfileBuilder`),
this skill generates **N independent simulated completions** of the patient's clinical
picture. Every variable marked ❌ Not Known or 📅 Deprecated in the original profile
is filled with a clinically plausible predicted value. Known variables are preserved unchanged.

The result is N complete, internally consistent hypothetical patient profiles suitable for:
synthetic cohort generation, clinical trial simulation, counterfactual analysis, sensitivity
testing, and ML training data augmentation.

### What the Pipeline Produces

```
{patient_id}_simulation/
├── [full copy of {patient_id}_profile/]     # Original profile as read-only reference
├── simulation_tables_1/                     # Simulated status tables — simulation #1
│   ├── 1.1_cardiology.html                  # (all 36 departments, 🔮 for predicted values)
│   └── ...
├── simulation_tables_2/                     # Simulation #2
│   └── ...
├── ... (N folders total)
├── simulation_tables_N/
│   └── ...
├── profile_simulation_1.html                # Full HTML: status + simulation + reasoning + history
├── profile_simulation_2.html
├── ...
├── profile_simulation_N.html
├── logs/
│   ├── simulation_1.log                     # Per-simulation audit trail
│   ├── ...
│   ├── simulation_N.log
│   └── simulation_summary.log               # Aggregate statistics across all N
└── simulation_manifest.json                 # Index with metadata for all simulations
```

### Core Principles

1. **Preserve known facts.** ✅ Known values are never altered. Simulation only fills gaps.
2. **Clinical plausibility.** Every prediction is grounded in demographics, diagnoses, history, and physiological correlations.
3. **Independence.** Each of the N simulations is generated independently with a unique random seed.
4. **Diversity.** Simulations explore different reasonable clinical trajectories — not N copies of the same prediction.
5. **Full audit trail.** Every predicted value has a reasoning trace. Every simulation has a log.

---

## When to Use This Skill

- Generate synthetic patient cohorts from a real patient profile for statistical analysis.
- Test how different clinical trajectories affect treatment decisions.
- Create counterfactual scenarios (what if this patient had different lab values?).
- Augment ML training data with plausible patient variations.
- Sensitivity analysis for clinical trial eligibility criteria.
- Demonstrate the range of possible clinical presentations given incomplete data.

---


### Distribution Sampling Guidance

When predicting unknown variables, the LLM MUST specify the distribution type and parameters:

| Variable Category | Default Distribution | Parameter Source |
|---|---|---|
| Lab values (continuous) | Normal(μ, σ) | μ = population mean adjusted for demographics; σ = population SD |
| Lab values (bounded, e.g., eGFR) | Truncated Normal(μ, σ, min, max) | Truncate at physiological limits |
| Binary variables (diagnosis Y/N) | Bernoulli(p) | p = prevalence adjusted for risk factors |
| Ordinal (tumor stage, NYHA class) | Categorical with ordered probabilities | Clinical staging distribution |
| Time-to-event (survival) | Exponential(λ) or Weibull | λ from literature |

**Seed encoding:** The seed string (e.g., "sim_01_20250621_a1b") determines all random draws.
If two simulations with the same seed produce different values, the simulation is INVALID.
## Simulation Methodology

Full methodology in `references/simulation_protocol.md`. Summary:

### Prediction Strategy by Variable Category

| Category | How to Predict |
|---|---|
| **Demographic-correlated** | Use population norms adjusted for age, sex, BMI |
| **Disease-correlated** | Predict from known disease severity and typical progression |
| **Treatment-correlated** | Predict based on medication effects and assumed compliance |
| **Independent screening** | Predict from general population prevalence |
| **History-deprecated** | Extrapolate trend from last known value + noise |

### Diversity Across N Simulations

For each simulation, vary:

| Dimension | How |
|---|---|
| Disease progression speed | Faster (sim 1-5) vs. slower (sim 16-20) |
| Treatment response | Good vs. partial vs. poor response |
| Complication emergence | Whether risk factors manifest as complications |
| Lifestyle trajectory | Smoking cessation, weight loss/gain |
| Lab noise | Values drawn from clinically informed distributions |

Each simulation gets a unique **Scenario Label** and **Seed ID**.

---

## Workflow

### Phase 0 — Setup

1. Copy `{patient_id}_profile/` contents into `{patient_id}_simulation/`.
2. Create `simulation_tables_1/` through `simulation_tables_N/`.
3. Create `logs/` directory.
4. Read the original profile thoroughly: status tables, history tables, profile.html, form_filling.txt.

### Phase 1 — Input Analysis

For each of the 36 departments, count:
- ✅ Known variables (will be preserved)
- 📅 Deprecated variables (will be predicted using history as anchor)
- ❌ Not Known variables (will be predicted from scratch)
- Total variables to simulate per department

Compute aggregate statistics for the simulation summary.

### Phase 2 — Generate N Independent Simulations

For **each** simulation `i` (1 to N):

**Step 2a. Assign scenario and seed.**
- Label the scenario (e.g., "Stable, Well-Controlled", "Progressive Decline").
- Generate a unique seed: `sim_{i:0{padding}d}_{YYYYMMDD}_{random3}`.


### Per-Variable Prediction Trace Format

For EVERY simulated variable, the LLM MUST record this structured trace in profile_simulation_{i}.html Section 3:


**Step 2b. Predict unknown variables.**
For each variable marked ❌ or 📅:
1. Classify the variable category (demographic/disease/treatment/screening/history).
2. Identify which known variables influence this prediction.
3. Choose a prediction method and a clinical distribution.
4. Sample a value from the distribution (vary across simulations using the seed).
5. Perform an internal consistency check against already-predicted correlated variables.
6. Record the prediction with full reasoning trace.

**Step 2c. Write simulation tables.**
The simulation tables use the **exact same format** as the original status tables from PatientProfileBuilder (same columns: #, Variable, Expected, Latest Value, Value Age, Status, Date, Source, Comment). The LLM:

1. Copies `{patient_id}_profile/status_tables/{dept}.html` into `simulation_tables_{i}/{dept}.html`.
2. Iterates through every row:
   - **✅ Known rows:** left completely unchanged.
   - **❌ Not Known rows:** fills Latest Value with the predicted value, sets Status to `🔮 Simulated` (CSS class `status-simulated`), sets Value Age to `"Simulated"`, sets Source to `"Simulation — Seed: {seed}"`, sets Comment to a brief reasoning trace + confidence level.
   - **📅 Deprecated rows:** same as Not Known, but Comment includes the old deprecated value and why it was superseded.

No new columns. No extra tables. The simulation tables are structurally identical to the originals — only the content of previously-empty cells changes.

**Step 2d. Write profile_simulation_{i}.html.**
Four collapsible sections:
1. Original Status (from profile) — read-only reference.
2. Simulated Profile — completed tables with 🔮 values.
3. Reasoning Traces — structured narrative for EVERY predicted variable.
4. Combined History — original + simulated events.

**Step 2e. Write simulation log.**
`logs/simulation_{i}.log` with:
- Input analysis counts.
- Per-variable prediction detail (factors, method, distribution, value, confidence, alternatives, rationale).
- Scenario rationale.
- Internal consistency verification.
- Seed for reproducibility.

### Phase 3 — Aggregate Summary

Write `logs/simulation_summary.log`:
- Aggregate statistics across all N simulations.
- Variables with highest variance across simulations.
- Variables that are consistent across all simulations.
- Distribution of scenario labels.

Write `simulation_manifest.json`:
- Index of all N simulations with metadata.

---

## Status Badges

| Badge | CSS Class | Meaning |
|---|---|---|
| ✅ Known | `status-known` | Original profile value, unchanged |
| 🔮 Simulated | `status-simulated` | Predicted by LLM |

---

## Confidence Levels

| Level | Meaning | When to Use |
|---|---|---|
| **High** | Strongly constrained by known data | e.g., eGFR predicted from known creatinine |
| **Medium** | Informed by demographics/diagnoses with moderate uncertainty | e.g., LDL predicted from diabetic+obese profile |
| **Low** | Largely independent of known data | e.g., screening colonoscopy result for asymptomatic patient |

---

## Reproducibility

Every simulation includes a `seed` that encodes all random choices. Re-running with the
same seed and model SHOULD produce identical results. The seed is recorded in:
- `profile_simulation_{i}.html` header
- `logs/simulation_{i}.log`
- `simulation_manifest.json`

---

## Quick Start

This skill is **pure LLM reasoning** — no scripts, no external tools.

1. Activate `@PatientSimulator` with a patient profile path.
2. Specify N (default: 20).
3. The LLM reads the profile, generates all N simulations, writes every file directly.

```
@PatientSimulator /path/to/patient_001_profile/ --N 20
```

---

## References

| Reference | Content |
|---|---|
| `references/simulation_protocol.md` | Full simulation methodology, prediction rules, reproducibility, audit log specification |
| `references/simulation_output_spec.md` | Output folder structure, table formats, naming conventions, manifest format |

## Assets

| Asset | Content |
|---|---|
| `assets/profile_simulation_template.html` | HTML template for profile_simulation_{i}.html — four collapsible sections |

---

## Integration with PatientProfileBuilder

PatientSimulator directly consumes PatientProfileBuilder output:

| PatientProfileBuilder Output | PatientSimulator Usage |
|---|---|
| `status_tables/*.html` | Ground truth — ✅ values preserved, ❌/📅 values identified for prediction |
| `history_tables/*.html` | Trend anchors for deprecated values; context for disease progression |
| `profile.html` | Overall clinical picture; demographic and diagnostic summary |
| `logs/form_filling.txt` | Audit trail for understanding which values are truly unknown vs. uncertain |

---

## Best Practices

1. **Preserve known facts.** ✅ values are NEVER altered.
2. **Clinical plausibility over statistical convenience.** A prediction must make clinical sense, not just be a population mean.
3. **Independence is mandatory.** Each simulation is a fresh generation, not a variant of sim_01.
4. **Full audit trail.** Every prediction has a reasoning trace. Every simulation has a log.
5. **Internal consistency.** Cross-check correlated variables before finalizing (LDL ↔ Total Cholesterol, HbA1c ↔ Fasting Glucose, etc.).
6. **Scenario diversity.** Use different clinical trajectories across simulations — conservative, aggressive, stable, progressive.
7. **Document the seed.** Reproducibility requires it.

## Limitations

- Simulated values are predictions, not measurements. They carry uncertainty.
- The LLM's clinical knowledge determines prediction quality — verify with domain experts.
- Simulations are only as good as the known data they're anchored to.
- Highly interdependent variables may be under- or over-constrained.
- This skill generates hypothetical data for analysis; it does not provide medical advice.
