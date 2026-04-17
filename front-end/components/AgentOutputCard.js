"use client";

import { useState } from "react";

const AGENT_META = {
  analyzer: { label: "Requirement Analysis", icon: "🔍", color: "indigo" },
  researcher: { label: "Technology Research", icon: "🔬", color: "violet" },
  estimator: { label: "Project Estimation", icon: "📊", color: "amber" },
  reviewer: { label: "Review Summary", icon: "✅", color: "emerald" },
  writer: { label: "Final Proposal", icon: "✍️", color: "blue" },
};

export default function AgentOutputCard({ agentName, output, isActive }) {
  const [expanded, setExpanded] = useState(false);

  if (!output) return null;

  const meta = AGENT_META[agentName] || { label: agentName, icon: "⚙️", color: "zinc" };

  return (
    <div
      className={`rounded-lg border transition-all ${
        isActive
          ? "border-indigo-500/30 bg-indigo-500/5 shadow-sm"
          : "border-[var(--border)] bg-[var(--background)] hover:border-[var(--muted)]/30"
      }`}
    >
      <button
        type="button"
        onClick={() => setExpanded(!expanded)}
        className="flex w-full items-center justify-between px-3.5 py-2.5 text-left"
      >
        <div className="flex items-center gap-2.5">
          <span className="text-sm">{meta.icon}</span>
          <span className="text-xs font-semibold text-[var(--foreground)]">
            {meta.label}
          </span>
          {isActive && (
            <span className="h-1.5 w-1.5 animate-pulse-dot rounded-full bg-indigo-500" />
          )}
        </div>
        <svg
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className={`text-[var(--muted)] transition-transform duration-200 ${
            expanded ? "rotate-180" : ""
          }`}
        >
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </button>

      {expanded && (
        <div className="animate-slide-down border-t border-[var(--border)] px-3.5 py-3">
          <pre className="whitespace-pre-wrap break-words font-mono text-[11px] leading-relaxed text-[var(--muted)]">
            {output}
          </pre>
        </div>
      )}
    </div>
  );
}
