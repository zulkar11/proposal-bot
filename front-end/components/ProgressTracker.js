"use client";

import { STAGES } from "@/lib/api";

export default function ProgressTracker({ currentStage, stagesCompleted }) {
  const completed = new Set(stagesCompleted);
  const currentIndex = STAGES.findIndex((s) => s.key === currentStage);
  const isComplete = currentStage === "completed";
  const isFailed = currentStage === "failed";

  return (
    <div className="flex flex-wrap items-center gap-2">
      {STAGES.map((stage, i) => {
        const done = completed.has(stage.key);
        const active = stage.key === currentStage;

        return (
          <div key={stage.key} className="flex items-center gap-2">
            <div
              className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-medium transition-all ${
                done || isComplete
                  ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400"
                  : active
                    ? "bg-indigo-500/10 text-indigo-600 dark:text-indigo-400"
                    : isFailed
                      ? "bg-red-500/10 text-red-500"
                      : "bg-[var(--surface)] text-[var(--muted)]"
              }`}
            >
              {done || isComplete ? (
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="20 6 9 17 4 12" />
                </svg>
              ) : active ? (
                <span className="h-1.5 w-1.5 animate-pulse-dot rounded-full bg-indigo-500" />
              ) : (
                <span className="text-[10px] opacity-60">{stage.icon}</span>
              )}
              {stage.label}
            </div>

            {i < STAGES.length - 1 && (
              <div className={`h-px w-3 ${done || isComplete ? "bg-emerald-500/30" : "bg-[var(--border)]"}`} />
            )}
          </div>
        );
      })}

      {/* Status badge */}
      {isComplete && (
        <span className="ml-2 rounded-full bg-emerald-500/10 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
          Done
        </span>
      )}
      {isFailed && (
        <span className="ml-2 rounded-full bg-red-500/10 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-red-500">
          Failed
        </span>
      )}
    </div>
  );
}
