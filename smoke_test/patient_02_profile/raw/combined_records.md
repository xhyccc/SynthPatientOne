# Combined Patient Health Records
**Generated:** 2026-06-21T09:46:08.338648
**Files Processed:** 4

---

## Document 1: cardiology_consult.txt

- **Source:** `/Users/haoyi/Desktop/working_space/SynthPatientOne/smoke_test/patient_02/cardiology_consult.txt`
- **Format:** text
- **Method:** direct_read
- **Languages:** en (English-dominant)

CARDIOLOGY CONSULT NOTE
=======================
Patient: Sarah Kim (MRN: PT-002)
DOB: 1972-08-22 (Age: 53)
Sex: Female
Consult Date: 2025-06-05

REQUESTING PHYSICIAN: Dr. Michael Torres, Internal Medicine
REASON FOR CONSULT: Pre-operative cardiac risk assessment prior to elective cholecystectomy.

HISTORY:
53-year-old female with hypertension (diagnosed 2016), type 2 diabetes mellitus
(diagnosed 2020), and symptomatic cholelithiasis scheduled for laparoscopic
cholecystectomy. Patient reports occasional palpitations but no syncope, chest
pain, or orthopnea. Functional capacity: walks 2 miles daily without limitation
(>4 METs).

CURRENT MEDICATIONS:
- Lisinopril 20mg daily
- Metformin 500mg BID
- Atorvastatin 20mg daily

PHYSICAL EXAM:
BP: 128/76 mmHg | HR: 72 bpm | RR: 16 | SpO2: 98% | BMI: 29.5 kg/m2
Cardiac: Regular rhythm, no murmurs, rubs, or gallops. No JVD.
Lungs: Clear to auscultation bilaterally.
Extremities: No edema, pulses 2+.

RECENT STUDIES:
- ECG (2025-06-05): Normal sinus rhythm, rate 72. No ST-T changes. QTc 410ms.
- Echocardiogram (2025-05-20): LVEF 62%. Normal LV wall thickness. Normal RV
  size and function. No valvular abnormalities. Estimated PA systolic pressure 28mmHg.
- Stress Test (2025-05-22): Exercise treadmill — achieved 10 METs. No chest pain.
  No ECG changes suggestive of ischemia. Duke Treadmill Score: +7 (low risk).
- Lipid Panel (2025-06-01): Total Chol 172, LDL 88, HDL 52, Triglycerides 145.
- HbA1c (2025-06-01): 6.8%

ASSESSMENT:
1. Low cardiac risk for elective surgery per RCRI (Revised Cardiac Risk Index = 0).
2. Hypertension well-controlled on ACEi.
3. Type 2 DM with improving glycemic control (HbA1c 6.8%, down from 8.1% in 2024).
4. Normal echocardiogram and stress test — no evidence of CAD or HF.

RECOMMENDATIONS:
1. Proceed with elective cholecystectomy. No further cardiac testing required.
2. Continue Lisinopril and Atorvastatin perioperatively.
3. Hold Metformin morning of surgery; resume post-operatively when eating.
4. No need for perioperative beta-blockade.

Dr. James Park, MD, FACC
Department of Cardiology


---

## Document 2: lab_results.csv

- **Source:** `/Users/haoyi/Desktop/working_space/SynthPatientOne/smoke_test/patient_02/lab_results.csv`
- **Format:** text
- **Method:** direct_read
- **Languages:** en (English-dominant)

