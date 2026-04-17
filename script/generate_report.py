"""
Generate Course Assignment PDF Report
DeepLearning.AI — Agentic AI Course
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable, KeepTogether, Preformatted,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

# ── Colors ──
PRIMARY = HexColor("#1F2937")  # near-black
DARK = HexColor("#111827")
GRAY = HexColor("#6B7280")
LIGHT_BG = HexColor("#F3F4F6")
BORDER = HexColor("#D1D5DB")
WHITE = HexColor("#FFFFFF")
ACCENT_GREEN = HexColor("#059669")

# ── Styles ──
styles = {}

styles["title"] = ParagraphStyle(
    "title", fontName="Helvetica-Bold", fontSize=22, leading=28,
    textColor=DARK, alignment=TA_CENTER, spaceAfter=4,
)
styles["subtitle"] = ParagraphStyle(
    "subtitle", fontName="Helvetica", fontSize=11, leading=14,
    textColor=GRAY, alignment=TA_CENTER, spaceAfter=2,
)
styles["meta"] = ParagraphStyle(
    "meta", fontName="Helvetica", fontSize=9, leading=12,
    textColor=GRAY, alignment=TA_CENTER, spaceAfter=6,
)
styles["h1"] = ParagraphStyle(
    "h1", fontName="Helvetica-Bold", fontSize=15, leading=20,
    textColor=DARK, spaceBefore=18, spaceAfter=8,
)
styles["h2"] = ParagraphStyle(
    "h2", fontName="Helvetica-Bold", fontSize=12, leading=16,
    textColor=DARK, spaceBefore=12, spaceAfter=6,
)
styles["body"] = ParagraphStyle(
    "body", fontName="Helvetica", fontSize=10, leading=15,
    textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=6,
)
styles["bullet"] = ParagraphStyle(
    "bullet", fontName="Helvetica", fontSize=10, leading=15,
    textColor=DARK, leftIndent=18, bulletIndent=6, spaceAfter=4,
    alignment=TA_JUSTIFY,
)
styles["bold_bullet"] = ParagraphStyle(
    "bold_bullet", fontName="Helvetica", fontSize=10, leading=15,
    textColor=DARK, leftIndent=18, bulletIndent=6, spaceAfter=4,
    alignment=TA_JUSTIFY,
)
styles["caption"] = ParagraphStyle(
    "caption", fontName="Helvetica-Oblique", fontSize=8.5, leading=11,
    textColor=GRAY, alignment=TA_CENTER, spaceBefore=4, spaceAfter=10,
)
styles["footer"] = ParagraphStyle(
    "footer", fontName="Helvetica", fontSize=7.5, leading=10,
    textColor=GRAY, alignment=TA_CENTER,
)
styles["code"] = ParagraphStyle(
    "code", fontName="Courier", fontSize=7, leading=10,
    textColor=DARK, leftIndent=0, rightIndent=0,
)
styles["code_title"] = ParagraphStyle(
    "code_title", fontName="Helvetica-Bold", fontSize=9, leading=12,
    textColor=WHITE, alignment=TA_LEFT, leftIndent=8,
)
styles["table_cell"] = ParagraphStyle(
    "table_cell", fontName="Helvetica", fontSize=8.5, leading=12,
    textColor=DARK,
)
styles["table_cell_bold"] = ParagraphStyle(
    "table_cell_bold", fontName="Helvetica-Bold", fontSize=8.5, leading=12,
    textColor=DARK,
)
styles["table_header"] = ParagraphStyle(
    "table_header", fontName="Helvetica-Bold", fontSize=8.5, leading=12,
    textColor=WHITE,
)


def make_table(headers, rows, col_widths=None):
    """Create a styled table with Paragraph-wrapped cells to prevent overflow."""
    # Wrap headers in Paragraph
    header_row = [Paragraph(h, styles["table_header"]) for h in headers]

    # Wrap every cell in Paragraph for auto line-wrapping
    wrapped_rows = []
    for row in rows:
        wrapped = []
        for i, cell in enumerate(row):
            if i == 0:
                wrapped.append(Paragraph(str(cell), styles["table_cell_bold"]))
            else:
                wrapped.append(Paragraph(str(cell), styles["table_cell"]))
        wrapped_rows.append(wrapped)

    data = [header_row] + wrapped_rows
    w = col_widths or [None] * len(headers)
    t = Table(data, colWidths=w, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("LEADING", (0, 0), (-1, -1), 13),
        ("BACKGROUND", (0, 1), (-1, -1), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def make_code_block(title, code_text, content_width):
    """Create a styled code block with a dark header bar and light code area."""
    elements = []
    # Title bar
    title_data = [[Paragraph(title, styles["code_title"])]]
    title_table = Table(title_data, colWidths=[content_width])
    title_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#1E1E2E")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    elements.append(title_table)

    # Code body
    code_style = ParagraphStyle(
        "code_inner", fontName="Courier", fontSize=6.8, leading=9.5,
        textColor=HexColor("#D4D4D8"), leftIndent=6,
    )
    # Escape XML-sensitive chars and preserve newlines
    safe = (code_text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br/>"))
    code_para = Paragraph(safe, code_style)
    code_data = [[code_para]]
    code_table = Table(code_data, colWidths=[content_width])
    code_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#1E1E2E")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    elements.append(code_table)
    return elements


def add_page_number(canvas, doc):
    """Footer with page number."""
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(
        A4[0] / 2, 15 * mm,
        f"Zulkar Nayin (11374) — DeepLearning.AI Agentic AI Course Report — Page {doc.page}"
    )
    canvas.restoreState()


def build_pdf():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)
    output_path = os.path.join(project_root, "Agentic_AI_Course_Report_Zulkar_Nayin.pdf")
    screenshot_path = os.path.join(base_dir, "front_end_screenshort.png")

    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=22 * mm, bottomMargin=22 * mm,
    )
    content_width = A4[0] - 40 * mm
    story = []

    # ════════════════════════════════════════
    # COVER / HEADER
    # ════════════════════════════════════════
    story.append(Spacer(1, 30))
    story.append(Paragraph("Agentic AI — Course Report", styles["title"]))
    story.append(Paragraph("DeepLearning.AI Course by Andrew Ng", styles["subtitle"]))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="40%", thickness=1.5, color=PRIMARY, spaceAfter=10))
    story.append(Paragraph(
        "<b>Name:</b> Zulkar Nayin &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>Employee ID:</b> 11374 &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>Email:</b> zulkar.nayin@bjitgroup.com",
        styles["meta"],
    ))
    story.append(Paragraph(
        "<b>Organization:</b> BJIT Limited &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>Date:</b> April 2026 &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<link href='https://github.com/zulkar11/proposal-bot'>"
        "<u>github.com/zulkar11/proposal-bot</u></link>",
        styles["meta"],
    ))
    story.append(Spacer(1, 14))

    # ════════════════════════════════════════
    # 1. COURSE SUMMARY
    # ════════════════════════════════════════
    story.append(Paragraph("1. Course Summary", styles["h1"]))
    story.append(Paragraph(
        "<b>Agentic AI</b> by Andrew Ng (DeepLearning.AI) is a 5-module course that teaches "
        "how to build AI systems that go beyond single prompts — systems that can autonomously "
        "plan, use tools, coordinate multiple agents, and self-correct through reflection. "
        "The course is structured around <b>four core design patterns</b>:",
        styles["body"],
    ))
    patterns = [
        ("<b>Reflection</b> — AI critiques and iteratively improves its own outputs", "bullet"),
        ("<b>Tool Use</b> — Connecting AI to databases, APIs, and code execution via function calling and MCP", "bullet"),
        ("<b>Planning</b> — Breaking complex tasks into executable steps with adaptive replanning", "bullet"),
        ("<b>Multi-Agent Systems</b> — Coordinating specialized AI agents to solve complex problems together", "bullet"),
    ]
    for text, _ in patterns:
        story.append(Paragraph(text, styles["bullet"], bulletText="•"))
    story.append(Paragraph(
        "The capstone project involves building a complete autonomous research agent "
        "that can gather information, analyze it, and produce a structured report.",
        styles["body"],
    ))

    # ════════════════════════════════════════
    # 2. KEY LEARNINGS
    # ════════════════════════════════════════
    story.append(Paragraph("2. What I Learned (Most Important)", styles["h1"]))

    learnings = [
        ("<b>Single prompts are not enough for real tasks</b> — Before this course, I mostly used "
         "ChatGPT/Copilot with one-shot prompts. The biggest eye-opener was that breaking a task "
         "into multiple agent steps with feedback loops produces dramatically better results."),
        ("<b>Reflection is the simplest and most powerful pattern</b> — Just having an LLM review "
         "its own output and try again catches most quality issues. I immediately saw how this "
         "applies to code review, writing, and even test generation in my daily work."),
        ("<b>LLMs can interact with real systems, not just generate text</b> — Function calling "
         "and MCP let agents read databases, call APIs, parse files, and execute code. This "
         "changes what's possible — AI can now do actual work, not just suggest it."),
        ("<b>Giving agents specialized roles works better than one big prompt</b> — When I built "
         "the POC, splitting the work across 5 focused agents (analyzer, researcher, estimator, "
         "reviewer, writer) produced far better proposals than asking one agent to do everything."),
        ("<b>You need to test agentic systems differently</b> — LLM outputs are non-deterministic. "
         "The course taught me to build evaluation frameworks and do systematic error analysis — "
         "something I hadn't considered before for AI-powered features."),
    ]
    for i, text in enumerate(learnings, 1):
        story.append(Paragraph(f"{i}. {text}", styles["bullet"], bulletText=""))

    # ════════════════════════════════════════
    # 3. APPLICATION TO WORK
    # ════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("3. How This Knowledge Can Be Used in My Work at BJIT", styles["h1"]))
    story.append(Paragraph(
        "As a software engineer at BJIT Limited, I work on client projects that involve "
        "requirement analysis, development, code reviews, and documentation. Here are the "
        "specific areas where I can apply what I learned:",
        styles["body"],
    ))

    story.append(make_table(
        ["My Daily Activity", "Agentic Pattern", "How I Can Use It"],
        [
            ["Writing code", "Reflection",
             "Use AI to review my code, suggest improvements, and iterate — like having a tireless code reviewer available 24/7"],
            ["Project estimation", "Multi-Agent + Planning",
             "Automate requirement breakdown and effort estimation before submitting to leads — reduces back-and-forth"],
            ["Researching tech\nsolutions", "Tool Use",
             "Let agents search docs, compare libraries, and summarize findings — saves hours of manual research per sprint"],
            ["Writing docs &\nREADMEs", "Multi-Agent + Reflection",
             "Generate documentation from code, then have a second agent review for clarity and completeness"],
            ["Writing unit tests", "Tool Use + Reflection",
             "Generate test cases from code, run them, analyze failures, and fix — speeds up test coverage significantly"],
            ["Client emails &\nstatus reports", "Reflection",
             "Draft professional client communications with a quality-check loop — especially useful for non-native English"],
        ],
        col_widths=[90, 100, content_width - 190],
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "The most immediate win for me personally is applying the <b>reflection pattern</b> "
        "to code review and documentation — these are tasks I do every day, and even a simple "
        "\"generate then review\" loop with an LLM noticeably improves output quality.",
        styles["body"],
    ))

    # ════════════════════════════════════════
    # 4. POC PROPOSAL
    # ════════════════════════════════════════
    story.append(Paragraph("4. POC Proposal — ProposalBot", styles["h1"]))
    story.append(Paragraph(
        "<b>ProposalBot</b> is a multi-agent system where a user uploads a requirement document "
        "and gets a professional project proposal with estimation, research, risk analysis, and "
        "polished output — all through a clean web app. This POC directly demonstrates "
        "<b>all four agentic design patterns</b> from the course.",
        styles["body"],
    ))

    story.append(Paragraph("Agentic Patterns Demonstrated", styles["h2"]))
    story.append(make_table(
        ["Pattern", "Implementation in ProposalBot"],
        [
            ["Reflection", "Reviewer agent critiques the estimation, triggers revision if quality is insufficient"],
            ["Tool Use", "PDF parsing via pdfplumber for document ingestion"],
            ["Planning", "Sequential 5-stage pipeline with progress tracking and stage orchestration"],
            ["Multi-Agent", "5 specialized agents (Analyzer → Researcher → Estimator → Reviewer → Writer) coordinated via CrewAI"],
        ],
        col_widths=[90, content_width - 90],
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Architecture Overview", styles["h2"]))
    story.append(Paragraph(
        "The system uses a <b>Next.js</b> frontend with a <b>FastAPI</b> backend. "
        "The backend orchestrates <b>5 CrewAI agents</b> in a sequential pipeline with a "
        "reflection loop at the review stage. LLM calls go through <b>LiteLLM</b> for provider "
        "flexibility (currently using z.ai GLM-5.1). Job status is tracked in-memory and polled "
        "by the frontend every 3 seconds.",
        styles["body"],
    ))

    story.append(Paragraph("User Flow", styles["h2"]))
    flow_steps = [
        "User opens the web app and uploads a PDF or pastes requirement text",
        "Clicks 'Generate Proposal' — backend starts the 5-agent pipeline",
        "Frontend polls for progress; each agent's output appears as it completes",
        "Reviewer agent checks quality — if insufficient, estimation is revised (reflection loop)",
        "Final polished proposal is rendered in Markdown with tables and sections",
        "User can copy to clipboard or download as PDF",
    ]
    for i, step in enumerate(flow_steps, 1):
        story.append(Paragraph(f"{i}. {step}", styles["bullet"], bulletText=""))

    story.append(Paragraph("Tech Stack", styles["h2"]))
    story.append(make_table(
        ["Layer", "Technology", "Purpose"],
        [
            ["Frontend", "Next.js 16 + Tailwind CSS 4", "SaaS-quality web UI"],
            ["Markdown", "react-markdown + remark-gfm", "Render proposal with tables"],
            ["PDF Export", "html2pdf.js", "Client-side PDF download"],
            ["Backend", "Python FastAPI", "REST API server"],
            ["Agents", "CrewAI 0.86", "Multi-agent orchestration"],
            ["LLM", "z.ai GLM-5.1 (via LiteLLM)", "Language model backend"],
            ["PDF Parse", "pdfplumber", "Extract text from uploaded PDFs"],
            ["Package Mgmt", "uv", "Fast Python package management"],
            ["Deployment", "Docker Compose", "Local setup with one command"],
        ],
        col_widths=[70, 120, content_width - 190],
    ))

    # ── Screenshot ──
    if os.path.exists(screenshot_path):
        story.append(Spacer(1, 10))
        story.append(Paragraph("Frontend Screenshot", styles["h2"]))
        img = Image(screenshot_path)
        # Scale to fit content width while maintaining aspect ratio
        aspect = img.imageWidth / img.imageHeight
        img_width = min(content_width, 160 * mm)
        img_height = img_width / aspect
        img = Image(screenshot_path, width=img_width, height=img_height)
        story.append(img)
        story.append(Paragraph(
            "Figure 1: ProposalBot landing page — 5-agent pipeline visualization with text/PDF input",
            styles["caption"],
        ))

    # ════════════════════════════════════════
    # CODE REFERENCES — Major Flow
    # ════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("Code References — Major Flow", styles["h1"]))
    story.append(Paragraph(
        "Below are the key code snippets that demonstrate the major architectural "
        "components of ProposalBot. These illustrate how the agentic design patterns "
        "are implemented in practice.",
        styles["body"],
    ))

    # ── Code 1: Agent Definition (Reflection Pattern) ──
    story.append(Spacer(1, 8))
    story.append(Paragraph("Agent Definition — Analyzer &amp; Reviewer (Reflection Pattern)", styles["h2"]))
    story.append(Paragraph(
        "Each agent is a CrewAI Agent with a specialized role, goal, and backstory. "
        "The Reviewer agent embodies the <b>Reflection pattern</b> — it critiques "
        "other agents' outputs and decides if revision is needed.",
        styles["body"],
    ))

    agent_code = '''from crewai import Agent
from app.config import get_llm_config

def create_analyzer() -> Agent:
    return Agent(
        role="Requirement Analyzer",
        goal=(
            "Parse and structure raw requirements into clear functional and "
            "non-functional categories. Identify key features, constraints, "
            "assumptions, ambiguities, and stakeholders."
        ),
        backstory=(
            "You are a senior business analyst with 15 years of experience "
            "in software requirements engineering. You excel at taking vague "
            "requirement documents and turning them into clear, structured "
            "analysis that engineering teams can act on."
        ),
        llm=get_llm_config(),
        verbose=True,
    )

def create_reviewer() -> Agent:
    return Agent(
        role="Estimation Reviewer",
        goal=(
            "Critically review the estimation for gaps, unrealistic timelines, "
            "and missing considerations. Provide a structured review decision "
            "indicating whether revision is needed."
        ),
        backstory=(
            "You are a QA-minded senior delivery manager who reviews project "
            "estimates before they go to clients. You output structured decisions "
            "with a clear needs_revision boolean, detailed feedback, and a "
            "confidence score between 0.0 and 1.0."
        ),
        llm=get_llm_config(),
        verbose=True,
    )'''
    story.extend(make_code_block("backend/app/agents/analyzer.py + reviewer.py", agent_code, content_width))
    story.append(Paragraph(
        "Figure 2: Agent definitions — each agent has a specialized persona with role, goal, and backstory",
        styles["caption"],
    ))

    # ── Code 2: Pipeline Orchestration (Multi-Agent + Planning) ──
    story.append(Spacer(1, 6))
    story.append(Paragraph("Pipeline Orchestration — Multi-Agent + Planning Pattern", styles["h2"]))
    story.append(Paragraph(
        "The pipeline runs 5 agents sequentially, passing each stage's output to the next. "
        "The <b>Reflection loop</b> at Stage 4 re-triggers estimation if the reviewer finds issues.",
        styles["body"],
    ))

    pipeline_code = '''def run_pipeline(job_id: str, requirement_text: str) -> None:
    """Run the full 5-agent pipeline with reflection loop."""
    store = get_job_store()

    # Create agents
    analyzer = create_analyzer()
    researcher = create_researcher()
    estimator = create_estimator()
    reviewer = create_reviewer()
    writer = create_writer()

    # Stage 1: Analyze
    store.update(job_id, status=ProposalStatus.ANALYZING)
    analyze_task = create_analyze_task(analyzer, requirement_text)
    crew = Crew(agents=[analyzer], tasks=[analyze_task],
                process=Process.sequential, verbose=True)
    result = crew.kickoff()
    analysis_output = str(result.tasks_output[0])
    store.update(job_id, stage_output={"analyzer": analysis_output})

    # Stage 2: Research (receives analysis)
    store.update(job_id, status=ProposalStatus.RESEARCHING)
    research_task = create_research_task(researcher, analysis=analysis_output)
    ...
    research_output = str(result.tasks_output[0])

    # Stage 3: Estimate (receives analysis + research)
    store.update(job_id, status=ProposalStatus.ESTIMATING)
    estimate_task = create_estimate_task(
        estimator, analysis=analysis_output, research=research_output)
    ...

    # Stage 4: Review — REFLECTION LOOP
    revision_rounds = 0
    while revision_rounds <= MAX_REVISION_ROUNDS:
        review_task = create_review_task(
            reviewer, analysis=analysis_output,
            research=research_output, estimation=estimation_output)
        ...
        review_decision = _parse_review_output(review_raw)

        if review_decision["needs_revision"] and revision_rounds < MAX_REVISION_ROUNDS:
            # Re-run estimation with reviewer feedback
            estimate_task = create_estimate_task(
                estimator, analysis=analysis_output,
                research=research_output,
                feedback=review_decision["feedback"])
            ...
            revision_rounds += 1
        else:
            break  # Proceed to writing

    # Stage 5: Write final proposal
    write_task = create_write_task(
        writer, analysis=analysis_output, research=research_output,
        estimation=estimation_output, review=review_summary)
    ...
    store.update(job_id, status=ProposalStatus.COMPLETED,
                 final_proposal=proposal_output)'''
    story.extend(make_code_block("backend/app/crew/pipeline.py", pipeline_code, content_width))
    story.append(Paragraph(
        "Figure 3: Pipeline orchestration — sequential 5-stage execution with reflection loop at review stage",
        styles["caption"],
    ))

    # ── Code 3: Task Definition with Context Passing ──
    story.append(Spacer(1, 6))
    story.append(Paragraph("Task Definition — Context Passing Between Agents", styles["h2"]))
    story.append(Paragraph(
        "Each task embeds the previous agents' outputs into its description, enabling "
        "the <b>Planning pattern</b> — each stage builds on the work of prior stages.",
        styles["body"],
    ))

    task_code = '''def create_estimate_task(
    agent, *, analysis: str, research: str, feedback: str = None
) -> Task:
    description = (
        "Based on the requirement analysis and technology research below, "
        "create a detailed project estimation. Your output must include:\\n"
        "1. **Effort Matrix** — Breakdown by module in person-hours\\n"
        "2. **Timeline** — Phases with durations (in weeks)\\n"
        "3. **Team Composition** — Roles and headcount\\n"
        "4. **Risk Factors** — Top risks with mitigation\\n"
        "5. **Assumptions for Estimation**\\n\\n"
        f"--- REQUIREMENT ANALYSIS ---\\n{truncate_text(analysis)}\\n"
        f"--- TECHNOLOGY RESEARCH ---\\n{truncate_text(research)}"
    )
    if feedback:
        description += (
            f"\\n\\n**REVISION FEEDBACK from Reviewer:**\\n{feedback}\\n"
            "Please revise your estimation to address the above feedback."
        )
    return Task(description=description, agent=agent,
        expected_output="A detailed project estimation...")'''
    story.extend(make_code_block("backend/app/crew/tasks.py — create_estimate_task()", task_code, content_width))
    story.append(Paragraph(
        "Figure 4: Task definition with context injection — previous outputs are embedded in prompts",
        styles["caption"],
    ))

    # ── Code 4: FastAPI Endpoint + Async Pipeline ──
    story.append(Spacer(1, 6))
    story.append(Paragraph("API Endpoint — Async Pipeline Trigger", styles["h2"]))
    story.append(Paragraph(
        "The FastAPI backend accepts PDF/text input and launches the pipeline in a "
        "background thread. The frontend polls for progress updates.",
        styles["body"],
    ))

    api_code = '''@app.post("/api/proposals/generate", response_model=GenerateResponse)
async def generate_proposal(
    file: UploadFile = File(None),
    text: str = Form(None),
):
    if not file and not text:
        raise HTTPException(status_code=400,
            detail="Provide either a PDF file or requirement text")

    requirement_text = ""
    if file:
        file_bytes = await file.read()
        requirement_text = extract_text_from_pdf(file_bytes)  # pdfplumber
    else:
        requirement_text = text.strip()

    # Create job and start pipeline in background thread
    job_id = str(uuid.uuid4())
    store = get_job_store()
    store.create(job_id)

    thread = threading.Thread(
        target=run_pipeline,
        args=(job_id, requirement_text),
        daemon=True)
    thread.start()

    return GenerateResponse(job_id=job_id, status="processing")'''
    story.extend(make_code_block("backend/app/main.py — generate_proposal()", api_code, content_width))
    story.append(Paragraph(
        "Figure 5: FastAPI endpoint — PDF/text ingestion with background pipeline execution",
        styles["caption"],
    ))

    # ── Code 5: Frontend Polling ──
    story.append(Spacer(1, 6))
    story.append(Paragraph("Frontend — Real-time Polling &amp; Pipeline Visualization", styles["h2"]))
    story.append(Paragraph(
        "The Next.js frontend polls the backend every 3 seconds and renders each "
        "agent's output as it completes, providing real-time pipeline visibility.",
        styles["body"],
    ))

    frontend_code = '''// front-end/app/page.js
const POLL_INTERVAL = 3000;

const poll = useCallback(async (jobId) => {
  const data = await getProposal(jobId);
  setJobData(data);
  if (data.status === "completed" || data.status === "failed") {
    stopPolling();
    setLoading(false);
  }
}, [stopPolling]);

async function handleSubmit({ file, text }) {
  setLoading(true);
  const res = await generateProposal({ file, text });
  setJobData({ job_id: res.job_id, status: res.status });
  pollingRef.current = setInterval(() => poll(res.job_id), POLL_INTERVAL);
}

// API client — front-end/lib/api.js
export async function generateProposal({ file, text }) {
  const formData = new FormData();
  if (file) formData.append("file", file);
  if (text) formData.append("text", text);
  const res = await fetch(`${API_BASE}/api/proposals/generate`, {
    method: "POST", body: formData });
  return res.json();
}

export const STAGES = [
  { key: "analyzing",   label: "Analyzing",   agent: "analyzer"   },
  { key: "researching", label: "Researching", agent: "researcher" },
  { key: "estimating",  label: "Estimating",  agent: "estimator"  },
  { key: "reviewing",   label: "Reviewing",   agent: "reviewer"   },
  { key: "writing",     label: "Writing",     agent: "writer"     },
];'''
    story.extend(make_code_block("front-end/app/page.js + lib/api.js", frontend_code, content_width))
    story.append(Paragraph(
        "Figure 6: Frontend polling logic and API client — real-time pipeline progress tracking",
        styles["caption"],
    ))

    # ════════════════════════════════════════
    # 5. RECOMMENDATIONS
    # ════════════════════════════════════════
    story.append(Paragraph("5. My Recommendations &amp; Suggestions", styles["h1"]))
    story.append(Paragraph(
        "Based on my experience taking this course and building the POC, here are my "
        "personal observations and suggestions for BJIT Limited:",
        styles["body"],
    ))

    recommendations = [
        ("<b>This course is practical, not theoretical — more engineers should take it</b> — "
         "Unlike many AI courses that focus on math and theory, this one is hands-on and "
         "directly applicable to our daily programming work. I'd recommend BJIT assign "
         "this to more engineering teams, especially those working on automation or "
         "AI-integrated products."),
        ("<b>Start using the reflection pattern immediately — it costs nothing</b> — "
         "Even without building agents, any engineer can improve their output today by "
         "adding a simple \"review and improve\" step when using ChatGPT or Copilot. "
         "I've already started doing this for code reviews and documentation, and the "
         "quality difference is noticeable."),
        ("<b>We should integrate agentic AI into our existing development workflow</b> — "
         "Rather than building new AI products, the fastest ROI is applying these patterns "
         "to what we already do: automated code review, test generation, requirement "
         "analysis, and documentation. These are daily pain points at BJIT that agentic "
         "AI can directly address."),
        ("<b>Don't overthink it — start small and iterate</b> — "
         "I initially planned a complex POC with databases, web search, and cloud deployment. "
         "But the course taught me to start simple, validate it works, then add complexity. "
         "My POC works end-to-end with just 5 agents and in-memory storage. "
         "I'd suggest the same approach for any BJIT team trying to adopt agentic AI."),
        ("<b>AI doesn't replace engineers — it makes us faster</b> — "
         "After building ProposalBot, my observation is that AI agents are best when they "
         "handle the repetitive, time-consuming parts of our work (research, drafting, "
         "reviewing) while we focus on design decisions and client understanding. "
         "The human-in-the-loop model is the right approach for client deliverables."),
        ("<b>Internal knowledge-sharing would multiply the impact</b> — "
         "The four agentic patterns (Reflection, Tool Use, Planning, Multi-Agent) are "
         "simple to explain and broadly useful. A 1-hour brown-bag session at BJIT could "
         "help other engineers start applying these patterns in their projects immediately."),
    ]
    for i, text in enumerate(recommendations, 1):
        story.append(Paragraph(f"{i}. {text}", styles["bullet"], bulletText=""))

    # ── Build ──
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"\n✅ PDF generated: {output_path}")
    return output_path


if __name__ == "__main__":
    build_pdf()
