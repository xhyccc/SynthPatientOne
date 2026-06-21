# Patient Simulation Output Specification

## Output Folder Structure

Given `{patient_id}_profile/` and simulation count N (default: 20):

```
{patient_id}_simulation/
├── [full copy of {patient_id}_profile/ contents]
│   ├── raw/
│   ├── status_tables/              # Original status tables (read-only reference)
│   ├── history_tables/             # Original history tables (read-only reference)
│   ├── logs/
│   │   ├── translation.txt
│   │   ├── form_filling.txt
│   │   └── profile_gen.txt
│   └── profile.html                # Original profile
│
├── simulation_tables_1/            # Simulated status tables — simulation #1
│   ├── 1.1_cardiology.html
│   ├── 1.2_pulmonology.html
│   ├── ...
│   └── 7.5_rehabilitation_medicine.html
│
├── simulation_tables_2/            # Simulated status tables — simulation #2
│   └── ...
│
├── ... (N folders total)
│
├── simulation_tables_N/
│   └── ...
│
├── profile_simulation_1.html       # Full HTML: status + simulation + reasoning + history
├── profile_simulation_2.html
├── ...
├── profile_simulation_N.html
│
├── logs/                           # Simulation audit logs
│   ├── simulation_1.log
│   ├── simulation_2.log
│   ├── ...
│   ├── simulation_N.log
│   └── simulation_summary.log      # Aggregate statistics across all N simulations
│
└── simulation_manifest.json        # Index of all simulations with metadata
```

---

## Copy Protocol

When copying `{patient_id}_profile/` into `{patient_id}_simulation/`:

- All files under `{patient_id}_profile/` are copied recursively.
- The original `status_tables/` and `history_tables/` serve as **read-only ground truth**.
- The simulation writes INTO `simulation_tables_i/` — never overwrites the originals.
- `profile.html` is copied as reference; simulation produces separate `profile_simulation_i.html` files.

---

## Simulation Table Format

Simulation tables use the **exact same columns** as PatientProfileBuilder status tables:
`# | Variable | Expected | Latest Value | Value Age | Status | Date | Source | Comment`

They are produced by **copying the original status table HTML** and modifying only
the rows with ❌ Not Known or 📅 Deprecated. No new columns. No extra tables.

### Row Transformation Rules

| Original Status | Simulation Action |
|---|---|
| ✅ Known | **No change.** Row left exactly as-is. |
| ⚠️ Uncertain | **No change.** Uncertain values are not simulated — they require clinical clarification, not prediction. |
| ❌ Not Known | Fill `Latest Value` with predicted value. Set `Status` to `🔮 Simulated`. Set `Value Age` to `"Simulated"`. Set `Source` to `"Simulation — Seed: {seed}"`. Set `Comment` to reasoning trace + confidence level. |
| 📅 Deprecated | Same as Not Known, but `Comment` MUST include both the old deprecated value and why it was superseded: e.g., `"Deprecated: HbA1c 8.2% (2023-01). Simulated via trend extrapolation: 7.1%. Confidence: Medium."` |

### Status Badges

| Badge | CSS Class | Meaning |
|---|---|---|
| ✅ Known | `status-known` | Value from original profile, unchanged |
| ⚠️ Uncertain | `status-uncertain` | From original — flagged but not simulated |
| 🔮 Simulated | `status-simulated` | Predicted by LLM |

### Example: ❌ Not Known → 🔮 Simulated

**Before (from original status table):**
```html
<tr>
  <td>3</td>
  <td>Lipid Panel — LDL</td>
  <td>mg/dL; &lt;100 optimal</td>
  <td class="fill-me">—</td>
  <td class="fill-me">—</td>
  <td class="fill-me">❌ Not Known</td>
  <td class="fill-me">—</td>
  <td class="fill-me">—</td>
  <td class="fill-me"></td>
</tr>
```

**After simulation:**
```html
<tr>
  <td>3</td>
  <td>Lipid Panel — LDL</td>
  <td>mg/dL; &lt;100 optimal</td>
  <td>132 mg/dL</td>
  <td>Simulated</td>
  <td class="status-simulated">🔮 Simulated</td>
  <td>Simulated (2025-06-21)</td>
  <td>Simulation — Seed: sim_01_20250621_x7k</td>
  <td>Disease-correlated: diabetic male 58, BMI 31.2, no statin. Normal(μ=125,σ=25). Confidence: Medium.</td>
</tr>
```

