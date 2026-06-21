# MDT Evaluation Framework

## Four Core Dimensions

The MDT is evaluated across four dimensions. Each dimension contains specific metrics
with defined scoring rubrics. Every metric is assessed against each of the N simulated
patient profiles, producing N independent evaluation results that are then aggregated.

---

## Dimension 1: Clinical Outcomes &amp; Efficacy

### 1.1 Diagnostic Concordance
**Question:** Would the MDT's diagnosis hold if the patient had the simulated (completed) profile?

**Scoring (per simulation):**
| Score | Criterion |
|---|---|
| 3 — Full Concordance | MDT's primary diagnosis matches the simulated pathology. All differential diagnoses correctly ruled in/out. |
| 2 — Partial Concordance | Primary diagnosis matches, but ≥1 differential missed or over-called. |
| 1 — Weak Concordance | Primary diagnosis partially matches but key elements differ. |
| 0 — Discordant | MDT diagnosis is inconsistent with simulated findings. MDT would have pursued wrong treatment path. |

### 1.2 Treatment Appropriateness
**Question:** Given the simulated patient's complete profile, was the MDT's recommended treatment optimal?

**Scoring (per simulation):**
| Score | Criterion |
|---|---|
| 3 — Optimal | Recommended treatment is the guideline-preferred intervention for the simulated profile. No contraindications violated. |
| 2 — Acceptable | Treatment is reasonable but a clearly superior alternative exists given simulated values. |
| 1 — Suboptimal | Treatment has significant risks not identified by MDT due to missing data they didn't have. |
| 0 — Contraindicated | Recommended treatment would be harmful given simulated values (e.g., surgery recommended but simulated profile shows severe coagulopathy). |

### 1.3 Guideline Concordance
**Question:** Does the MDT's treatment plan align with established clinical guidelines (NCCN, ESC, AHA, ASCO, etc.)?

**Scoring (per simulation):**
| Score | Criterion |
|---|---|
| 3 — Full Adherence | Protocol exactly follows guideline recommendations for the clinical scenario. |
| 2 — Justified Deviation | Deviation from guideline, but MDT documented explicit clinical rationale. |
| 1 — Unjustified Deviation | Deviation without adequate documentation. |
| 0 — Guideline-Contradictory | MDT plan directly contradicts guideline without any rationale. |

### 1.4 Morbidity/Mortality Risk Assessment
**Question:** Did the MDT accurately assess the procedural and long-term risks?

**Scoring (per simulation):**
| Score | Criterion |
|---|---|
| 3 — Complete | All major risks identified and discussed. Risk mitigation strategies documented. |
| 2 — Adequate | Key risks identified but some minor risks missed. |
| 1 — Incomplete | Significant risks missed that could change the risk-benefit calculus. |
| 0 — Absent | No documented risk assessment. |

### 1.5 Diagnostic Completeness
**Question:** Did the MDT identify what further diagnostics were needed BEFORE treatment?

**Scoring (per simulation):**
| Score | Criterion |
|---|---|
| 3 — Complete | MDT correctly identified all missing critical diagnostics. |
| 2 — Mostly Complete | Identified most, missed 1-2 non-critical tests. |
| 1 — Incomplete | Missed ≥1 critical diagnostic that the simulated profile shows as abnormal. |
| 0 — Wrong Tests | MDT ordered unnecessary tests or omitted essential ones. |

### 1.6 Missing Diagnosis Detection
**Question:** Did the MDT identify and act on clinically significant diagnoses that were not formally recorded in the original profile, but which the simulated completion reveals as present?

**Scoring (per simulation):**
| Score | Criterion |
|---|---|
| 3 — Identified & Addressed | MDT flagged the condition as a probable or possible diagnosis and included confirmatory workup in the plan. |
| 2 — Identified, Not Actioned | MDT noted a differential but did not incorporate confirmatory steps into the plan. |
| 1 — Partial | MDT recognised general diagnostic uncertainty but did not name the specific missing diagnosis. |
| 0 — Missed | The simulated profile confirms the diagnosis; MDT did not raise it. Clinical trajectory would be adversely affected. |
| N/A | No potential missing diagnoses flagged in the profile. |