Test,Date,Value,Unit,Reference Range,Flag
HbA1c,2025-06-17,6.8,%,<5.7,HIGH
Fasting Glucose,2025-06-17,132,mg/dL,70-100,HIGH
Total Cholesterol,2025-06-01,172,mg/dL,<200,Normal
LDL Cholesterol,2025-06-01,88,mg/dL,<100,Optimal
HDL Cholesterol,2025-06-01,52,mg/dL,>50,Optimal
Triglycerides,2025-06-01,145,mg/dL,<150,Normal
Serum Creatinine,2025-06-17,0.82,mg/dL,0.5-1.1,Normal
eGFR,2025-06-17,88,mL/min/1.73m2,>90,BORDERLINE
BUN,2025-06-17,14,mg/dL,7-20,Normal
Sodium,2025-06-17,140,mmol/L,135-145,Normal
Potassium,2025-06-17,4.2,mmol/L,3.5-5.0,Normal
Hemoglobin,2025-06-17,13.1,g/dL,12.0-15.5,Normal
WBC,2025-06-17,7.2,x10^3/uL,4.0-11.0,Normal
Platelets,2025-06-17,268,x10^3/uL,150-400,Normal
ALT,2025-06-17,42,U/L,7-56,Normal
AST,2025-06-17,35,U/L,10-40,Normal
ALP,2025-06-17,110,U/L,44-147,Normal
Total Bilirubin,2025-06-17,0.8,mg/dL,0.1-1.2,Normal
Lipase,2025-06-17,45,U/L,13-60,Normal
PT,2025-06-17,12.8,sec,11-13.5,Normal
INR,2025-06-17,1.0,,0.9-1.1,Normal
aPTT,2025-06-17,28,sec,25-35,Normal
TSH,2025-03-10,1.9,mIU/L,0.4-4.0,Normal
Vitamin D,2025-03-10,35,ng/mL,30-100,Sufficient
Calcium,2025-06-17,9.4,mg/dL,8.5-10.5,Normal
Albumin,2025-06-17,4.2,g/dL,3.5-5.0,Normal
Urine Protein,2025-06-17,12,mg/g Cr,<30,Normal


---

## Document 3: radiology_reports.txt

- **Source:** `/Users/haoyi/Desktop/working_space/SynthPatientOne/smoke_test/patient_02/radiology_reports.txt`
- **Format:** text
- **Method:** direct_read
- **Languages:** en (English-dominant)

RADIOLOGY REPORT — Abdominal Ultrasound
=========================================
Patient: Sarah Kim (MRN: PT-002)
Study Date: 2025-06-15
Modality: Right Upper Quadrant Ultrasound

INDICATION: Right upper quadrant pain, suspected cholelithiasis.

FINDINGS:
- Gallbladder: Multiple mobile echogenic foci with posterior acoustic shadowing,
  consistent with gallstones. Largest stone measures 1.2cm. Gallbladder wall
  thickness 3mm (normal <3mm). No pericholecystic fluid. Sonographic Murphy's
  sign: positive (pain with probe pressure over gallbladder).
- Common Bile Duct: 4mm caliber (normal <6mm). No intrahepatic biliary dilation.
- Liver: Normal size (14.5cm span). Diffuse increased echogenicity consistent
  with mild hepatic steatosis. No focal mass or lesion. Portal vein is patent
  with hepatopetal flow.
- Pancreas: Visualized body and tail appear normal. Head obscured by bowel gas.
- Right Kidney: 10.2cm. Normal corticomedullary differentiation. No
  hydronephrosis, stones, or mass.
- Abdominal Aorta: Visualized portions normal caliber (<3cm).

IMPRESSION:
1. Cholelithiasis with sonographic Murphy's sign, consistent with symptomatic
   gallstone disease. No evidence of acute cholecystitis.
2. Mild hepatic steatosis.
3. Otherwise normal abdominal ultrasound.

RECOMMENDATION: Surgical consultation for cholecystectomy.

Dr. Robert Chen, MD
Department of Radiology

=====

MAMMOGRAM REPORT
=================
Patient: Sarah Kim (MRN: PT-002)
Study Date: 2025-04-10
Modality: Screening Digital Mammogram with Tomosynthesis

INDICATION: Routine screening. Patient is BRCA2 positive (sister diagnosed
breast cancer at age 48).

FINDINGS:
- Bilateral CC and MLO views obtained with tomosynthesis.
- Breast composition: Heterogeneously dense (ACR Category C), which may
  obscure small masses.
