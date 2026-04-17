"use client";

import { useRef, useState } from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function ProposalView({ proposal }) {
  const contentRef = useRef(null);
  const [copied, setCopied] = useState(false);
  const [downloading, setDownloading] = useState(false);

  if (!proposal) return null;

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(proposal);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      const textarea = document.createElement("textarea");
      textarea.value = proposal;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      document.body.removeChild(textarea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }

  async function handleDownloadPdf() {
    setDownloading(true);
    try {
      const html2pdf = (await import("html2pdf.js")).default;
      const element = contentRef.current;
      html2pdf()
        .set({
          margin: [10, 10, 10, 10],
          filename: "proposal.pdf",
          image: { type: "jpeg", quality: 0.98 },
          html2canvas: { scale: 2 },
          jsPDF: { unit: "mm", format: "a4", orientation: "portrait" },
        })
        .from(element)
        .save();
    } catch (err) {
      console.error("PDF generation failed:", err);
    } finally {
      setDownloading(false);
    }
  }

  return (
    <div className="space-y-3">
      {/* Action bar */}
      <div className="flex items-center gap-2">
        <button
          type="button"
          onClick={handleCopy}
          className={`inline-flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-xs font-medium transition-all ${
            copied
              ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400"
              : "border-[var(--border)] bg-[var(--background)] text-[var(--muted)] hover:bg-[var(--surface)] hover:text-[var(--foreground)]"
          }`}
        >
          {copied ? (
            <>
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="20 6 9 17 4 12" />
              </svg>
              Copied!
            </>
          ) : (
            <>
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
              </svg>
              Copy Markdown
            </>
          )}
        </button>

        <button
          type="button"
          onClick={handleDownloadPdf}
          disabled={downloading}
          className="inline-flex items-center gap-1.5 rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-1.5 text-xs font-medium text-[var(--muted)] transition-colors hover:bg-[var(--surface)] hover:text-[var(--foreground)] disabled:opacity-50"
        >
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="7 10 12 15 17 10" />
            <line x1="12" y1="15" x2="12" y2="3" />
          </svg>
          {downloading ? "Generating..." : "Download PDF"}
        </button>
      </div>

      {/* Markdown content */}
      <div
        ref={contentRef}
        className="prose prose-sm max-w-none rounded-xl border border-[var(--border)] bg-[var(--background)] px-8 py-6 text-[var(--foreground)] shadow-sm"
      >
        <Markdown remarkPlugins={[remarkGfm]}>{proposal}</Markdown>
      </div>
    </div>
  );
}
