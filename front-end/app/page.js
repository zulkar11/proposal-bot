"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import Header from "@/components/Header";
import InputSection from "@/components/InputSection";
import ProgressTracker from "@/components/ProgressTracker";
import AgentOutputCard from "@/components/AgentOutputCard";
import ProposalView from "@/components/ProposalView";
import { generateProposal, getProposal } from "@/lib/api";

const POLL_INTERVAL = 3000;

const FEATURES = [
  { icon: "1", title: "Analyze", desc: "Parse & structure requirements" },
  { icon: "2", title: "Research", desc: "Recommend technology stack" },
  { icon: "3", title: "Estimate", desc: "Effort, timeline & team sizing" },
  { icon: "4", title: "Review", desc: "Quality check with reflection" },
  { icon: "5", title: "Write", desc: "Polished client-ready proposal" },
];

export default function Home() {
  const [jobData, setJobData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const pollingRef = useRef(null);

  const stopPolling = useCallback(() => {
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
      pollingRef.current = null;
    }
  }, []);

  const poll = useCallback(
    async (jobId) => {
      try {
        const data = await getProposal(jobId);
        setJobData(data);
        setError(null);
        if (data.status === "completed" || data.status === "failed") {
          stopPolling();
          setLoading(false);
        }
      } catch (err) {
        setError(err.message);
        stopPolling();
        setLoading(false);
      }
    },
    [stopPolling]
  );

  useEffect(() => {
    return () => stopPolling();
  }, [stopPolling]);

  async function handleSubmit({ file, text }) {
    setError(null);
    setJobData(null);
    setLoading(true);
    try {
      const res = await generateProposal({ file, text });
      setJobData({ job_id: res.job_id, status: res.status });
      pollingRef.current = setInterval(() => poll(res.job_id), POLL_INTERVAL);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  }

  function handleReset() {
    stopPolling();
    setJobData(null);
    setError(null);
    setLoading(false);
  }

  const isDone = jobData?.status === "completed";
  const isFailed = jobData?.status === "failed";
  const isProcessing = loading && !isDone && !isFailed;

  return (
    <div className="flex min-h-screen flex-col bg-[var(--background)]">
      <Header />

      <main className="flex-1">
        {/* ── Landing / Input State ── */}
        {!jobData && (
          <div className="animate-fade-in">
            {/* Hero */}
            <div className="border-b border-[var(--border)] bg-[var(--surface)]">
              <div className="mx-auto max-w-6xl px-6 py-16 text-center">
                <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--background)] px-3 py-1 text-xs font-medium text-[var(--muted)]">
                  <span className="h-1.5 w-1.5 rounded-full bg-indigo-500" />
                  Powered by 5 AI Agents
                </div>
                <h2 className="mx-auto max-w-2xl text-3xl font-bold tracking-tight text-[var(--foreground)] sm:text-4xl">
                  Turn requirements into
                  <span className="bg-gradient-to-r from-indigo-500 to-violet-500 bg-clip-text text-transparent"> professional proposals</span>
                </h2>
                <p className="mx-auto mt-4 max-w-xl text-sm leading-relaxed text-[var(--muted)]">
                  Upload a PDF or paste requirement text. Our multi-agent pipeline will analyze,
                  research, estimate, review, and write a polished project proposal.
                </p>

                {/* Pipeline steps visual */}
                <div className="mx-auto mt-10 flex max-w-2xl items-center justify-between">
                  {FEATURES.map((f, i) => (
                    <div key={f.title} className="flex items-center">
                      <div className="flex flex-col items-center gap-1.5">
                        <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-[var(--border)] bg-[var(--background)] text-xs font-bold text-[var(--muted)]">
                          {f.icon}
                        </div>
                        <span className="text-[11px] font-semibold text-[var(--foreground)]">{f.title}</span>
                        <span className="text-[10px] text-[var(--muted)] hidden sm:block">{f.desc}</span>
                      </div>
                      {i < FEATURES.length - 1 && (
                        <div className="mx-2 h-px w-6 bg-[var(--border)] sm:mx-3 sm:w-10" />
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Input Card */}
            <div className="mx-auto max-w-2xl px-6 py-10">
              <div className="rounded-xl border border-[var(--border)] bg-[var(--background)] p-6 shadow-sm">
                <InputSection onSubmit={handleSubmit} disabled={loading} />
              </div>
              {error && (
                <div className="mt-4 flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/50 dark:bg-red-950/20 dark:text-red-400">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="shrink-0">
                    <circle cx="12" cy="12" r="10" /><line x1="15" y1="9" x2="9" y2="15" /><line x1="9" y1="9" x2="15" y2="15" />
                  </svg>
                  {error}
                </div>
              )}
            </div>
          </div>
        )}

        {/* ── Pipeline / Results State ── */}
        {jobData && (
          <div className="animate-fade-in mx-auto max-w-6xl px-6 py-8">
            {/* Top bar */}
            <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex items-center gap-3">
                <ProgressTracker
                  currentStage={jobData.current_stage || jobData.status}
                  stagesCompleted={jobData.stages_completed || []}
                />
              </div>
              <div className="flex items-center gap-3">
                {isProcessing && jobData.metadata?.elapsed_seconds != null && (
                  <span className="flex items-center gap-1.5 rounded-full bg-[var(--surface)] px-3 py-1 text-xs font-medium tabular-nums text-[var(--muted)]">
                    <span className="h-1.5 w-1.5 animate-pulse-dot rounded-full bg-indigo-500" />
                    {jobData.metadata.elapsed_seconds}s
                  </span>
                )}
                <button
                  type="button"
                  onClick={handleReset}
                  className="inline-flex items-center gap-1.5 rounded-lg border border-[var(--border)] bg-[var(--background)] px-3.5 py-1.5 text-xs font-medium text-[var(--muted)] transition-colors hover:bg-[var(--surface)] hover:text-[var(--foreground)]"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="1 4 1 10 7 10" /><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10" />
                  </svg>
                  New
                </button>
              </div>
            </div>

            {/* Error */}
            {isFailed && (
              <div className="mb-6 flex items-start gap-3 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/50 dark:bg-red-950/20 dark:text-red-400">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="mt-0.5 shrink-0">
                  <circle cx="12" cy="12" r="10" /><line x1="15" y1="9" x2="9" y2="15" /><line x1="9" y1="9" x2="15" y2="15" />
                </svg>
                <div>
                  <p className="font-medium">Pipeline failed</p>
                  <p className="mt-0.5 text-xs opacity-80">{jobData.metadata?.error || "Unknown error. Please try again."}</p>
                </div>
              </div>
            )}

            {/* Two-column layout: Agent outputs + Final proposal */}
            <div className="grid gap-6 lg:grid-cols-[340px_1fr]">
              {/* Left: Agent output cards */}
              {jobData.agent_outputs && (
                <div className="space-y-2">
                  <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">
                    Agent Outputs
                  </h3>
                  {Object.entries(jobData.agent_outputs).map(
                    ([agent, output]) => (
                      <AgentOutputCard
                        key={agent}
                        agentName={agent}
                        output={output}
                        isActive={
                          jobData.current_stage ===
                          {
                            analyzer: "analyzing",
                            researcher: "researching",
                            estimator: "estimating",
                            reviewer: "reviewing",
                            writer: "writing",
                          }[agent]
                        }
                      />
                    )
                  )}
                </div>
              )}

              {/* Right: Final proposal or loading placeholder */}
              <div className="min-w-0">
                {isDone && jobData.final_proposal ? (
                  <div>
                    <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">
                      Generated Proposal
                    </h3>
                    <ProposalView proposal={jobData.final_proposal} />
                  </div>
                ) : isProcessing ? (
                  <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-[var(--border)] bg-[var(--surface)] py-20">
                    <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-indigo-500/10">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="animate-spin text-indigo-500">
                        <path d="M21 12a9 9 0 1 1-6.219-8.56" />
                      </svg>
                    </div>
                    <p className="text-sm font-medium text-[var(--foreground)]">Generating proposal...</p>
                    <p className="mt-1 text-xs text-[var(--muted)]">This usually takes 1-3 minutes</p>
                  </div>
                ) : null}
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="border-t border-[var(--border)]">
        <div className="mx-auto flex h-12 max-w-6xl items-center justify-between px-6">
          <p className="text-[11px] text-[var(--muted)]">
            ProposalBot &mdash; Multi-Agent AI Proposal Generator
          </p>
          <p className="text-[11px] text-[var(--muted)]">
            CrewAI + z.ai GLM
          </p>
        </div>
      </footer>
    </div>
  );
}