- No suspicious masses, architectural distortion, or microcalcifications
  identified in either breast.
- No axillary lymphadenopathy.
- Skin and nipple are normal.

IMPRESSION:
BI-RADS Category 2 (Benign). Routine screening mammogram in 12 months
recommended. Consider supplemental screening with breast MRI given BRCA2
mutation status and dense breast tissue.

Dr. Rachel Kim, MD
Department of Radiology, Breast Imaging Section


---

## Document 4: surgical_admission.txt

- **Source:** `/Users/haoyi/Desktop/working_space/SynthPatientOne/smoke_test/patient_02/surgical_admission.txt`
- **Format:** text
- **Method:** direct_read
- **Languages:** en (English-dominant)

SURGICAL ADMISSION NOTE
========================
Patient: Sarah Kim (MRN: PT-002)
DOB: 1972-08-22 (Age: 53) | Sex: Female
Admission: 2025-06-18 | Surgery: 2025-06-18

ATTENDING SURGEON: Dr. Lisa Wong, General Surgery

PRE-OPERATIVE DIAGNOSIS: Symptomatic cholelithiasis with biliary colic.

PROCEDURE: Laparoscopic cholecystectomy.

PAST MEDICAL HISTORY:
- Hypertension (2016) — on Lisinopril 20mg
- Type 2 Diabetes Mellitus (2020) — on Metformin 500mg BID
- Hyperlipidemia — on Atorvastatin 20mg
- No prior surgeries
- Allergies: Penicillin (rash)

SOCIAL HISTORY:
- Never smoker
- Alcohol: 1-2 glasses wine/week
- Occupation: High school teacher

FAMILY HISTORY:
- Mother: DM, HTN, alive at 78
- Father: CAD, CABG at 65, alive at 80
- Sister: Breast cancer at 48 (BRCA2 positive)

PRE-OPERATIVE LABS (2025-06-17):
- WBC: 7.2 | Hb: 13.1 | Plt: 268
- Na: 140 | K: 4.2 | Cr: 0.82 | eGFR: 88
- Glucose: 132 (fasting) | HbA1c: 6.8%
- PT: 12.8s | INR: 1.0 | aPTT: 28s
- LFTs: ALT 42, AST 35, ALP 110, Total Bili 0.8
- Lipase: 45 (normal)
- Urinalysis: Normal, no protein

ABDOMINAL ULTRASOUND (2025-06-15):
- Multiple gallstones, largest 1.2cm. Gallbladder wall thickness 3mm.
- No pericholecystic fluid. Common bile duct 4mm (normal).
- Liver: Mild steatosis. No focal lesions.
- Pancreas: Normal. Kidneys: Normal size, no hydronephrosis.

SURGICAL FINDINGS:
- Laparoscopic cholecystectomy completed without complication.
- Gallbladder: distended, multiple mixed stones. No evidence of acute
  cholecystitis. No bile leak.
- Estimated blood loss: 20mL. Operative time: 45 minutes.

POST-OPERATIVE COURSE:
- Patient recovered well in PACU. Pain controlled with acetaminophen and
  PRN oxycodone (2 doses only).
- Tolerating clear liquids POD#0. Advanced to regular diet POD#1.
- Ambulating independently POD#1.
- Blood glucose monitoring: fasting 118-145, post-prandial 155-180.
  Endocrinology consulted for perioperative glucose management.

DISCHARGE PLAN (anticipated POD#2):
- Discharge to home.
- Follow-up with General Surgery in 2 weeks for wound check.
- Resume Metformin and other home medications.
- No heavy lifting for 4 weeks.

DISCHARGE MEDICATIONS:
1. Lisinopril 20mg daily
2. Metformin 500mg BID
3. Atorvastatin 20mg daily
4. Acetaminophen 650mg q6h PRN pain
5. Oxycodone 5mg q6h PRN breakthrough (limited supply)

Dr. Lisa Wong, MD, FACS
Department of General Surgery


---

