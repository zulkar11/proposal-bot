# Architecture & Tech Stack

## System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Next.js Frontend                       │
│                                                          │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │  Upload   │  │  Progress    │  │  Results           │  │
│  │  (PDF/    │  │  Tracker     │  │  • Agent outputs   │  │
│  │   Text)   │  │  (Polling)   │  │  • Final proposal  │  │
│  │           │  │              │  │  • PDF download     │  │
│  └──────────┘  └──────────────┘  └───────────────────┘  │
└──────────────────────┬───────────────────────────────────┘
                       │  REST API
                       ▼
┌──────────────────────────────────────────────────────────┐
│                  FastAPI Backend                          │
│                                                          │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │  PDF       │  │  CrewAI      │  │  In-Memory       │  │
│  │  Parser    │  │  Pipeline    │  │  Job Store       │  │
│  │            │  │              │  │                   │  │
│  │ pdfplumber │  │ 5 Agents     │  │ (dict-based)     │  │
│  │            │  │ Sequential   │  │                   │  │
│  └────────────┘  └──────┬───────┘  └─────────────────┘  │
└──────────────────────────┼───────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│                    CrewAI Agents                          │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌────────────┐             │
│  │ Analyzer │→ │ Research │→ │ Estimation │             │
│  └──────────┘  └──────────┘  └─────┬──────┘             │
│                                     │                    │
│                              ┌──────▼───────┐            │
│                              │  Reflection  │            │
│                              │              │            │
│                              │  ┌───────┐   │            │
│                              │  │Revise?│──→ Back to     │
│                              │  │  🔄   │   Estimation   │
│                              │  └───┬───┘                │
│                              │      │ ✅                  │
│                              └──────┼───────┘            │
│                                     ▼                    │
│                              ┌──────────────┐            │
│                              │   Proposal   │            │
│                              │   Writer     │            │
│                              └──────────────┘            │
└──────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Next.js 16 + Tailwind CSS 4 | SaaS-style web UI |
| Markdown Render | react-markdown + remark-gfm | Render proposals with tables |
| PDF Export | html2pdf.js | Client-side PDF download |
| Backend | Python FastAPI | REST API server |
| Agents | CrewAI 0.86 | Multi-agent orchestration |
| LLM | z.ai GLM-5.1 / OpenAI (via LiteLLM) | Language model backend |
| PDF Parse | pdfplumber | Extract text from uploaded PDFs |
| Job Storage | In-memory dict | Track pipeline status (no DB) |
| Package Mgmt | uv | Fast Python dependency management |
| Deployment | Docker Compose | Local setup with one command |

---

## Project Structure

```
proposal_bot/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app + routes
│   │   ├── config.py            # Environment config + LLM setup
│   │   ├── models.py            # Pydantic request/response models
│   │   │
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── analyzer.py      # Requirement Analyzer agent
│   │   │   ├── researcher.py    # Technology Researcher agent
│   │   │   ├── estimator.py     # Project Estimator agent
│   │   │   ├── reviewer.py      # Estimation Reviewer (Reflection agent)
│   │   │   └── writer.py        # Proposal Writer agent
│   │   │
│   │   ├── crew/
│   │   │   ├── __init__.py
│   │   │   ├── tasks.py         # Task definitions with context passing
│   │   │   └── pipeline.py      # Pipeline orchestration + reflection loop
│   │   │
│   │   ├── services/
│   │   │   ├── pdf_parser.py    # pdfplumber text extraction
│   │   │   └── job_store.py     # In-memory job status tracking
│   │   │
│   │   └── utils/
│   │       └── helpers.py       # Token truncation, sanitization
│   │
│   ├── pyproject.toml           # Python dependencies (managed by uv)
│   ├── uv.lock
│   ├── .env.example
│   └── Dockerfile
│
├── front-end/
│   ├── app/
│   │   ├── page.js              # Main page + polling logic
│   │   ├── layout.js            # Root layout + Geist fonts
│   │   └── globals.css          # Design system + animations
│   │
│   ├── components/
│   │   ├── Header.js            # SaaS header with branding
│   │   ├── InputSection.js      # Text/PDF input tabs
│   │   ├── ProgressTracker.js   # Pipeline progress pills
│   │   ├── AgentOutputCard.js   # Expandable agent output accordion
│   │   └── ProposalView.js      # Markdown render + PDF download
│   │
│   ├── lib/
│   │   └── api.js               # API client + stage definitions
│   │
│   ├── package.json
│   └── Dockerfile
│
├── sample_docs/
│   ├── ecommerce_requirements.txt
│   └── saas_platform_brief.txt
│
├── docs/
│   ├── assignment.md            # Course assignment submission
│   ├── poc-proposal.md          # POC scope & features
│   ├── architecture.md          # This file
│   ├── api-design.md            # API endpoints & models
│   └── agent-pipeline.md        # Agent roles & reflection logic
│
├── script/
│   ├── generate_report.py       # PDF report generator
│   └── front_end_screenshort.png
│
├── docker-compose.yml
└── README.md
```

---

## Key Design Decisions

| Decision | Rationale |
|---|---|
| **In-memory job store** instead of MongoDB | POC doesn't need persistence; removes infra dependency |
| **Polling (3s)** instead of WebSocket/SSE | Simpler to implement; sufficient for LLM pipeline stages that take 10-60s each |
| **CrewAI** for agent orchestration | Aligns with course concepts; handles sequential task pipelines well |
| **LiteLLM** wrapper for LLM | Allows easy switching between z.ai, OpenAI, Gemini, local models without code changes |
| **uv** for Python package management | Faster than pip; lockfile ensures reproducible builds |
| **Docker Compose** for local setup | One-command setup; no cloud dependency for demo |
| **html2pdf.js** (client-side) | No server-side PDF generation complexity; simple and reliable |
