/**
 * Michelin Veterinary Clinical Co-Pilot Client Application
 */

let currentPatientId = "pat_michelin_001";
let currentPatientData = null;
let conversationHistory = [];

document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) {
    lucide.createIcons();
  }
  loadSelectedPatient();
});

async function loadSelectedPatient() {
  const selectElem = document.getElementById("patientSelect");
  currentPatientId = selectElem.value;
  conversationHistory = [];

  try {
    const res = await fetch(`/api/patients/${currentPatientId}`);
    if (!res.ok) throw new Error("Failed to fetch patient data");
    const data = await res.json();
    currentPatientData = data.patient;
    
    renderPatientProfile(data.patient);
    renderSafetyAlerts(data.safety_analysis);
    renderTimeline(data.patient);
    renderLabResults(data.patient);
    renderClinicalNotes(data.patient);
    renderDifferentials(data.differentials);
    renderProactivePills(data.safety_analysis.proactive_collaborative_inquiries);
    
    // Seed initial agent welcome & clinical summary
    initChatWelcome(data.patient, data.safety_analysis, data.differentials);

    if (window.lucide) {
      lucide.createIcons();
    }
  } catch (err) {
    console.error("Error loading patient:", err);
  }
}

function renderPatientProfile(patient) {
  document.getElementById("patientName").innerText = patient.name;
  document.getElementById("patientMeta").innerText = `${patient.breed} • ${patient.age_years} Years • ${patient.sex}`;
  document.getElementById("patientOwner").innerText = `Owner: ${patient.owner_name} • ${patient.primary_clinic}`;
  
  const latestVital = patient.vitals_history[patient.vitals_history.length - 1] || {};
  document.getElementById("patientWeight").innerHTML = `${latestVital.weight_kg || patient.weight_kg} kg <span class="text-[9px] text-red-500 font-semibold">(-14%)</span>`;
  document.getElementById("patientTemp").innerText = `${latestVital.temp_c || 38.5} °C`;
  document.getElementById("patientResp").innerText = `${latestVital.resp_rate || 28} bpm`;
}

function renderSafetyAlerts(safety) {
  const container = document.getElementById("safetyAlertContent");
  if (!safety || !safety.active_alerts || safety.active_alerts.length === 0) {
    container.innerHTML = `<span class="text-emerald-700 font-medium">No critical false-negative flags active. Routine monitoring.</span>`;
    return;
  }

  let html = "";
  safety.active_alerts.forEach(alert => {
    html += `
      <div class="mb-2 last:mb-0">
        <p class="font-bold text-red-800 text-[11px] mb-0.5">⚠️ ${alert.condition}</p>
        <p class="text-[11px] text-red-900/90 leading-snug">${alert.rationale}</p>
        <p class="text-[10px] text-red-700 font-semibold mt-1">→ Action: ${alert.action}</p>
      </div>
    `;
  });
  container.innerHTML = html;
}

function renderTimeline(patient) {
  const container = document.getElementById("timelineContainer");
  let items = [];

  // Combine Owner Observations and Clinical Notes
  (patient.owner_observations || []).forEach(obs => {
    items.push({
      type: "owner",
      date: obs.timestamp.split("T")[0],
      title: obs.reporter,
      text: obs.note,
      badge: obs.severity === "Urgent" ? "bg-red-100 text-red-700" : "bg-amber-100 text-amber-700"
    });
  });

  (patient.clinical_notes || []).forEach(note => {
    items.push({
      type: "clinical",
      date: note.date,
      title: note.vet_name,
      text: `<strong>Assessment:</strong> ${note.assessment}<br><span class="text-slate-500">${note.plan}</span>`,
      badge: "bg-blue-100 text-blue-700"
    });
  });

  items.sort((a, b) => new Date(b.date) - new Date(a.date));

  container.innerHTML = items.map(item => `
    <div class="p-2.5 rounded-xl border border-slate-100 bg-slate-50/70 text-xs space-y-1">
      <div class="flex items-center justify-between">
        <span class="font-bold text-slate-800">${item.title}</span>
        <span class="text-[10px] px-1.5 py-0.5 rounded font-semibold ${item.badge}">${item.date}</span>
      </div>
      <p class="text-slate-600 text-[11px] leading-relaxed">${item.text}</p>
    </div>
  `).join("");
}

function renderLabResults(patient) {
  const tbody = document.getElementById("labTableBody");
  const labs = patient.lab_results || [];
  if (labs.length === 0) {
    tbody.innerHTML = `<tr><td colspan="4" class="py-4 text-center text-slate-400">No lab panels on file</td></tr>`;
    return;
  }

  const metrics = labs[0].metrics;
  let rows = "";
  for (const [key, data] of Object.entries(metrics)) {
    const isCritical = data.flag.includes("CRITICAL");
    const isHighOrLow = data.flag.includes("HIGH") || data.flag.includes("LOW");
    
    let flagBadge = `<span class="px-1.5 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-600">Normal</span>`;
    if (isCritical) {
      flagBadge = `<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-red-100 text-red-700">${data.flag}</span>`;
    } else if (isHighOrLow) {
      flagBadge = `<span class="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-amber-100 text-amber-800">${data.flag}</span>`;
    }

    rows += `
      <tr class="${isCritical ? 'bg-red-50/50' : 'hover:bg-slate-50'}">
        <td class="py-2 px-2.5 font-semibold text-slate-800">${key.replace('_', ' ')}</td>
        <td class="py-2 px-2.5 font-mono font-bold ${isCritical ? 'text-red-700' : 'text-slate-900'}">${data.value} ${data.unit}</td>
        <td class="py-2 px-2.5 text-slate-400 font-mono text-[11px]">${data.ref_min} - ${data.ref_max}</td>
        <td class="py-2 px-2.5">${flagBadge}</td>
      </tr>
    `;
  }
  tbody.innerHTML = rows;
}

