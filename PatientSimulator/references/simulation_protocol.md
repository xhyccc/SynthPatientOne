# Patient Simulation Protocol

## Purpose

Given a patient profile with known values, unknown variables, and deprecated data,
generate N independent, clinically plausible simulated completions of the patient's
profile. Each simulation fills all ❌ Not Known and 📅 Deprecated variables with
reasonable predicted values, producing a complete hypothetical patient for downstream
analysis (clinical trial simulation, synthetic cohort generation, counterfactual analysis).

---

## Simulation Methodology

### Step 1 — Input Analysis

For each ❌ Not Known or 📅 Deprecated variable across all 36 departments, classify it:

| Category | Description | Prediction Strategy |
|---|---|---|
| **Demographic-correlated** | Value strongly correlated with age, sex, BMI, smoking status | Use population norms adjusted for demographics |
| **Disease-correlated** | Value expected given existing diagnoses | Predict based on known disease severity and typical progression |
| **Treatment-correlated** | Value influenced by known medications | Predict based on medication effects and compliance |
| **Independent screening** | Standard screening tests unrelated to known conditions | Predict from general population prevalence |
| **History-deprecated** | Old value exists in history table | Use trend from last known value with noise |

### Step 2 — Prediction Rules

For each variable, the LLM MUST follow these constraints:

1. **Never violate known facts.** If the patient has a known diagnosis of CKD Stage 3 with eGFR 45, a simulated eGFR of 90 is implausible.
2. **Respect physiological correlations.** LDL, HDL, and triglycerides must be internally consistent. HbA1c and fasting glucose must align.
3. **Use history when available.** If a deprecated value exists (e.g., HbA1c 8.2% from 2023-01), use it as an anchor — simulate a plausible trajectory from that point to the present. Typically: regression toward the mean with noise.
4. **Independent across simulations.** Each of the N simulations must be generated independently. Use different random seeds. Simulations should explore different reasonable clinical trajectories — not just N variations of the same prediction.
5. **Document every prediction.** Every simulated value must have a reasoning trace: which factors influenced the prediction, what distribution was used, and why this specific value was chosen.

### Step 3 — Simulation Diversity (N independent trajectories)

For N simulations, the LLM should vary the following across runs:

