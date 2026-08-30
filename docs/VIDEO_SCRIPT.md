# 🎬 Michelin — 4-Minute Demo Video Script & Storyboard
**All Things Agentic Hackathon** | **Track:** The Collaborative Partner

---

## ⏱️ Video Structure Breakdown (Total Duration: 4:00)

| Timestamp | Section | Key Visual | Core Message |
|---|---|---|---|
| **0:00 - 0:45** | **The Problem & Personal Inspiration** | Photo of Michelin the cat / Clinical emergency room b-roll | Cats hide illness; missed diagnoses cost lives. Michelin's story. |
| **0:45 - 1:30** | **The Solution & Collaborative Architecture** | Architecture diagram & UI introduction | Introducing Michelin: Multimodal clinical partner powered by Gemini & GCP. |
| **1:30 - 3:15** | **Live Interactive Walkthrough** | Web UI demo: Longitudinal timeline, X-Ray viewer, Agent Chat | Proactive questions, false-negative sentinel, live differential matrix. |
| **3:15 - 3:45** | **Google Cloud Proof & Backend Verification** | Google Cloud Console, Cloud Run service, Vertex AI logs | Showing live deployment on Google Cloud with zero-trust architecture. |
| **3:45 - 4:00** | **Impact & Real-World Pilot** | Aguascalientes clinic photo / Closing slide | Piloting in Aguascalientes, Mexico. Saving feline lives worldwide. |

---

## 🎙️ Turn-by-Turn Narration & Storyboard

### [0:00 - 0:45] Act 1: The Problem & The Mission
* **Visual:** Speaker on camera with warm, sincere tone. Cut to photo of Michelin the cat.
* **Narration:**
  > *"Meet Michelin. He was the love of my life. Like so many cats, Michelin suffered from a progressive condition that wasn't caught in time. In veterinary medicine, cats are evolutionary masters at concealing pain. By the time subtle symptoms like mild lethargy or decreased appetite appear, conditions like FIP, cardiomyopathy, or kidney disease have often reached critical stages.*
  >
  > *During a hectic 15-minute consultation, it is extraordinarily difficult for veterinarians to cross-reference months of owner notes, subtle blood biomarker ratios, and subtle imaging clues. We built Michelin to change that forever."*

---

### [0:45 - 1:30] Act 2: Introducing Michelin (The Collaborative Partner)
* **Visual:** Full-screen presentation of the System Architecture Diagram, transitioning smoothly to the live web application.
* **Narration:**
  > *"Submitted to the **Collaborative Partner** track of the All Things Agentic Hackathon, **Michelin** is an intelligent veterinary clinical co-pilot powered by **Google Gemini 2.5/3.5 Pro** and deployed on **Google Cloud Run**.*
  >
  > *Michelin doesn't just passively answer questions. It actively collaborates with the veterinarian. It ingests longitudinal patient records—including digital radiographs, blood chemistry panels, and owner symptom logs—and works as an experienced feline medicine specialist by your side, proactively prompting the vet to eliminate dangerous false negatives."*

---

### [1:30 - 3:15] Act 3: Live Application Walkthrough
* **Visual:** Screen recording of the **Michelin Veterinary Dashboard** in action.
* **Action 1: Longitudinal Vault & Sentinel (1:30 - 2:00)**
  > *"Here is Michelin's live patient profile. On the left, our **False-Negative Sentinel** has already detected a critical warning: an inverted Albumin-to-Globulin ratio of 0.34 and a 14% progressive weight loss over seven weeks.*
  >
  > *In the center, our multimodal diagnostic viewer analyzes his thoracic radiograph using Gemini Vision, identifying subtle pleural fissure lines and peritoneal fluid."*

* **Action 2: Collaborative Agent Interaction (2:00 - 2:45)**
  > *"Look at the right panel. The Michelin Agent doesn't wait for us to figure everything out. It proactively surfaces high-yield clinical inquiries: 'Did you perform a diagnostic centesis with a Rivalta test?' or 'What is the resting sleeping respiratory rate?'*
  >
  > *Let's ask the agent: 'The owner noticed abdominal distension and fluid wave. What is our immediate priority?'*
  >
  > *Watch how fast the agent synthesizes the AAFP guidelines: It calculates a 94% probability for FIP, warns against delaying with standard antibiotics, and provides immediate step-by-step diagnostic rule-out protocols."*

* **Action 3: Live Differential Matrix & Owner Logging (2:45 - 3:15)**
  > *"The Differential Diagnosis Matrix dynamically updates in real time, giving veterinarians clear probabilistic rankings and definitive rule-out tests. Owners can also submit home observation logs directly to the vault, closing the loop between clinic and home."*

---

### [3:15 - 3:45] Act 4: Proof of Google Cloud Deployment
* **Visual:** Switch browser tab to **Google Cloud Console**:
  - Show the **Cloud Run** service `michelin-vet-copilot` in `us-central1` with green checkmark status.
  - Show Cloud Logs streaming request metrics and Gemini API integration.
  - Show Google Cloud Build deployment pipeline.
* **Narration:**
  > *"Under the hood, Michelin is fully containerized and running in production on **Google Cloud Run** in `us-central1`. Our serverless backend orchestrates multimodal payloads with Gemini, backed by Google Cloud Firestore for secure, longitudinal patient vaults and Cloud Storage for high-resolution DICOM imaging."*

---

### [3:45 - 4:00] Act 5: Real-World Impact & Conclusion
* **Visual:** Return to presenter with contact info and clinic photo of Clínica Veterinaria Aguascalientes.
* **Narration:**
  > *"Michelin isn't just a prototype—it is currently being piloted with real clinical data at a veterinary clinic in Aguascalientes, Mexico. With Gemini and Google Cloud, we are turning grief into hope, ensuring every cat receives the timely diagnosis they deserve.*
  >
  > *Thank you for checking out Michelin!"*

---

## 💡 Recording Tips for Success
1. **Screen Resolution**: Record in 1080p (1920x1080) at 60fps for crisp text.
2. **Audio**: Use a dedicated microphone with low background noise.
3. **Cloud Run Proof**: Keep the Google Cloud Console tab open in a separate window to seamlessly switch and demonstrate proof within 20 seconds.
