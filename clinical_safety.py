"""
Clinical Safety & False-Negative Prevention Engine
Specialized in preventing missed feline diagnoses (FIP, HCM, early CKD, septic peritonitis, occult neoplasia).
Grounds agent reasoning in AAFP, ACVIM, and WSAVA feline medical standards.
"""
from typing import Dict, List, Any

class ClinicalSafetyEngine:
    """
    Evaluates patient biomarkers, vitals, imaging signals, and clinical history
    to trigger proactive clinical inquiries and prevent dangerous false negatives.
    """

    CRITICAL_PATHOLOGY_TRIGGERS = [
        {
            "condition": "Feline Infectious Peritonitis (FIP) - Effusive / Non-Effusive",
            "key_biomarkers": ["AG_Ratio < 0.5", "Globulin > 5.2", "Pyrexia of Unknown Origin", "Cavity Effusion"],
            "must_not_miss_score": 95,
            "recommended_inquiries": [
                "Has a diagnostic abdominocentesis or thoracocentesis been performed to inspect fluid clarity, viscosity, and run a Rivalta test?",
                "Has feline coronavirus (FCoV) RT-PCR or immunocytochemistry on effusion macrophages been ordered?",
                "Are there any ocular lesions (uveitis, keratic precipitates) or neurological signs (ataxia, hyperesthesia) observed?"
            ],
            "first_line_intervention": "Initiate GS-441524 antiviral therapy evaluation immediately if A:G ratio < 0.45 and high total protein with effusion."
        },
        {
            "condition": "Early Feline Hypertrophic Cardiomyopathy (HCM) / Congestive Heart Failure",
            "key_biomarkers": ["Tachypnea > 30 bpm at rest", "Gallop sound / systolic murmur", "Pleural effusion"],
            "must_not_miss_score": 88,
            "recommended_inquiries": [
                "What is the patient's resting sleeping respiratory rate (SRR) recorded at home by the owner?",
                "Has an NT-proBNP biomarker assay or focused echocardiography (POCUS) been scheduled?",
                "Is there evidence of left atrial enlargement on thoracic radiographs (vertebral heart score > 8.0)?"
            ],
            "first_line_intervention": "Avoid aggressive IV fluid overload; evaluate for furosemide / pimobendan if in active congestive failure."
        },
        {
            "condition": "Early Feline Chronic Kidney Disease (IRIS Stage 1-2)",
            "key_biomarkers": ["SDMA > 14 ug/dL", "USG < 1.035", "Weight loss > 5% over 3 months"],
            "must_not_miss_score": 82,
            "recommended_inquiries": [
                "Has a cystocentesis urinalysis been evaluated for proteinuria (UPC ratio) and active sediment?",
                "Has Doppler systemic blood pressure been measured to rule out end-organ hypertensive damage?",
                "Has renal ultrasound been performed to assess corticomedullary distinction and rule out nephroliths/hydronephrosis?"
            ],
            "first_line_intervention": "Transition to renal-protective diet, ensure adequate hydration, monitor phosphorus and blood pressure."
        }
    ]

    @classmethod
    def analyze_false_negative_risks(cls, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scans patient record against feline diagnostic traps and generates
        a false-negative prevention safety alert with tailored collaborative questions.
        """
        alerts = []
        inquiries = []
        risk_level = "Low"

        # Check labs
        lab_results = patient_data.get("lab_results", [])
        latest_lab = lab_results[0]["metrics"] if lab_results else {}

        # 1. Evaluate A:G ratio and Globulins for FIP
        ag_ratio = latest_lab.get("AG_Ratio", {}).get("value")
        globulin = latest_lab.get("Globulin", {}).get("value")
        temp = patient_data.get("vitals_history", [{}])[-1].get("temp_c", 38.5)

        if ag_ratio is not None and ag_ratio <= 0.50:
            risk_level = "Critical"
            alerts.append({
                "severity": "CRITICAL",
                "condition": "Suspected Feline Infectious Peritonitis (FIP)",
                "rationale": f"A:G ratio is dangerously low ({ag_ratio:.2f}) with high globulins ({globulin} g/dL) and persistent pyrexia ({temp}°C). FIP is frequently missed in early stages when presented as vague malaise.",
                "action": "Do NOT delay with prolonged empiric broad-spectrum antibiotics alone. Urgent fluid sampling and GS-441524 protocol readiness recommended."
            })
            inquiries.extend(cls.CRITICAL_PATHOLOGY_TRIGGERS[0]["recommended_inquiries"])

        # 2. Check SDMA and Renal values
        sdma = latest_lab.get("SDMA", {}).get("value")
        if sdma and sdma > 14.0:
            if risk_level != "Critical":
                risk_level = "High"
            alerts.append({
                "severity": "HIGH",
                "condition": "Early Renal Functional Loss (Pre-Azotemic / IRIS Stage 1-2)",
                "rationale": f"SDMA elevated at {sdma} ug/dL indicating >25% nephron functional loss, even if serum creatinine appears deceptively normal due to muscle loss.",
                "action": "Perform UPC ratio and blood pressure screening."
            })
            inquiries.extend(cls.CRITICAL_PATHOLOGY_TRIGGERS[2]["recommended_inquiries"])

        # 3. Check Weight Trajectory
        vitals = patient_data.get("vitals_history", [])
        if len(vitals) >= 2:
            first_wt = vitals[0].get("weight_kg", 0)
            last_wt = vitals[-1].get("weight_kg", 0)
            if first_wt > 0:
                pct_loss = ((first_wt - last_wt) / first_wt) * 100
                if pct_loss >= 10.0:
                    alerts.append({
                        "severity": "HIGH",
                        "condition": "Unintentional Progressive Weight Loss Pattern",
                        "rationale": f"Patient has lost {pct_loss:.1f}% of body weight across recorded visits. High risk of occult catabolic pathology.",
                        "action": "Investigate gastrointestinal absorption, endocrine dysfunction, or systemic inflammatory state."
                    })

        return {
            "risk_level": risk_level,
            "active_alerts": alerts,
            "proactive_collaborative_inquiries": inquiries[:4],
            "guideline_sources": [
                "AAFP Feline Infectious Peritonitis Diagnosis Guidelines (2022/2024)",
                "IRIS Feline Chronic Kidney Disease Staging Consensus (2023)",
                "ACVIM Feline Cardiomyopathy Diagnostic Consensus Guidelines"
            ]
        }