function renderClinicalNotes(patient) {
  const container = document.getElementById("clinicalNotesList");
  const notes = patient.clinical_notes || [];
  if (notes.length === 0) {
    container.innerHTML = `<p class="text-xs text-slate-400">No clinical visit notes recorded.</p>`;
    return;
  }

  container.innerHTML = notes.map(note => `
    <div class="bg-slate-50 rounded-xl p-3 border border-slate-200 text-xs space-y-2">
      <div class="flex justify-between items-center font-bold text-slate-800">
        <span>${note.vet_name}</span>
        <span class="text-slate-400 font-normal">${note.date}</span>
      </div>
      <div>
        <span class="font-semibold text-slate-700 block">Objective Findings:</span>
        <p class="text-slate-600 text-[11px]">${note.objective}</p>
      </div>
      <div>
        <span class="font-semibold text-slate-700 block">Assessment & Plan:</span>
        <p class="text-slate-600 text-[11px]">${note.assessment} — <em>${note.plan}</em></p>
      </div>
    </div>
  `).join("");
}

function renderDifferentials(differentials) {
  const container = document.getElementById("differentialContainer");
  if (!differentials || differentials.length === 0) {
    container.innerHTML = `<p class="text-xs text-slate-400">No differentials generated.</p>`;
    return;
  }

  container.innerHTML = differentials.map((diff, index) => {
    const isTop = index === 0;
    const barColor = diff.severity === 'CRITICAL' ? 'bg-red-600' : diff.severity === 'HIGH' ? 'bg-amber-500' : 'bg-blue-500';
    return `
      <div class="p-3 rounded-xl border ${isTop ? 'border-red-200 bg-red-50/30' : 'border-slate-100 bg-slate-50/50'} space-y-2">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <span class="w-5 h-5 rounded-full ${isTop ? 'bg-red-600' : 'bg-slate-300'} text-white text-[10px] font-bold flex items-center justify-center">${index + 1}</span>
            <h4 class="text-xs font-bold text-slate-900">${diff.diagnosis}</h4>
          </div>
          <span class="text-xs font-extrabold font-mono ${diff.severity === 'CRITICAL' ? 'text-red-700' : 'text-slate-700'}">${diff.probability_percentage}%</span>
        </div>
        
        <!-- Probability Bar -->
        <div class="w-full bg-slate-200 rounded-full h-1.5 overflow-hidden">
          <div class="${barColor} h-1.5 rounded-full" style="width: ${diff.probability_percentage}%"></div>
        </div>

        <div class="text-[11px] text-slate-600 space-y-1">
          <p><strong>Primary Rule-Out:</strong> ${diff.rule_out_tests ? diff.rule_out_tests[0] : 'Further diagnostic panels'}</p>
        </div>
      </div>
    `;
  }).join("");
}

function renderProactivePills(inquiries) {
  const container = document.getElementById("proactivePillsContainer");
  if (!inquiries || inquiries.length === 0) {
    container.innerHTML = `<span class="text-[10px] text-slate-400">All preliminary questions answered.</span>`;
    return;
  }

  container.innerHTML = inquiries.map(inquiry => `
    <button onclick="askQuickInquiry('${inquiry.replace(/'/g, "\\'")}')" class="text-left text-[10px] bg-white hover:bg-blue-50 text-blue-700 border border-blue-200 rounded-lg px-2 py-1 transition shadow-2xs font-medium">
      💬 ${inquiry.length > 55 ? inquiry.substring(0, 52) + '...' : inquiry}
    </button>
  `).join("");
}

function switchDiagnosticTab(tab) {
  const tabs = ["imaging", "labs", "notes"];
  tabs.forEach(t => {
    const btn = document.getElementById(`tabBtn${t.charAt(0).toUpperCase() + t.slice(1)}`);
    const content = document.getElementById(`tabContent${t.charAt(0).toUpperCase() + t.slice(1)}`);
    if (t === tab) {
      btn.className = "px-3 py-1.5 text-xs font-bold rounded-lg bg-blue-50 text-blue-700 border border-blue-200";
      content.classList.remove("hidden");
    } else {
      btn.className = "px-3 py-1.5 text-xs font-medium rounded-lg text-slate-600 hover:bg-slate-50";
      content.classList.add("hidden");
    }
  });
}