| Dimension | Variation |
|---|---|
| **Disease progression** | Faster vs. slower progression for chronic conditions |
| **Treatment response** | Good vs. poor response to known medications |
| **Complication emergence** | Whether new complications develop from known risk factors |
| **Lifestyle factors** | Smoking cessation vs. continuation, weight change |
| **Lab noise** | Values drawn from plausible clinical distributions |
| **Missing diagnosis resolution** | In some simulations, a suspected-but-unconfirmed diagnosis (from the profile's Potential Missing Diagnoses section) IS present; in others it is absent. Vary which suspected conditions manifest across the N runs. |
| **Diagnostic reliability** | In some simulations, simulate the outcome where a flagged test result was a false positive or false negative (from the profile's Diagnostic Reliability Flags section) — showing how management would differ if the original result was erroneous. |
| **Trajectory branch** | For each active condition with a non-stable projected trajectory, create simulations that follow the progression path versus those that plateau or improve. |

Each simulation gets a **Scenario Label** (e.g., "Stable, Well-Controlled", "Progressive Decline", "Partial Response", "Complication Cascade", "Missed Diagnosis Confirmed", "Diagnostic False Positive — Revised Workup", "Trajectory Inflection — Early Decompensation") and a **Seed ID** (e.g., `sim_01_seed_20250621_abc`).

### Step 4 — Simulation Table Format

Each simulation table mirrors the status table format but replaces the Status column:

| Column | Original Status Table | Simulation Table |
|---|---|---|
| Variable | Same | Same |
| Expected | Same | Same |
| Latest Value | Known values from profile | Known values unchanged |
| Value Age | From profile | From profile |
| Status | ✅/⚠️/📅/❌ | 🔮 Simulated for originally ❌/📅 variables; ✅ unchanged for known |
| Date | Original date | "Simulated (YYYY-MM-DD)" |
| Source | Original source | "Simulation — Seed: {seed_id}" |
| Comment | Original comment | **Reasoning trace:** why this value was predicted |
| **Simulation Confidence** | N/A (new column) | High/Medium/Low — how confident is this prediction? |

### Step 5 — profile_simulation_{i}.html Structure

Each HTML file contains four collapsible sections:

1. **Status (from profile):** The original status tables, unmodified. Source: `{patient_id}_profile/status_tables/`.
2. **Simulation (predicted completion):** The simulation tables with 🔮 Simulated values. Every cell that was originally ❌/📅 now has a predicted value. Known values unchanged.
3. **Reasoning Traces:** A structured narrative showing, for each predicted variable:
   - Original status (❌ Not Known / 📅 Deprecated with old value)
   - Factors considered (demographics, diagnoses, history, correlations)
   - Prediction method (population norm adjusted, disease model, trend extrapolation, etc.)
   - Predicted value with confidence
   - Alternative plausible values considered
4. **History (combined):** Original history tables + simulated events that would have occurred to produce the predicted current values. New events marked as 🔮.

---

## Reproducibility

Each simulation run MUST record:

```yaml
simulation_id: sim_01
seed: "{timestamp}_{random_suffix}"
scenario_label: "Stable, Well-Controlled"
generation_date: "YYYY-MM-DD HH:MM:SS"
model: "{LLM model used}"
N_total: 20
profile_source: "{path to patient_id}_profile/"
variables_simulated:
  total_predicted: {count}
  confidence_high: {count}
  confidence_medium: {count}
  confidence_low: {count}
```

---

## Audit Log Specification

Each simulation produces a log file `logs/simulation_{i}.log` with:

```
======================================================================
SIMULATION LOG — sim_{i} / {N}
Seed: {seed_id}
Scenario: {scenario_label}
Generated: YYYY-MM-DD HH:MM:SS
======================================================================

=== SIMULATION INPUT ANALYSIS ===
Total variables in profile: {N}
✅ Known (unchanged): {count}
📅 Deprecated (to predict): {count}
❌ Not Known (to predict): {count}
Total to simulate: {count}

=== PREDICTION DETAIL ===

--- Department: 1.1 Cardiology ---
Row 3 — Lipid Panel — LDL:
  Original status: ❌ Not Known
  Factors considered:
    - Demographics: Age 58M, BMI 31.2 (obese)
    - Diagnoses: Hypertension, Type 2 Diabetes
    - Treatment: Not on statin
    - Population: NHANES data suggests mean LDL ~115 for similar profile
  Prediction method: Disease-correlated + demographic-adjusted
  Distribution used: Normal(μ=125, σ=25)
  Predicted value: 132 mg/dL
  Confidence: Medium
  Alternative considered: 98 mg/dL (if on statin — but not prescribed)
  Rationale: Diabetic patients typically have mixed dyslipidemia. Without
    statin therapy, LDL in 110-150 range is most probable. Chose 132 as
    modal value for untreated diabetic male with obesity.

Row 6 — 12-Lead ECG:
  Original status: ❌ Not Known
  Factors considered:
    - Diagnoses: Hypertension (Stage 1)
    - Age: 58
    - No history of chest pain, palpitations, or syncope
  Prediction method: Population norm adjusted
  Predicted value: Normal sinus rhythm, possible LVH by voltage criteria
    (given hypertension duration)
  Confidence: Medium
  Rationale: ~30% of hypertensive patients show LVH on ECG. Borderline
    prediction — could go either way.

... [for every predicted variable]

=== SIMULATION SCENARIO RATIONALE ===
Scenario: {scenario_label}
Why this scenario: {explanation of the chosen trajectory — what assumptions
were made about disease progression, treatment response, lifestyle}

=== INTERNAL CONSISTENCY CHECK ===
{List of cross-variable consistency verifications}
- LDL 132 vs Total Cholesterol: consistent (assuming HDL ~40, TG ~180 → TC ~208)
- HbA1c 7.1% vs Fasting Glucose 142: consistent for Type 2 DM
- ...

=== SIMULATION SEED ===
seed: {seed_id}
For reproducibility, re-running with this seed and the same model
SHOULD produce identical results. The seed encodes all random choices
made during this simulation.
```
