# Sensitivity Analysis — patient_02 (N=10)

## Summary Statistics
**Mean Overall Score:** 74.8 / 100 | **Min:** 62.1 (Bile Leak, DVT, Readmission) | **Max:** 92.2 (Optimal Recovery)

## Dimension Score Distribution
| Dimension | Mean | Min | Max | Interpretation |
|---|---|---|---|---|
| D1: Clinical Outcomes | 74.7 | 60 | 95 | Most sensitive — complication type is the key driver |
| D2: Process Efficiency | 70.8 | 55 | 92 | Second most sensitive — LOS and contingency protocol gaps |
| D3: Patient Experience | 71.0 | 58 | 90 | Sensitive to unexpected complications |
| D4: Team Governance | 85.3 | 85 | 88 | **Robust** — team dynamics are outcome-independent |

## Key Sensitivity Drivers

### 1. Post-Operative Complication Type (Primary Driver)
- **Baseline delta:** Uncomplicated (92.2) → Complicated (62.1-76.7) = up to **30-point swing**
- **Mechanism:** Complication scenarios expose absence of documented post-operative contingency plans in MDT
- **Type:** Threshold effect — complication present/absent is binary, not linear
- **Clinical threshold:** Any Grade A/B post-operative complication triggers score drop due to missing contingency protocol

### 2. Missing Contingency Protocols (Secondary Driver)
- MDT plan has no documented response pathways for: bile leak, DVT, wound infection, readmission
- Each complication scenario reveals the same structural gap → 30% of simulations show major score impact
- **Recommendation:** Add "Phase 4B — Post-Operative Contingency Plan" to MDTBuilder Phase 4 deliverables

### 3. Gastroenterology Absence from MDT (Tertiary Driver)
- Bile leak (sim_04) and readmission for biloma (sim_10) both required ERCP
- Gastroenterology was absent from MDT despite cholecystectomy being a biliary procedure
- **Recommendation:** For all biliary surgery MDTs, include Gastroenterology as advisory member

### 4. DVT Prophylaxis Not Documented
- sim_05 (DVT): MDT did not include a documented DVT prophylaxis protocol
- Patient has risk factors: DM, surgical procedure
- **Recommendation:** Add DVT risk stratification (Caprini score) to MDTBuilder pre-op checklist

## Robust Variables (Low Sensitivity)
- **D4 Team Governance:** 85-88 across all scenarios — team processes are outcome-independent (correct)
- **Shared Decision-Making component:** Stable at 85-88 — pre-operative counseling was consistent
- **Surgical decision to proceed:** Vindicated in 7/10 simulations (overall score ≥70)

## Comparison Table
| Variable | Baseline (sim_01) | Worst Case (sim_04/05/10) | Score Delta | Effect Type |
|---|---|---|---|---|
| Complication present | None | Bile leak, DVT, Readmission | -30.1 | Threshold |
| LOS | POD#2 | POD#8 | -15 D2 | Linear |
| Gastro in MDT | N/A | Required for ERCP | -10 D2 | Threshold |
| DVT prophylaxis documented | Not needed | Required | -10 D2 | Threshold |
| Glucose control | Optimal | Suboptimal (sim_02) | -9.0 D1 | Linear |

## Actionable Recommendations for MDT Improvement
1. **Add post-operative complication contingency plan** to Phase 4 deliverables (impact: +15 points across 30% of simulation distribution)
2. **Include Gastroenterology** as advisory member for all biliary surgery MDTs
3. **Add DVT risk stratification** (Caprini score) to pre-operative checklist
4. **Document perioperative glucose protocol** for all T2DM patients (currently handled informally)
5. **Initiate BRCA2 genetic counseling** — outstanding action item (not simulation-dependent)