function initChatWelcome(patient, safety, differentials) {
  const chat = document.getElementById("chatMessages");
  const topDiff = differentials[0] || { diagnosis: "Feline Infectious Peritonitis", probability_percentage: 94 };
  
  chat.innerHTML = `
    <div class="chat-bubble-agent p-3 rounded-2xl rounded-tl-sm space-y-1.5">
      <div class="flex items-center space-x-1.5 font-bold text-emerald-800">
        <i data-lucide="bot" class="w-3.5 h-3.5"></i>
        <span>Michelin Clinical Sentinel</span>
      </div>
      <p class="text-emerald-950">
        Hello Dr. Mendez! I have synthesized <strong>${patient.name}'s</strong> longitudinal file. 
        Notice the critical A:G ratio inversion (<strong>0.34</strong>) alongside the 14% progressive weight loss and persistent pyrexia (39.7°C).
      </p>
      <p class="text-emerald-900 font-semibold text-[11px]">
        Top Diagnostic Priority: <strong>${topDiff.diagnosis} (${topDiff.probability_percentage}%)</strong>.
      </p>
    </div>
  `;
}

function askQuickInquiry(question) {
  document.getElementById("chatInput").value = question;
  sendConsultMessage(new Event("submit"));
}

async function sendConsultMessage(event) {
  event.preventDefault();
  const input = document.getElementById("chatInput");
  const message = input.value.trim();
  if (!message) return;

  const chat = document.getElementById("chatMessages");

  // Append Vet message
  chat.innerHTML += `
    <div class="chat-bubble-vet p-3 rounded-2xl rounded-tr-sm ml-6 space-y-1">
      <div class="flex items-center justify-end space-x-1.5 font-bold text-blue-800">
        <span>Dr. Carlos Mendez</span>
        <i data-lucide="user" class="w-3.5 h-3.5"></i>
      </div>
      <p class="text-blue-950 text-right">${escapeHtml(message)}</p>
    </div>
  `;
  input.value = "";
  chat.scrollTop = chat.scrollHeight;

  // Append typing loader
  const loaderId = `loader_${Date.now()}`;
  chat.innerHTML += `
    <div id="${loaderId}" class="chat-bubble-agent p-3 rounded-2xl rounded-tl-sm space-y-1 text-slate-500">
      <div class="flex items-center space-x-2">
        <span class="animate-spin w-3.5 h-3.5 border-2 border-emerald-500 border-t-transparent rounded-full"></span>
        <span>Michelin Agent reasoning & grounding against AAFP guidelines...</span>
      </div>
    </div>
  `;
  chat.scrollTop = chat.scrollHeight;

  try {
    const res = await fetch(`/api/patients/${currentPatientId}/consult`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        patient_id: currentPatientId,
        message: message,
        conversation_history: conversationHistory
      })
    });

    const data = await res.json();
    const loader = document.getElementById(loaderId);
    if (loader) loader.remove();

    // Render agent response with Markdown
    const renderedHtml = marked.parse(data.response || "No response received.");

    chat.innerHTML += `
      <div class="chat-bubble-agent p-3.5 rounded-2xl rounded-tl-sm space-y-2 text-emerald-950">
        <div class="flex items-center space-x-1.5 font-bold text-emerald-800">
          <i data-lucide="sparkles" class="w-3.5 h-3.5 text-emerald-600"></i>
          <span>Michelin Collaborative Assessment</span>
        </div>
        <div class="prose prose-xs max-w-none text-emerald-950 leading-relaxed">
          ${renderedHtml}
        </div>
      </div>
    `;

    // Refresh proactive pills & differentials if updated
    if (data.proactive_inquiries) {
      renderProactivePills(data.proactive_inquiries);
    }
    if (data.differential_matrix) {
      renderDifferentials(data.differential_matrix);
    }

    conversationHistory.push({ role: "vet", message: message });
    conversationHistory.push({ role: "agent", message: data.response });

    if (window.lucide) {
      lucide.createIcons();
    }
    chat.scrollTop = chat.scrollHeight;
  } catch (err) {
    const loader = document.getElementById(loaderId);
    if (loader) loader.remove();
    chat.innerHTML += `<div class="p-2 text-red-600 text-[11px]">Error reaching agent server.</div>`;
  }
}

function openAddObservationModal() {
  document.getElementById("obsModal").classList.remove("hidden");
}

function closeAddObservationModal() {
  document.getElementById("obsModal").classList.add("hidden");
}

async function submitObservation() {
  const reporter = document.getElementById("obsReporter").value;
  const note = document.getElementById("obsNote").value;
  const severity = document.getElementById("obsSeverity").value;

  if (!note) return;

  try {
    const res = await fetch(`/api/patients/${currentPatientId}/owner-obs`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ reporter, note, severity })
    });
    if (res.ok) {
      closeAddObservationModal();
      document.getElementById("obsNote").value = "";
      loadSelectedPatient();
    }
  } catch (err) {
    console.error("Failed to add observation:", err);
  }
}

function openUploadModal() {
  alert("Multimodal Upload Simulator: Select any feline DICOM or lab PDF to analyze with Gemini Vision.");
}

function exportClinicalReport() {
  window.print();
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
