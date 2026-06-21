# Combined Patient Health Records
**Generated:** 2026-06-21T09:15:21.785043
**Files Processed:** 3

---

## Document 1: discharge_summary.txt

- **Source:** `/Users/haoyi/Desktop/working_space/SynthPatientOne/patient_smoke_test/discharge_summary.txt`
- **Format:** text
- **Method:** direct_read
- **Languages:** en (English-dominant)

DISCHARGE SUMMARY
==================
Patient: John Doe (MRN: PT-001)
DOB: 1967-03-15 (Age: 58)
Sex: Male
Admission Date: 2025-06-10
Discharge Date: 2025-06-15

ATTENDING PHYSICIAN: Dr. Sarah Chen, Internal Medicine

CHIEF COMPLAINT:
 chest pain and shortness of breath for 3 days.

HISTORY OF PRESENT ILLNESS:
58-year-old male with history of hypertension, type 2 diabetes mellitus,
and COPD (GOLD Stage 2) presents with progressive dyspnea on exertion
and intermittent substernal chest pressure over 3 days. Patient reports
the chest discomfort is "like a weight", non-radiating, 4/10 intensity,
worse with activity and partially relieved by rest. Denies palpitations,
syncope, nausea, or diaphoresis.

PAST MEDICAL HISTORY:
- Hypertension, diagnosed 2015, on Lisinopril 10mg daily
- Type 2 Diabetes Mellitus, diagnosed 2018, on Metformin 1000mg BID
- COPD, diagnosed 2020, GOLD Stage 2, on Tiotropium 18mcg daily
- No prior myocardial infarction, stroke, or TIA
- No known drug allergies

SOCIAL HISTORY:
- Smoking: 35 pack-years, current smoker (1 pack/day)
- Alcohol: 2-3 drinks/week
- Occupation: Construction worker (reduced hours due to dyspnea)

FAMILY HISTORY:
- Father: MI at age 52, deceased at 68 (heart failure)
- Mother: Alive at 82, hypertension, osteoporosis
- Brother: Type 2 diabetes, diagnosed at 50

PHYSICAL EXAMINATION:
- BP: 142/88 mmHg | HR: 82 bpm | RR: 18/min | Temp: 36.8°C | SpO2: 94% on room air
- BMI: 31.2 kg/m2
- HEENT: Normal
- Neck: No JVD, no carotid bruits
- Chest: Decreased breath sounds bilaterally, prolonged expiratory phase, no wheezes
- Cardiac: Regular rhythm, no murmurs, rubs, or gallops
- Abdomen: Soft, non-tender, no organomegaly
- Extremities: No edema, pulses 2+ bilaterally

HOSPITAL COURSE:
Patient was admitted for rule-out ACS. Serial troponins were negative
(Troponin I <0.01 ng/mL at 0h, 3h, 6h). ECG showed normal sinus rhythm
with no ischemic changes. Chest X-ray showed hyperinflated lungs consistent
with COPD, no acute infiltrates or effusions. The working diagnosis is
COPD exacerbation with atypical chest discomfort, likely musculoskeletal
or related to increased work of breathing. ACS ruled out.

Patient was started on prednisone 40mg daily x 5 days and azithromycin
250mg daily x 5 days for COPD exacerbation. Respiratory status improved.
The hypertension and diabetes were noted to be suboptimally controlled
during admission. Cardiology consult was not obtained due to low pretest
probability after negative troponins and normal ECG.

DISCHARGE MEDICATIONS:
1. Lisinopril 10mg daily
2. Metformin 1000mg BID
3. Tiotropium 18mcg daily via HandiHaler
4. Albuterol 90mcg 2 puffs q4-6h PRN

DISCHARGE PLAN:
- Follow up with PCP in 1 week
- Pulmonology referral for COPD management optimization
- Smoking cessation counseling recommended
- Not candidate for cardiac catheterization at this time

Dictated by: Dr. Sarah Chen, MD
Date: 2025-06-15


---

## Document 2: lab_results.csv

- **Source:** `/Users/haoyi/Desktop/working_space/SynthPatientOne/patient_smoke_test/lab_results.csv`
- **Format:** text
- **Method:** direct_read
- **Languages:** en (English-dominant)

Test,Date,Value,Unit,Reference Range,Flag
HbA1c,2025-06-11,7.8,%,<5.7,HIGH
Fasting Glucose,2025-06-11,156,mg/dL,70-100,HIGH
Total Cholesterol,2024-03-20,198,mg/dL,<200,Normal
LDL Cholesterol,2024-03-20,112,mg/dL,<100,BORDERLINE
HDL Cholesterol,2024-03-20,38,mg/dL,>40,LOW
Triglycerides,2024-03-20,240,mg/dL,<150,HIGH
Serum Creatinine,2025-06-11,1.05,mg/dL,0.6-1.2,Normal
eGFR,2025-06-11,82,mL/min/1.73m2,>90,BORDERLINE LOW
BUN,2025-06-11,18,mg/dL,7-20,Normal
Sodium,2025-06-11,139,mmol/L,135-145,Normal
Potassium,2025-06-11,4.1,mmol/L,3.5-5.0,Normal
TSH,2024-01-15,2.8,mIU/L,0.4-4.0,Normal
Hemoglobin,2025-06-11,14.2,g/dL,13.5-17.5,Normal
WBC,2025-06-11,8.9,x10^3/uL,4.0-11.0,Normal
Platelets,2025-06-11,245,x10^3/uL,150-400,Normal
Troponin I (0h),2025-06-11,<0.01,ng/mL,<0.04,Normal
Troponin I (3h),2025-06-11,<0.01,ng/mL,<0.04,Normal
Troponin I (6h),2025-06-11,<0.01,ng/mL,<0.04,Normal


---

## Document 3: referral_letter.txt

- **Source:** `/Users/haoyi/Desktop/working_space/SynthPatientOne/patient_smoke_test/referral_letter.txt`
- **Format:** text
- **Method:** direct_read
- **Languages:** en (English-dominant)

PULMONOLOGY REFERRAL LETTER
============================
Date: 2025-06-15

To: Pulmonology Department
From: Dr. Sarah Chen, Internal Medicine

RE: John Doe (MRN: PT-001, DOB: 1967-03-15)

Dear Colleague,

I am referring this 58-year-old male patient for COPD management optimization.

The patient was recently admitted (2025-06-10 to 2025-06-15) with a COPD
exacerbation presenting as progressive dyspnea and atypical chest discomfort.
ACS was ruled out with serial negative troponins and normal ECG.

Key findings:
- SpO2: 94% on room air at discharge (nadir 91% on admission)
- Chest X-ray: Hyperinflated lungs, no infiltrates
- Smoking: 35 pack-years, CURRENT SMOKER (1 pack/day)
- BMI: 31.2 (obese)

Current COPD medications:
- Tiotropium 18mcg daily
- Albuterol 90mcg PRN

Pulmonary Function Tests have NOT been performed in the past 3 years.
I recommend formal PFTs to reassess the GOLD stage and consider whether
ICS/LABA therapy would be beneficial.

The patient also has poorly controlled Type 2 DM (HbA1c 7.8%) and
Stage 1 Hypertension. These should be considered in any interventional
planning.

Thank you for your assessment.

Sincerely,
Dr. Sarah Chen, MD
Department of Internal Medicine


---