### Required CSS Addition

Add to the `<style>` block of every simulation table (inherited from original + this addition):
```css
.status-simulated { background: #e8daef !important; color: #6c3483; font-weight: 600; }
```

---

## profile_simulation_{i}.html Format

Self-contained HTML with four collapsible `<details>` sections:

### Section 1 — Original Status (from profile)
Read-only display of the original status tables. Source: `status_tables/`.

### Section 2 — Simulated Profile
The completed profile — all 36 departments with:
- Known values (✅) preserved from original
- Simulated values (🔮) filling all gaps
- Color coding: known = green, simulated = blue/purple
- Completeness: now 100% (all variables have values)

### Section 3 — Reasoning Traces
For EVERY simulated variable, a structured narrative block:

```
### 1.1 Cardiology — Row 3: Lipid Panel — LDL
**Original Status:** ❌ Not Known
**Prediction Method:** Disease-correlated (diabetes + obesity + age)
**Distribution:** Normal(μ=125, σ=25)
**Result:** 132 mg/dL
**Confidence:** Medium
**Alternative Considered:** 98 mg/dL (rejected — no statin prescribed)
**Clinical Rationale:** Diabetic dyslipidemia typically presents with
  elevated LDL despite normal total cholesterol. Population data
  (NHANES) shows mean LDL 115-135 for untreated diabetic males 50-65.
  Selected 132 as modal value given obesity as additional risk factor.
```

### Section 4 — Combined History
Original history tables + simulated events (marked 🔮) that would have
occurred to produce the predicted current state.

---

## logs/simulation_{i}.log Format

Plain text file following the specification in `references/simulation_protocol.md`.
Minimum content:
1. Simulation input analysis (counts of ✅/📅/❌)
2. Per-variable prediction detail (department, row, original status, factors, method, distribution, value, confidence, alternatives, rationale)
3. Scenario rationale
4. Internal consistency check
5. Simulation seed

---

## logs/simulation_summary.log Format

```yaml
simulation_summary:
  profile_source: "{patient_id}_profile/"
  N_simulations: 20
  generation_date: "YYYY-MM-DD HH:MM:SS"
  total_variables_per_simulation: {count}
  
  simulations:
    - id: sim_01
      seed: "sim_01_20250621_x7k"
      scenario: "Stable, Well-Controlled"
      predicted_count: 247
      confidence_high: 89
      confidence_medium: 112
      confidence_low: 46
      
    - id: sim_02
      seed: "sim_02_20250621_m3p"
      ...
      
  aggregate_statistics:
    mean_predicted_per_sim: 247.3
    std_predicted_per_sim: 12.1
    variables_with_high_variance:  # Variables that differ most across simulations
      - "1.1 Cardiology — Lipid Panel LDL: range [98, 165]"
      - ...
    variables_with_low_variance:  # Variables that are consistent across simulations
      - "1.6 Neurology — MRI Brain: 'No acute abnormality' in all 20 sims"
      - ...
```

---

## simulation_manifest.json Format

```json
{
  "profile_source": "{patient_id}_profile/",
  "simulation_date": "2025-06-21T10:00:00",
  "N": 20,
  "model": "claude-sonnet-4-20250514",
  "simulations": [
    {
      "id": "sim_01",
      "seed": "sim_01_20250621_x7k",
      "scenario": "Stable, Well-Controlled",
      "table_dir": "simulation_tables_1/",
      "profile_html": "profile_simulation_1.html",
      "log": "logs/simulation_1.log"
    },
    ...
  ]
}
```

---

## Naming Convention

| Element | Format | Example |
|---|---|---|
| Simulation folder | `simulation_tables_{i}/` | `simulation_tables_1/` |
| Profile HTML | `profile_simulation_{i}.html` | `profile_simulation_1.html` |
| Log file | `logs/simulation_{i}.log` | `logs/simulation_1.log` |
| Seed | `sim_{i}_{YYYYMMDD}_{random3}` | `sim_01_20250621_x7k` |
| Scenario label | Short descriptive phrase | `"Stable, Well-Controlled"` |

All indices use 1-based numbering (`sim_01`, `sim_02`, ..., `sim_N`).
Zero-padded to the width of N (e.g., `sim_01` through `sim_20` for N=20;
`sim_001` through `sim_100` for N=100).
