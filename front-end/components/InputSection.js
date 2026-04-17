"use client";

import { useState, useRef } from "react";

export default function InputSection({ onSubmit, disabled }) {
  const [mode, setMode] = useState("text");
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  function handleSubmit(e) {
    e.preventDefault();
    if (disabled) return;
    onSubmit({ file: mode === "file" ? file : null, text: mode === "text" ? text : "" });
  }

  function handleDrag(e) {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else {
      setDragActive(false);
    }
  }

  function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files?.[0]) {
      setFile(e.dataTransfer.files[0]);
      setMode("file");
    }
  }

  function handleFileChange(e) {
    if (e.target.files?.[0]) {
      setFile(e.target.files[0]);
    }
  }

  const canSubmit = !disabled && ((mode === "text" && text.trim()) || (mode === "file" && file));

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* Tab switcher */}
      <div className="flex rounded-lg bg-[var(--surface)] p-1">
        {[
          { key: "text", label: "Paste Text", icon: (
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
              <polyline points="14 2 14 8 20 8" />
              <line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" /><line x1="10" y1="9" x2="8" y2="9" />
            </svg>
          )},
          { key: "file", label: "Upload PDF", icon: (
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="17 8 12 3 7 8" /><line x1="12" y1="3" x2="12" y2="15" />
            </svg>
          )},
        ].map((tab) => (
          <button
            key={tab.key}
            type="button"
            onClick={() => setMode(tab.key)}
            className={`flex flex-1 items-center justify-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition-all ${
              mode === tab.key
                ? "bg-[var(--background)] text-[var(--foreground)] shadow-sm"
                : "text-[var(--muted)] hover:text-[var(--foreground)]"
            }`}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </div>

      {/* Text input */}
      {mode === "text" && (
        <div className="relative">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste your requirement document here..."
            rows={7}
            disabled={disabled}
            className="w-full resize-none rounded-lg border border-[var(--border)] bg-[var(--surface)] px-4 py-3 text-sm text-[var(--foreground)] placeholder-[var(--muted)] transition-colors focus:border-indigo-500/50 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 disabled:cursor-not-allowed disabled:opacity-50"
          />
          {text.length > 0 && (
            <span className="absolute bottom-3 right-3 text-[10px] tabular-nums text-[var(--muted)]">
              {text.length.toLocaleString()} chars
            </span>
          )}
        </div>
      )}

      {/* File input */}
      {mode === "file" && (
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`group flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed px-6 py-12 transition-all ${
            dragActive
              ? "border-indigo-500 bg-indigo-500/5"
              : file
                ? "border-emerald-500/50 bg-emerald-500/5"
                : "border-[var(--border)] hover:border-[var(--muted)] hover:bg-[var(--surface)]"
          } ${disabled ? "cursor-not-allowed opacity-50" : ""}`}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            disabled={disabled}
            className="hidden"
          />
          {file ? (
            <div className="flex flex-col items-center gap-2">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-500/10">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-emerald-500">
                  <polyline points="20 6 9 17 4 12" />
                </svg>
              </div>
              <p className="text-sm font-medium text-[var(--foreground)]">{file.name}</p>
              <p className="text-xs text-[var(--muted)]">{(file.size / 1024).toFixed(0)} KB &middot; Click to replace</p>
            </div>
          ) : (
            <div className="flex flex-col items-center gap-2">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[var(--surface)] transition-colors group-hover:bg-indigo-500/10">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="text-[var(--muted)] transition-colors group-hover:text-indigo-500">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="17 8 12 3 7 8" /><line x1="12" y1="3" x2="12" y2="15" />
                </svg>
              </div>
              <p className="text-sm font-medium text-[var(--foreground)]">Drop a PDF here or click to browse</p>
              <p className="text-xs text-[var(--muted)]">PDF files only, up to 10MB</p>
            </div>
          )}
        </div>
      )}

      {/* Submit */}
      <button
        type="submit"
        disabled={!canSubmit}
        className={`inline-flex w-full items-center justify-center gap-2 rounded-lg px-6 py-2.5 text-sm font-semibold transition-all ${
          canSubmit
            ? "bg-gradient-to-r from-indigo-500 to-violet-600 text-white shadow-md shadow-indigo-500/25 hover:shadow-lg hover:shadow-indigo-500/30 active:scale-[0.98]"
            : "cursor-not-allowed bg-[var(--surface)] text-[var(--muted)]"
        }`}
      >
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
        </svg>
        {disabled ? "Generating..." : "Generate Proposal"}
      </button>
    </form>
  );
}
