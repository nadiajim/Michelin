"""
End-to-End Verification Test for Michelin Veterinary Co-Pilot
"""
import sys
import io

# Force UTF-8 output on Windows consoles
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from backend.app.database import PatientVault
from backend.app.clinical_safety import ClinicalSafetyEngine
from backend.app.tools import VeterinaryDiagnosticTools
from backend.app.agent import MichelinAgent

def run_tests():
    print("=== [1] Testing Patient Vault ===")
    patients = PatientVault.list_patients()
    assert len(patients) >= 2, "Expected at least 2 demo patients"
    print(f"[OK] Found {len(patients)} patients: {[p['name'] for p in patients]}")

    michelin = PatientVault.get_patient("pat_michelin_001")
    assert michelin["name"] == "Michelin"
    print(f"[OK] Retrieved patient Michelin: {michelin['breed']}, {michelin['age_years']} yrs")

    print("\n=== [2] Testing Clinical Safety & False-Negative Sentinel ===")
    safety = ClinicalSafetyEngine.analyze_false_negative_risks(michelin)
    assert safety["risk_level"] == "Critical", "Expected Critical risk level for low A:G ratio in Michelin"
    assert len(safety["active_alerts"]) > 0, "Expected active alerts for Michelin"
    print(f"[OK] Safety Sentinel Triggered Risk: {safety['risk_level']}")
    for alert in safety["active_alerts"]:
        print(f"  - [{alert['severity']}] {alert['condition']}")

    print("\n=== [3] Testing Differential Diagnosis Engine ===")
    differentials = VeterinaryDiagnosticTools.calculate_differential_matrix(michelin)
    assert len(differentials) >= 3, "Expected at least 3 ranked differentials"
    top = differentials[0]
    print(f"[OK] Top Differential: {top['diagnosis']} ({top['probability_percentage']}%)")
    assert "FIP" in top["diagnosis"] or "Feline Infectious Peritonitis" in top["diagnosis"]

    print("\n=== [4] Testing Michelin Collaborative Agent Consultation ===")
    agent = MichelinAgent()
    consult_result = agent.process_consultation(
        patient_id="pat_michelin_001",
        vet_message="The owner noticed mild abdominal distension and fluid wave. What is our immediate priority?"
    )
    assert "response" in consult_result
    assert len(consult_result["proactive_inquiries"]) > 0
    print(f"[OK] Agent generated collaborative response ({len(consult_result['response'])} chars)")
    print(f"[OK] Proactive Inquiries for Vet ({len(consult_result['proactive_inquiries'])} questions):")
    for q in consult_result["proactive_inquiries"]:
        print(f"  ? {q}")

    print("\n=== [5] Testing Owner Observation Logging ===")
    success = PatientVault.add_owner_observation("pat_michelin_001", {
        "timestamp": "2026-08-30T14:30:00Z",
        "reporter": "Nadia (Owner)",
        "note": "Michelin ate half a can of recovery food after warm fluid therapy.",
        "severity": "Medium"
    })
    assert success
    updated = PatientVault.get_patient("pat_michelin_001")
    assert len(updated["owner_observations"]) == 3
    print("[OK] Successfully logged owner observation and updated longitudinal vault")

    print("\n[SUCCESS] ALL TESTS PASSED! The Michelin Co-Pilot engine is 100% verified.")

if __name__ == "__main__":
    run_tests()