### 1.7 Disease Trajectory Planning
**Question:** Did the MDT's plan adequately account for the expected progression of the patient's active conditions, and were appropriate monitoring and escalation triggers specified?

**Scoring (per simulation):**
| Score | Criterion |
|---|---|
| 3 — Comprehensive | Plan includes specific monitoring parameters, target intervals, and escalation thresholds consistent with the simulated trajectory. |
| 2 — Adequate | Core trajectory addressed with follow-up scheduled, but monitoring thresholds not fully specified. |
| 1 — Superficial | Follow-up noted but no structured monitoring or escalation criteria. |
| 0 — Absent | Plan makes no provision for disease progression; the simulated trajectory indicates the patient would deteriorate without the escalation pathway. |

### 1.8 Diagnostic Reliability Verification
**Question:** Did the MDT recognise and address tests or diagnoses in the profile that carry a material risk of error or misclassification, before making major clinical decisions that depend on those results?

**Scoring (per simulation):**
| Score | Criterion |
|---|---|
| 3 — Fully Addressed | MDT explicitly flagged unreliable test results, deferred dependent decisions, and specified confirmatory steps with owners and timelines. |
| 2 — Partly Addressed | MDT flagged the uncertainty but did not fully defer or plan confirmation. |
| 1 — Incidentally Noted | Uncertainty mentioned in discussion but not reflected in the decision or action plan. |
| 0 — Not Recognised | MDT made major clinical decisions directly from a flagged unreliable result; the simulated profile shows a different ground truth. |
| N/A | No diagnostic reliability flags raised in the profile. |

---

## Dimension 2: Process &amp; Operational Efficiency

### 2.1 Time-to-Treatment
**Question:** Would the MDT's recommended timeline be appropriate given the simulated patient's disease severity?

**Scoring (per simulation):**
| Score | Criterion |
|---|---|
| 3 — Optimal | Timeline matches urgency. Emergency → immediate; elective → reasonable window. |
| 2 — Acceptable | Slight delay but within clinically safe window. |
| 1 — Delayed | Unnecessary delay that could allow disease progression. |
| 0 — Dangerous | Critical delay that would lead to preventable deterioration. |

### 2.2 Implementation Feasibility
**Question:** Can the MDT's plan actually be executed given the simulated patient's complete profile?

**Scoring (per simulation):**
| Score | Criterion |
|---|---|
| 3 — Fully Feasible | All orders can be placed immediately. No barriers. |
| 2 — Minor Barriers | Requires 1-2 additional clearances (e.g., cardiology clearance) that are likely to pass. |
| 1 — Significant Barriers | Major obstacle (e.g., requires unavailable specialist, contraindicated drug). |
| 0 — Infeasible | Plan cannot be executed as written (e.g., surgical candidate but no surgeon available, or patient factors make it impossible). |

### 2.3 Case Preparation Quality
**Question:** Was the data presented to the MDT complete enough to make informed decisions?

**Scoring (per simulation):**
| Score | Criterion |
|---|---|
| 3 — Complete | All relevant imaging, pathology, and labs available. No missing data hindered discussion. |
| 2 — Minor Gaps | Missing non-critical data; didn't affect core decision. |
| 1 — Significant Gaps | Missing data that the simulated profile shows as critical (e.g., no echo before cardiac surgery decision). |
| 0 — Inadequate | Core decision was made on incomplete data that would have changed the outcome. |

---

## Dimension 3: Patient Experience &amp; Quality of Life

### 3.1 Patient-Reported Outcome Measures (PROMs) — Projected
**Question:** Based on the simulated profile and the MDT's recommended intervention, what is the projected quality of life outcome?

**Scoring (per simulation):**
| Score | Criterion |
|---|---|
| 3 — Significant Improvement | Intervention likely to substantially improve functional status, pain, or QoL. |
| 2 — Moderate Improvement | Some improvement expected. |
| 1 — Minimal Change | Intervention unlikely to meaningfully change QoL. |
| 0 — Harmful | Intervention likely to worsen QoL (excessive morbidity, loss of function). |

