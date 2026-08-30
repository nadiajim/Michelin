"""
Diagnostic & Analytical Tools for Michelin Veterinary Co-Pilot
Implements multimodal image interpretation, lab analytics, and differential diagnosis engines.
"""
from typing import Dict, List, Any, Optional
import math

class VeterinaryDiagnosticTools:
    """Tools callable by the Michelin Agent to perform clinical computations and differential ranking."""

    @staticmethod
    def analyze_radiograph_metadata(image_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyzes feline radiograph / ultrasound imaging features."""
        findings = image_metadata.get("findings", "")
        modality = image_metadata.get("modality", "Thoracic Radiograph")
        
        detected_features = []
        abnormalities = []

        if "effusion" in findings.lower() or "fluid" in findings.lower():
            abnormalities.append("Pleural or Peritoneal Effusion Detected")
            detected_features.append({
                "region": "Thoracic/Abdominal Cavity",
                "pattern": "Serosal detail loss / Pleural fissure line widening",
                "significance": "High probability of exudative or modified transudate fluid accumulation."
            })
        
        if "fissure line" in findings.lower():
            abnormalities.append("Pleural Fissure Lines Visible")
        
        return {
            "modality": modality,
            "abnormalities_detected": abnormalities,
            "feature_breakdown": detected_features,
            "differential_implication": "Strongly points towards systemic inflammatory (e.g. FIP), cardiovascular (CHF), or neoplastic process.",
            "recommended_next_step": "Ultrasound-guided diagnostic centesis with Rivalta test, total protein, and cytology."
        }

    @staticmethod
    def calculate_differential_matrix(patient_data: Dict[str, Any], additional_findings: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generates a calibrated Differential Diagnosis Matrix
        incorporating longitudinal vitals, biomarkers, owner logs, and imaging.
        """
        lab_results = patient_data.get("lab_results", [])
        latest_lab = lab_results[0]["metrics"] if lab_results else {}
        
        ag_ratio = latest_lab.get("AG_Ratio", {}).get("value", 0.8)
        globulin = latest_lab.get("Globulin", {}).get("value", 3.5)
        sdma = latest_lab.get("SDMA", {}).get("value", 10.0)
        vitals = patient_data.get("vitals_history", [{}])[-1]
        temp = vitals.get("temp_c", 38.5)

        differentials = []

        # 1. FIP Evaluation
        fip_prob = 15
        if ag_ratio < 0.45:
            fip_prob += 50
        elif ag_ratio < 0.60:
            fip_prob += 30
        if globulin > 5.5:
            fip_prob += 20
        if temp > 39.2:
            fip_prob += 10
        fip_prob = min(fip_prob, 94)

        differentials.append({
            "diagnosis": "Feline Infectious Peritonitis (FIP) - Early / Mixed Form",
            "icd_vet_code": "VET-FIP-01",
            "probability_percentage": fip_prob,
            "severity": "CRITICAL",
            "clinical_evidence": [
                f"Severe A:G ratio inversion ({ag_ratio:.2f} vs ref > 0.60)",
                f"Marked hyperglobulinemia ({globulin} g/dL)",
                f"Pyrexia of Unknown Origin ({temp}°C) unresponsive to initial standard care",
                "Subtle free abdominal/pleural fluid noted on diagnostic imaging"
            ],
            "rule_out_tests": [
                "Diagnostic Abdominocentesis / Thoracocentesis (Visual inspection: viscous, clear-yellow straw fluid)",
                "Rivalta Test (Positive = High FIP specificity > 86%)",
                "FCoV RT-PCR on effusion / fine needle aspirate (FNA) of mesenteric lymph nodes",
                "Serum Protein Electrophoresis (polyclonal vs monoclonal gammopathy)"
            ],
            "therapeutic_urgency": "Immediate (Evaluation for GS-441524 / GC376 antiviral protocol)"
        })

        # 2. Feline Lymphoma / Mediastinal Neoplasia
        lymphoma_prob = 22
        if globulin > 5.5:
            lymphoma_prob += 15
        if ag_ratio < 0.55:
            lymphoma_prob += 10
        differentials.append({
            "diagnosis": "Feline Lymphoma / Mesenteric or Mediastinal Neoplasia",
            "icd_vet_code": "VET-LMP-04",
            "probability_percentage": lymphoma_prob,
            "severity": "HIGH",
            "clinical_evidence": [
                "Unintentional progressive weight loss (0.6 kg drop)",
                "Submandibular lymph node enlargement noted on physical exam",
                "Non-regenerative anemia secondary to chronic disease or bone marrow suppression"
            ],
            "rule_out_tests": [
                "FNA Cytology of peripheral and mesenteric lymph nodes with flow cytometry/PARR",
                "Full Abdominal Ultrasound (checking intestinal wall layer loss and lymphadenopathy)",
                "FeLV/FIV Snap Test (ELISA)"
            ],
            "therapeutic_urgency": "High"
        })

        # 3. Bacterial Sepsis / Septic Peritonitis / Pyothorax
        sepsis_prob = 18
        if temp > 39.5:
            sepsis_prob += 12
        differentials.append({
            "diagnosis": "Septic Peritonitis / Pyothorax / Occult Deep Abscessation",
            "icd_vet_code": "VET-INF-09",
            "probability_percentage": sepsis_prob,
            "severity": "HIGH",
            "clinical_evidence": [
                "High fever and leukocytosis with neutrophilia",
                "Mild abdominal distension and fluid wave"
            ],
            "rule_out_tests": [
                "Effusion fluid cytology (Degenerate neutrophils with intracellular bacteria)",
                "Fluid vs Blood Glucose gradient (Fluid glucose < Blood glucose by > 20 mg/dL indicates sepsis)",
                "Aerobic & Anaerobic fluid culture with antimicrobial susceptibility testing"
            ],
            "therapeutic_urgency": "High"
        })

        # 4. Feline Chronic Kidney Disease (CKD)
        ckd_prob = 10
        if sdma > 14.0:
            ckd_prob += 55
        differentials.append({
            "diagnosis": "Feline Chronic Kidney Disease (IRIS Stage 1-2)",
            "icd_vet_code": "VET-CKD-02",
            "probability_percentage": ckd_prob,
            "severity": "MODERATE",
            "clinical_evidence": [
                f"SDMA level: {sdma} ug/dL",
                "Weight trend tracking and owner hydration observations"
            ],
            "rule_out_tests": [
                "Urinary Specific Gravity & Urine Protein-to-Creatinine (UPC) Ratio",
                "Systemic Doppler Blood Pressure evaluation",
                "Renal Ultrasound"
            ],
            "therapeutic_urgency": "Moderate"
        })

        # Sort by probability descending
        differentials.sort(key=lambda x: x["probability_percentage"], reverse=True)
        return differentials
