# 🐾 Michelin — Collaborative Feline Clinical Co-Pilot
**All Things Agentic Hackathon Submission**
* **Track:** The Collaborative Partner
* **Target Category:** Healthcare & Veterinary AI / Autonomous Clinical Systems
* **Pilot Site:** Clínica Veterinaria Aguascalientes, Mexico

---

## 📌 Elevator Pitch
**Michelin** is an intelligent, multimodal veterinary clinical co-pilot powered by Gemini and Google Cloud that collaborates with veterinarians and cat owners to prevent missed or delayed feline diagnoses. By fusing longitudinal health records, X-rays, lab panels, and owner symptom logs, Michelin actively asks clarifying diagnostic questions, formulates probabilistic differential diagnoses, and enforces strict false-negative safety guardrails for stealth feline conditions.

---

## 💖 Inspiration
Michelin is the love of my life. He suffered from a severe feline health issue that was not detected in time, leading to heartbreak that no pet parent or veterinarian should ever have to endure. 

Cats are biologically hardwired to mask illness and pain until diseases reach advanced, irreversible stages. Subtle shifts—such as a dropping Albumin-to-Globulin (A:G) ratio, minor weight decline, or subtle changes in sleeping respiratory rate—are frequently overlooked during brief 15-minute consultations. 

We created **Michelin** so that no cat or human has to go through this pain again, turning retrospective grief into proactive, life-saving clinical collaboration.

---

## ⚙️ What It Does

Michelin transforms veterinary diagnosis from static, isolated consultations into a continuous, collaborative clinical partnership:

1. **Longitudinal Patient Health Vault**:
   - Aggregates and correlates multi-source health data: DICOM/radiographs, ultrasounds, CBC & chemistry panels, consultation SOAP notes, and real-time home logs from pet owners.
2. **Bidirectional Clinical Collaboration (The Collaborative Partner)**:
   - Rather than acting as a passive chatbot, Michelin actively leads diagnostic exploration. It asks veterinarians targeted, high-yield clarifying questions (e.g., *"Did you notice paradoxical breathing or muffled heart sounds on auscultation?"*, *"Has fluid viscosity been checked with a Rivalta test?"*).
3. **High-Sensitivity False-Negative Sentinel**:
   - Specifically engineered to catch stealth feline killers (Feline Infectious Peritonitis [FIP], Hypertrophic Cardiomyopathy [HCM], and early Chronic Kidney Disease [CKD]). It flags discordant biomarkers (e.g. inverted A:G ratio < 0.45, elevated SDMA despite normal creatinine) before irreparable organ damage occurs.
4. **Live Probabilistic Differential Diagnosis Matrix**:
   - Ranks differential diagnoses in real time, accompanied by concrete "Must-Rule-Out" tests and immediate therapeutic action protocols grounded in AAFP (American Association of Feline Practitioners) and WSAVA guidelines.

---

## 🏗️ How We Built It

Michelin is built on a state-of-the-art Google AI and Google Cloud foundation:

* **Google Gemini 2.5 / 3.5 Pro Multimodal**: Performs high-fidelity reasoning across feline radiograph images, lab blood panels, and longitudinal clinical text.
* **Google Agent Development Framework & Antigravity Agent Runtime**: Powers the collaborative agent loops, tool-calling interfaces, and bidirectional clinical inquiry.
* **Google Cloud Run**: Serverless, autoscaling backend hosting our FastAPI microservices and static clinical UI with low latency and zero idle costs.
* **Google Cloud Firestore & Cloud Storage**: Secure, HIPAA/enterprise-compliant storage for longitudinal patient histories, DICOM imaging, and lab reports.
* **Clinical Safety & Grounding Layer**: Rule-based and semantic guardrails grounded in AAFP FIP Guidelines, IRIS Staging, and ACVIM Cardiomyopathy Consensus to eliminate diagnostic hallucinations and minimize false negatives.

---

## 🛡️ Challenges We Ran Into & Clinical Safety

Since the data directly concerns a feline patient's health and life, our highest engineering hurdle was **eliminating false negatives**:
* **The "Asymptomatic Illusion" Challenge**: Early-stage feline diseases often present with nonspecific signs (mild lethargy, fluctuating low-grade fever). We built custom biomarker ratio detectors (such as A:G ratio inversion and weight-loss velocity tracking) that trigger proactive alerts even when standard reference ranges look deceptively "borderline".
* **Source Reliability & Grounding**: We anchored every clinical suggestion and differential score to verified veterinary literature (AAFP, WSAVA, VIN) with explicit references displayed in the UI.

---

## 🏆 Accomplishments That We're Proud Of

1. **Real-World Deployment in Aguascalientes**:
   - Partnered with a veterinary clinic in Aguascalientes, Mexico, piloting the system with real feline clinical records to validate usability and diagnostic speed.
2. **True Collaborative Partnership**:
   - The agent doesn't just answer—it proactively guides veterinarians through complex diagnostic trees and actively integrates owner behavioral logs.
3. **Production-Ready Google Cloud Architecture**:
   - Deployed on Google Cloud Run with complete Docker containerization and continuous deployment via Google Cloud Build.

---

## 🔬 What We Learned

* **Agentic Proactivity > Passive Search**: Veterinarians don't need another search engine; they need a vigilant co-pilot that flags anomalies they might miss during a busy clinic shift.
* **Multimodal Fusion is Essential in Vet Medicine**: Diagnostic truth in feline medicine rarely comes from a single test; it requires the synthesis of visual imaging (X-rays), numerical data (biomarkers), and owner behavioral observations over time.

---

## 🚀 What's Next for Michelin

* **Edge Ultrasound & POCUS Video Analysis**: Expanding multimodal capabilities to ingest live point-of-care ultrasound (POCUS) video streams during examinations.
* **Continuous IoT Wearable Integration**: Integrating smart cat collars and smart litter box sensors (monitoring daily weight, urination frequency, and sleep respiration rate) for automated longitudinal alerts.
* **Nationwide Veterinary Clinic Rollout**: Expanding the pilot from Aguascalientes to veterinary hospitals across Mexico and Latin America.

---

## 🧰 Built With
* `Google Gemini 2.5/3.5 Pro`
* `Google Agent Development Kit (ADK)`
* `Antigravity Agent Runtime`
* `Google Cloud Run`
* `Google Cloud Firestore`
* `Google Cloud Storage`
* `Google Cloud Build`
* `Python & FastAPI`
* `Tailwind CSS & JavaScript`
