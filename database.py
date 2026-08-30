"""
Database & Longitudinal Patient Record Vault
Simulates a Google Cloud Firestore / Cloud Storage backend with rich feline clinical cases.
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import copy

PATIENTS_STORE: Dict[str, Dict[str, Any]] = {
    "pat_michelin_001": {
        "id": "pat_michelin_001",
        "name": "Michelin",
        "species": "Feline",
        "breed": "Domestic Shorthair",
        "age_years": 4.2,
        "sex": "Male Neutered",
        "weight_kg": 3.8,
        "owner_name": "Nadia Jiménez",
        "primary_clinic": "Clínica Veterinaria Aguascalientes",
        "microchip": "985141002948172",
        "created_at": "2026-06-15T09:30:00Z",
        "status": "Under Active Collaborative Investigation",
        "critical_flags": [
            "Hyperglobulinemia with A:G Ratio < 0.5",
            "Fluctuating Low-Grade Fever Unresponsive to Initial Antibiotics",
            "High False-Negative Risk for FIP / Early Effusive Pathology"
        ],
        "vitals_history": [
            {"date": "2026-07-10", "weight_kg": 4.4, "temp_c": 38.6, "heart_rate": 180, "resp_rate": 26},
            {"date": "2026-08-01", "weight_kg": 4.1, "temp_c": 39.4, "heart_rate": 195, "resp_rate": 32},
            {"date": "2026-08-28", "weight_kg": 3.8, "temp_c": 39.7, "heart_rate": 205, "resp_rate": 38}
        ],
        "owner_observations": [
            {
                "timestamp": "2026-08-26T18:20:00Z",
                "reporter": "Owner (Nadia)",
                "note": "Michelin seems much quieter over the past two weeks. He used to jump onto the high cat tree easily, but now he hesitates and rests on the bottom tier. His appetite is down ~40% and his breathing looks slightly more abdominal when resting.",
                "severity": "High"
            },
            {
                "timestamp": "2026-08-29T08:15:00Z",
                "reporter": "Owner (Nadia)",
                "note": "Gave morning wet food; Michelin only licked the gravy. His ears felt warm. Slight swelling noticed in abdomen.",
                "severity": "Urgent"
            }
        ],
        "clinical_notes": [
            {
                "visit_id": "vis_20260828",
                "date": "2026-08-28",
                "vet_name": "Dr. Carlos Mendez, MVZ",
                "subjective": "Michelin presented for lethargy, hyporexia, and progressive weight loss (0.6 kg drop in 7 weeks).",
                "objective": "T: 39.7°C, HR: 205 bpm, RR: 38 bpm. Submandibular lymph nodes mildly enlarged. Mucous membranes mildly pale, CRT 2s. Abdomen mildly distended with subtle fluid wave on palpation. Thoracic auscultation: slightly muffled ventral lung sounds.",
                "assessment": "Pyrexia of unknown origin with progressive weight loss and possible early cavitary effusion.",
                "plan": "Complete CBC, serum biochemistry panel with electrophoresis, two-view thoracic & abdominal radiographs, abdominal ultrasound."
            }
        ],
        "lab_results": [
            {
                "lab_id": "lab_cbc_20260828",
                "date": "2026-08-28",
                "panel_type": "CBC & Serum Chemistry",
                "metrics": {
                    "RBC": {"value": 5.1, "unit": "M/uL", "ref_min": 6.5, "ref_max": 10.0, "flag": "LOW (Mild Non-Regenerative Anemia)"},
                    "Hematocrit": {"value": 24.2, "unit": "%", "ref_min": 30.0, "ref_max": 45.0, "flag": "LOW"},
                    "WBC": {"value": 19.8, "unit": "K/uL", "ref_min": 5.5, "ref_max": 19.5, "flag": "HIGH (Mild Leukocytosis with Neutrophilia)"},
                    "Total_Protein": {"value": 9.4, "unit": "g/dL", "ref_min": 6.0, "ref_max": 8.0, "flag": "HIGH"},
                    "Albumin": {"value": 2.4, "unit": "g/dL", "ref_min": 2.5, "ref_max": 3.9, "flag": "LOW"},
                    "Globulin": {"value": 7.0, "unit": "g/dL", "ref_min": 2.8, "ref_max": 5.1, "flag": "CRITICALLY HIGH"},
                    "AG_Ratio": {"value": 0.34, "unit": "", "ref_min": 0.60, "ref_max": 1.20, "flag": "CRITICALLY LOW (< 0.40 highly suggestive of FIP)"},
                    "BUN": {"value": 26.0, "unit": "mg/dL", "ref_min": 16.0, "ref_max": 36.0, "flag": "NORMAL"},
                    "Creatinine": {"value": 1.3, "unit": "mg/dL", "ref_min": 0.8, "ref_max": 2.4, "flag": "NORMAL"},
                    "ALT": {"value": 48.0, "unit": "U/L", "ref_min": 12.0, "ref_max": 130.0, "flag": "NORMAL"},
                    "Bilirubin_Total": {"value": 0.6, "unit": "mg/dL", "ref_min": 0.0, "ref_max": 0.4, "flag": "SLIGHTLY HIGH"}
                }
            }
        ],
        "imaging_studies": [
            {
                "image_id": "img_xray_20260828_01",
                "date": "2026-08-28",
                "modality": "Thoracic & Abdominal Digital Radiograph",
                "view": "Right Lateral & Ventrodorsal",
                "image_url": "/static/images/michelin_xray_sample.png",
                "findings": "Mild pleural fissure line prominence in caudoventral thorax; loss of serosal detail in mid-abdomen consistent with mild peritoneal free fluid."
            }
        ]
    },
    "pat_luna_002": {
        "id": "pat_luna_002",
        "name": "Luna",
        "species": "Feline",
        "breed": "Siamese",
        "age_years": 8.5,
        "sex": "Female Spayed",
        "weight_kg": 3.2,
        "owner_name": "Valeria Morales",
        "primary_clinic": "Clínica Veterinaria Aguascalientes",
        "microchip": "985141008821940",
        "created_at": "2026-05-10T11:00:00Z",
        "status": "Chronic Care Monitoring",
        "critical_flags": ["Elevated SDMA (Early IRIS Stage 2 CKD)", "Borderline Systemic Hypertension"],
        "vitals_history": [
            {"date": "2026-05-10", "weight_kg": 3.4, "temp_c": 38.4, "heart_rate": 170, "resp_rate": 24},
            {"date": "2026-08-15", "weight_kg": 3.2, "temp_c": 38.5, "heart_rate": 185, "resp_rate": 26}
        ],
        "owner_observations": [
            {
                "timestamp": "2026-08-14T14:00:00Z",
                "reporter": "Owner (Valeria)",
                "note": "Luna is drinking from the water fountain significantly more often. Litter box clumps have doubled in volume.",
                "severity": "Medium"
            }
        ],
        "clinical_notes": [
            {
                "visit_id": "vis_20260815",
                "date": "2026-08-15",
                "vet_name": "Dr. Carlos Mendez, MVZ",
                "subjective": "Presenting for polydipsia/polyuria and mild coat dullness.",
                "objective": "T: 38.5°C, HR: 185 bpm, Systolic BP: 162 mmHg (Doppler). Kidneys palpate slightly small and irregular.",
                "assessment": "Suspect Early Feline Chronic Kidney Disease (CKD) with mild pre-hypertension.",
                "plan": "Urine specific gravity, SDMA, serum creatinine, renal diet transition."
            }
        ],
        "lab_results": [
            {
                "lab_id": "lab_renal_20260815",
                "date": "2026-08-15",
                "panel_type": "Renal Function Panel",
                "metrics": {
                    "SDMA": {"value": 16.5, "unit": "ug/dL", "ref_min": 0.0, "ref_max": 14.0, "flag": "HIGH (Early Renal Loss)"},
                    "Creatinine": {"value": 1.9, "unit": "mg/dL", "ref_min": 0.8, "ref_max": 2.4, "flag": "BORDERLINE HIGH (IRIS Stage 2)"},
                    "BUN": {"value": 38.0, "unit": "mg/dL", "ref_min": 16.0, "ref_max": 36.0, "flag": "HIGH"},
                    "USG": {"value": 1.022, "unit": "", "ref_min": 1.035, "ref_max": 1.060, "flag": "INADEQUATELY CONCENTRATED"}
                }
            }
        ],
        "imaging_studies": []
    }
}

class PatientVault:
    """Manages longitudinal feline patient records."""

    @staticmethod
    def list_patients() -> List[Dict[str, Any]]:
        return [
            {
                "id": p["id"],
                "name": p["name"],
                "breed": p["breed"],
                "age_years": p["age_years"],
                "weight_kg": p["weight_kg"],
                "status": p["status"],
                "critical_flags": p["critical_flags"]
            }
            for p in PATIENTS_STORE.values()
        ]

    @staticmethod
    def get_patient(patient_id: str) -> Optional[Dict[str, Any]]:
        if patient_id in PATIENTS_STORE:
            return copy.deepcopy(PATIENTS_STORE[patient_id])
        return None

    @staticmethod
    def add_clinical_note(patient_id: str, note_data: Dict[str, Any]) -> bool:
        if patient_id not in PATIENTS_STORE:
            return False
        PATIENTS_STORE[patient_id]["clinical_notes"].insert(0, note_data)
        return True

    @staticmethod
    def add_owner_observation(patient_id: str, obs_data: Dict[str, Any]) -> bool:
        if patient_id not in PATIENTS_STORE:
            return False
        PATIENTS_STORE[patient_id]["owner_observations"].insert(0, obs_data)
        return True

    @staticmethod
    def add_lab_result(patient_id: str, lab_data: Dict[str, Any]) -> bool:
        if patient_id not in PATIENTS_STORE:
            return False
        PATIENTS_STORE[patient_id]["lab_results"].insert(0, lab_data)
        return True

    @staticmethod
    def add_imaging_study(patient_id: str, image_data: Dict[str, Any]) -> bool:
        if patient_id not in PATIENTS_STORE:
            return False
        PATIENTS_STORE[patient_id]["imaging_studies"].insert(0, image_data)
        return True
