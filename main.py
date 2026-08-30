"""
FastAPI Server for Michelin Veterinary Collaborative Co-Pilot
Exposes RESTful endpoints for patient records, multimodal analysis, and collaborative clinical sessions.
"""
import os
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from .database import PatientVault
from .agent import MichelinAgent
from .tools import VeterinaryDiagnosticTools
from .clinical_safety import ClinicalSafetyEngine

app = FastAPI(
    title="Michelin Veterinary Clinical Co-Pilot API",
    description="Multimodal collaborative diagnostic agent for feline internal medicine powered by Gemini and Google Cloud.",
    version="1.0.0"
)

# Enable CORS for local development and cloud deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = MichelinAgent()

class ConsultationRequest(BaseModel):
    patient_id: str
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = []

class ClinicalNoteRequest(BaseModel):
    vet_name: str
    subjective: str
    objective: str
    assessment: str
    plan: str

class OwnerObsRequest(BaseModel):
    reporter: str
    note: str
    severity: str = "Medium"

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "michelin-vet-copilot",
        "gemini_live_client": agent.client is not None,
        "cloud_region": os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
    }

@app.get("/api/patients")
def list_patients():
    return {"patients": PatientVault.list_patients()}

@app.get("/api/patients/{patient_id}")
def get_patient_profile(patient_id: str):
    patient = PatientVault.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    safety = ClinicalSafetyEngine.analyze_false_negative_risks(patient)
    differentials = VeterinaryDiagnosticTools.calculate_differential_matrix(patient)
    return {
        "patient": patient,
        "safety_analysis": safety,
        "differentials": differentials
    }

@app.post("/api/patients/{patient_id}/consult")
def consult_agent(patient_id: str, request: ConsultationRequest):
    result = agent.process_consultation(
        patient_id=patient_id,
        vet_message=request.message,
        conversation_history=request.conversation_history
    )
    return result

@app.post("/api/patients/{patient_id}/notes")
def add_clinical_note(patient_id: str, req: ClinicalNoteRequest):
    note = {
        "visit_id": f"vis_manual_{os.urandom(4).hex()}",
        "date": "2026-08-30",
        "vet_name": req.vet_name,
        "subjective": req.subjective,
        "objective": req.objective,
        "assessment": req.assessment,
        "plan": req.plan
    }
    success = PatientVault.add_clinical_note(patient_id, note)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"status": "success", "note": note}

@app.post("/api/patients/{patient_id}/owner-obs")
def add_owner_observation(patient_id: str, req: OwnerObsRequest):
    obs = {
        "timestamp": "2026-08-30T14:00:00Z",
        "reporter": req.reporter,
        "note": req.note,
        "severity": req.severity
    }
    success = PatientVault.add_owner_observation(patient_id, obs)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"status": "success", "observation": obs}

@app.post("/api/patients/{patient_id}/upload-imaging")
async def upload_imaging(
    patient_id: str,
    modality: str = Form("Thoracic Radiograph"),
    view: str = Form("Right Lateral"),
    findings: str = Form(""),
    file: Optional[UploadFile] = File(None)
):
    image_record = {
        "image_id": f"img_{os.urandom(4).hex()}",
        "date": "2026-08-30",
        "modality": modality,
        "view": view,
        "image_url": "/static/images/michelin_xray_sample.png",
        "findings": findings or "Digital imaging uploaded for multimodal assessment."
    }
    PatientVault.add_imaging_study(patient_id, image_record)
    analysis = VeterinaryDiagnosticTools.analyze_radiograph_metadata(image_record)
    return {
        "status": "success",
        "imaging_record": image_record,
        "analysis": analysis
    }

# Mount static frontend assets
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Michelin Veterinary Co-Pilot API is running."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