### 3.2 Shared Decision-Making
**Question:** Did the MDT document patient communication and consent?

**Scoring (per simulation):**
| Score | Criterion |
|---|---|
| 3 — Fully Documented | Patient summary exists, risks explained, options discussed, consent pathway clear. |
| 2 — Partially Documented | Summary exists but lacks detail on alternatives or risks. |
| 1 — Minimal | Only a brief mention of patient communication. |
| 0 — Absent | No evidence of patient communication or consent planning. |

### 3.3 Psychosocial Support
**Question:** For severe diagnoses, did the MDT include psychosocial/supportive care referrals?

**Scoring (per simulation):**
| Score | Criterion |
|---|---|
| 3 — Comprehensive | Mental health, social work, palliative care, and rehabilitation services addressed as needed. |
| 2 — Adequate | Key psychosocial needs identified and referred. |
| 1 — Minimal | Token mention without specific referrals. |
| 0 — Absent | No psychosocial assessment despite clear need in the simulated profile. |

---

## Dimension 4: Team Dynamics &amp; Governance

### 4.1 Quorum and Representation
**Question:** Were all necessary specialties represented in the MDT?

**Scoring (per simulation):**
| Score | Criterion |
|---|---|
| 3 — Full Quorum | All relevant First-Tier departments represented. Radiology and Pathology present if imaging/biopsies exist. |
| 2 — Minor Absences | One non-critical department missing. |
| 1 — Significant Absences | Key specialty missing whose input could change the decision. |
| 0 — No Quorum | Core decision-making departments absent. |

### 4.2 Documentation Quality
**Question:** Are the MDT minutes and consensus report clear, legally sound, and actionable?

**Scoring (per simulation):**
| Score | Criterion |
|---|---|
| 3 — Excellent | Minutes are structured, every recommendation has rationale and evidence citation. Consensus report is comprehensive. |
| 2 — Adequate | Clear decisions but some rationale missing. |
| 1 — Poor | Decisions recorded but lacking supporting evidence or rationale. |
| 0 — Inadequate | Minutes are unclear, contradictory, or missing key decisions. |

### 4.3 Conflict Resolution Quality
**Question:** If departmental conflicts existed, were they resolved transparently and fairly?

**Scoring (per simulation):**
| Score | Criterion |
|---|---|
| 3 — Exemplary | Conflicts identified, framework applied, rationale documented, dissents recorded. |
| 2 — Adequate | Conflicts resolved but documentation could be stronger. |
| 1 — Superficial | Conflicts noted but resolution lacks depth or evidence. |
| 0 — Unresolved | Conflicts evident but no resolution documented, or one department's view suppressed without justification. |
| N/A | No conflicts identified. |

---

## Aggregate Scoring

Each dimension produces a score from 0-3 per metric (or N/A where applicable).
The overall MDT Quality Score is calculated as:

```
Dimension Score = mean of all metric scores in that dimension (excluding N/A)
Overall Score   = mean of all dimension scores
```

### Score Interpretation

| Overall Score | Rating |
|---|---|
| ≥ 2.7 | Excellent — MDT process is robust across all dimensions |
| 2.3 – 2.69 | Good — Minor improvements needed in specific areas |
| 1.8 – 2.29 | Adequate — Systematic improvements recommended |
| 1.2 – 1.79 | Marginal — Significant process re-engineering required |
| < 1.2 | Poor — MDT process is failing; urgent intervention needed |

---

## Cross-Simulation Analysis

After evaluating all N simulations, metrics that show HIGH VARIANCE across simulations
indicate that the MDT's performance is sensitive to the specific clinical scenario.
Metrics with LOW VARIANCE indicate consistent strengths or weaknesses.

This analysis feeds the **Sensitivity Report** — identifying which MDT decisions are
robust across diverse patient presentations and which are fragile.
