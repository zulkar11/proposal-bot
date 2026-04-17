# POC Proposal: ProposalBot

## Project Title
**ProposalBot** — A multi-agent system where a user uploads a requirement document and gets a professional project proposal with estimation, research, risk analysis, and polished output — all through a clean web app.

---

## Objective

Demonstrate practical application of all four agentic AI design patterns learned in the course by building a working end-to-end system that solves a real workplace problem: turning raw requirements into structured project proposals.

---

## Agentic Patterns Used

| Pattern | Implementation |
|---|---|
| **Reflection** | Reviewer agent critiques the estimation, triggers revision if needed |
| **Tool Use** | PDF parsing via pdfplumber for document ingestion |
| **Planning** | Sequential 5-stage pipeline with progress tracking |
| **Multi-Agent** | 5 specialized agents coordinated via CrewAI |

---

## Scope

### Phase 1 — POC (In Scope)

| Feature | Justification |
|---|---|
| PDF + Text input (tabs) | Real-world flexibility |
| 5-agent pipeline (sequential) | Core of the POC |
| Real-time stage progress (polling) | UX matters in a demo |
| Individual agent output panels | Shows agentic thinking |
| Final proposal in Markdown render | Professional output |
| Copy to clipboard | Practical utility |
| PDF download of final proposal | Client-ready deliverable |
| Dark-themed responsive UI | Clean presentation |
| Error handling & edge cases | Production-readiness |

### Phase 2 — Future Enhancements (Out of Scope)

| Feature | Why Deferred |
|---|---|
| Proposal history (MongoDB) | Adds infra complexity |
| Web search (Serper API) | Extra cost + API key management |
| WebSocket/SSE streaming | Polling is simpler & sufficient |
| Edit/regenerate individual sections | Too much complexity for POC |
| User authentication | Not needed for POC |
| DOCX parsing | PDF + text is sufficient |
| Multi-language output | English only for POC |
| Comparing multiple proposals | Phase 2 feature |
| Cloud deployment (Vercel/Railway) | Local-only for POC |

---

## How It Works (User Flow)

```
1. User opens the web app
2. Uploads a PDF or pastes requirement text
3. Clicks "Generate Proposal"
4. Watches real-time progress as each agent completes its stage
5. Views individual agent outputs (analysis, research, estimation, review)
6. Reads the final polished proposal in rendered Markdown
7. Downloads as PDF or copies to clipboard
```

---

## Technical Details

- [Architecture & Tech Stack →](architecture.md)
- [API Design →](api-design.md)
- [Agent Pipeline & Reflection Logic →](agent-pipeline.md)
