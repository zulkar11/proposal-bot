const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function generateProposal({ file, text }) {
  const formData = new FormData();
  if (file) {
    formData.append("file", file);
  }
  if (text) {
    formData.append("text", text);
  }

  const res = await fetch(`${API_BASE}/api/proposals/generate`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }

  return res.json();
}

export async function getProposal(jobId) {
  const res = await fetch(`${API_BASE}/api/proposals/${jobId}`);

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }

  return res.json();
}

export const STAGES = [
  { key: "analyzing", label: "Analyzing", agent: "analyzer", icon: "1" },
  { key: "researching", label: "Researching", agent: "researcher", icon: "2" },
  { key: "estimating", label: "Estimating", agent: "estimator", icon: "3" },
  { key: "reviewing", label: "Reviewing", agent: "reviewer", icon: "4" },
  { key: "writing", label: "Writing", agent: "writer", icon: "5" },
];
