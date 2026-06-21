# Comprehensive MDT Protocol

## Phase 1: Infrastructure and Team Formation

**Goal:** Establish the foundational rules, required personnel, and technological systems for the MDT.

### Step 1.1: Define the MDT Scope
- Identify the specific pathology or patient population this MDT will handle (e.g., Gastrointestinal Oncology, Complex Trauma, Stroke).
- For the PatientProfileBuilder integration: scope is derived from the patient's key diagnoses and flagged unknowns in the profile.

### Step 1.2: Appoint Core Roles
| Role | Responsibility |
|---|---|
| **Lead Clinician (Chair)** | Facilitates the meeting, ensures equal participation, holds final clinical responsibility. |
| **MDT Coordinator** | Manages logistics, gathers patient lists, ensures data availability, records the final plan. |
| **Core Specialists** | Mandatory representatives from relevant First-Tier departments (Internal Medicine, Surgery, Radiology, Pathology, etc.). Determined by case scope. |

### Step 1.3: Establish the Technological Backbone
- Ensure all departments have shared access to a unified system capable of tracking MDT notes, viewing high-resolution imaging, and logging pathology reports.
- In this skill context: the `{patient_id}_profile/` folder serves as the shared data backbone. All status tables and history tables are the "EHR."

---

## Phase 2: Pre-Meeting Workflow (Data Collection & Logging)

**Goal:** Ensure all clinical data is gathered and preliminary assessments are documented before the team convenes.

### Step 2.1: Case Submission (T-minus 4 days)
- Any clinician can submit a complex case to the MDT Coordinator.
- Coordinator finalizes the agenda and alerts all relevant departments.
- **LLM Action:** Identify which departments have findings/unknowns in the patient profile that warrant MDT review. Create the agenda.

### Step 2.2: Independent Departmental Review (T-minus 3 to 1 days)
| Department | Review Task |
|---|---|
| **Pathology** | Finalize biopsy reports, stage cellular disease. |
| **Radiology** | Review imaging, document tumor size, anatomical abnormalities, injury extent. |
| **Clinical/Surgical** | Assess patient fitness, surgical risk, baseline organ function (Cardiology clearance, Nephrology kidney function). |
| **All other relevant** | Review status tables for their domain; note concerns, recommendations, and evidence gaps. |

### Step 2.3: Asynchronous Logging
- Every specialist logs preliminary findings using a standardized format.
- **Requirement:** Specialists must state their evidence explicitly (e.g., "Recommend against surgical intervention due to severe COPD noted by Pulmonology").
- **LLM Action:** For each relevant department, produce a `departmental_review.md` following the template.

---

## Phase 3: The MDT Meeting (Execution & Conflict Resolution)

**Goal:** Synthesize information, mediate clinical disagreements, formulate a unified patient action plan.

### Step 3.1: Case Presentation
- Referring physician presents patient history, current status, and core clinical question.
- **LLM Action:** Summarize from profile.html and status tables.

### Step 3.2: Objective Data Review
- Radiology and Pathology display visual evidence to establish undisputed facts.
- **LLM Action:** Extract all imaging and pathology findings from the profile; flag any missing critical imaging.

### Step 3.3: Collaborative Discussion & Conflict Resolution

If disciplinary conflicts arise, the Lead Clinician initiates the resolution framework:

| Step | Action |
|---|---|
| **Consult Guidelines** | Check national/international clinical pathways (NCCN, ESC, AHA, etc.). |
| **Weigh Risks** | Compare morbidity/mortality risks of each intervention. |
| **Assess Patient Capacity** | Review frailty, performance status, and overall health goals. |

### Step 3.4: Formalize the Conclusion

The team must reach consensus on one of these standard outcomes:

| Outcome | Description |
|---|---|
| **Therapeutic Intervention** | Medical or surgical — specify modality, timeline, responsible department. |
| **Further Diagnostics Required** | Specify test(s), urgency, and which department orders them. |
| **Active Surveillance / Monitoring** | Define monitoring interval, triggers for re-escalation. |
| **Referral to External Specialist** | Specify specialist type, reason, urgency. |
| **Palliative / Supportive Care** | Define care plan, symptom management goals. |

---

## Phase 4: Post-Meeting Action and Follow-Up

**Goal:** Communicate the plan and execute clinical interventions.

### Step 4.1: Documentation
- MDT Coordinator finalizes the "MDT Consensus Report" within 24 hours.
- **LLM Action:** Produce `mdt/consensus_report.html`.

### Step 4.2: Patient Communication
- Lead Clinician meets with patient/family to explain recommendations, discuss risks, obtain informed consent.
- **LLM Action:** Generate a patient-facing summary in plain language.

### Step 4.3: Order Execution
- Responsible department assumes primary care and places necessary orders.
- **LLM Action:** List specific orders per department.

### Step 4.4: Outcome Tracking
- Schedule follow-up date for case review at future MDT meeting.
- **LLM Action:** Set recommended follow-up timeline with triggers for re-evaluation.

---

## Phase 5: Continuous Improvement

**Goal:** Monitor MDT process effectiveness.

### Step 5.1: Quarterly Audit
- Review attendance records, case discussion timeframes, audit random sample of cases.
- **LLM Action:** Produce an MDT process quality self-audit checklist based on this session.

---

## Conflict Resolution Framework

When two departments disagree on the treatment path:

```
1. IDENTIFY: What is the exact point of disagreement?
2. EVIDENCE: What does each department cite?
   - Dept A: [evidence] (source: status table X, guideline Y)
   - Dept B: [evidence] (source: status table Z, guideline W)
3. RISK COMPARISON:
   - Option A risks: [list]
   - Option B risks: [list]
4. PATIENT FACTORS: ECOG status, comorbidities, patient preference, age
5. GUIDELINE REFERENCE: [NCCN/ESC/AHA/etc. recommendation]
6. CHAIR DECISION: [recommendation with rationale]
```

---

## MDT Quality Indicators

| Metric | Target |
|---|---|
| Cases discussed with complete pre-meeting data | ≥ 95% |
| Consensus reached without deferral | ≥ 90% |
| MDT recommendation implemented within 30 days | ≥ 85% |
| Patient informed of MDT outcome within 7 days | 100% |
| Documentation completed within 24 hours | 100% |
