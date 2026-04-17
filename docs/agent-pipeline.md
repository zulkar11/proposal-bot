# Agent Pipeline & Reflection Logic

## Pipeline Overview

ProposalBot uses a **sequential 5-agent pipeline** where each agent specializes in one aspect of proposal generation. The output of each agent feeds into the next.

```
┌──────────┐    ┌──────────┐    ┌────────────┐    ┌────────────┐    ┌──────────┐
│ Analyzer │ →  │ Research │ →  │ Estimation │ →  │  Reviewer  │ →  │  Writer  │
│          │    │          │    │            │    │ (Reflect)  │    │          │
└──────────┘    └──────────┘    └────────────┘    └─────┬──────┘    └──────────┘
                                       ▲                │
                                       │    ┌───────────┘
                                       │    │ needs_revision?
                                       │    ▼
                                       └─ YES → Re-run with feedback
                                          NO  → Continue to Writer
```

---

## Agent Descriptions

### 1. Requirement Analyzer
| Attribute | Value |
|---|---|
| **Role** | Requirement Analyzer |
| **Goal** | Parse and structure raw requirements into clear functional/non-functional categories |
| **Input** | Raw requirement text (from PDF or pasted text) |
| **Output** | Structured analysis: key features, constraints, assumptions, ambiguities, stakeholders |

### 2. Technology Researcher
| Attribute | Value |
|---|---|
| **Role** | Technology Researcher |
| **Goal** | Recommend appropriate technologies based on the analyzed requirements |
| **Input** | Analyzer output |
| **Output** | Tech stack recommendations with justification, alternatives considered, compatibility notes |

### 3. Project Estimator
| Attribute | Value |
|---|---|
| **Role** | Project Estimator |
| **Goal** | Provide effort and timeline estimation broken down by phase and module |
| **Input** | Analyzer + Researcher outputs |
| **Output** | Effort matrix (person-hours), timeline, team composition, risk factors with mitigation |

### 4. Estimation Reviewer (Reflection Agent)
| Attribute | Value |
|---|---|
| **Role** | Estimation Reviewer |
| **Goal** | Critically review the estimation for gaps, unrealistic timelines, and missing considerations |
| **Input** | All previous agent outputs |
| **Output** | Structured review decision (JSON): `needs_revision`, `feedback`, `confidence_score` |

### 5. Proposal Writer
| Attribute | Value |
|---|---|
| **Role** | Proposal Writer |
| **Goal** | Compile all agent outputs into a polished, client-ready project proposal |
| **Input** | All finalized agent outputs |
| **Output** | Complete Markdown proposal with executive summary, scope, timeline, estimation, tech stack, risks |

---

## Reflection Loop Logic

The **Reflection pattern** is the core differentiator of this pipeline. The Reviewer agent uses **structured Pydantic output** (not fragile string matching) to reliably signal whether revision is needed.

```python
# pipeline.py — Actual implementation
from crewai import Agent, Task, Crew, Process

MAX_REVISION_ROUNDS = 1  # Keep bounded for POC

def run_pipeline(job_id: str, requirement_text: str) -> None:
    """Run the full 5-agent pipeline with reflection loop."""
    store = get_job_store()

    # Create agents (each defined in its own file)
    analyzer = create_analyzer()      # role="Requirement Analyzer"
    researcher = create_researcher()  # role="Technology Researcher"
    estimator = create_estimator()    # role="Project Estimator"
    reviewer = create_reviewer()      # role="Estimation Reviewer"
    writer = create_writer()          # role="Proposal Writer"

    # Stage 1-3: Run sequentially, passing context forward
    analyze_task = create_analyze_task(analyzer, requirement_text)
    crew = Crew(agents=[analyzer], tasks=[analyze_task],
                process=Process.sequential, verbose=True)
    analysis_output = str(crew.kickoff().tasks_output[0])

    research_task = create_research_task(researcher, analysis=analysis_output)
    # ... same pattern for research and estimation ...

    # Stage 4: Reflection Loop
    revision_rounds = 0
    while revision_rounds <= MAX_REVISION_ROUNDS:
        review_task = create_review_task(
            reviewer, analysis=analysis_output,
            research=research_output, estimation=estimation_output)
        # ... run reviewer crew ...
        review_decision = _parse_review_output(review_raw)  # JSON parsing

        if review_decision["needs_revision"] and revision_rounds < MAX_REVISION_ROUNDS:
            # Re-run estimator with feedback
            estimate_task = create_estimate_task(
                estimator, analysis=analysis_output,
                research=research_output,
                feedback=review_decision["feedback"])
            revision_rounds += 1
        else:
            break

    # Stage 5: Write final proposal
    write_task = create_write_task(writer, analysis=analysis_output,
        research=research_output, estimation=estimation_output,
        review=review_summary)
```

### Reflection Loop Control Flow

```
1. Run stages: Analyzer → Researcher → Estimator
2. Run Reviewer → outputs structured JSON with needs_revision, feedback, confidence_score
3. IF needs_revision == True AND revision_rounds < MAX_REVISION_ROUNDS:
     → Re-run Estimator with reviewer.feedback injected into task description
     → Re-run Reviewer on revised estimation
     → revision_rounds += 1
4. Run Writer with all finalized outputs
```

### Review Output Parsing

The reviewer outputs a JSON structure, which is parsed with fallback handling:

| Approach | Problem |
|---|---|
| ❌ `if "NEEDS_REVISION" in output` | LLMs don't output exact strings consistently; fragile and unreliable |
| ✅ JSON parsing with `_parse_review_output()` | Tries direct JSON, then markdown code block extraction, then safe fallback |

```python
def _parse_review_output(review_raw: str) -> dict:
    """Parse reviewer's JSON output with fallback handling."""
    try:
        return json.loads(review_raw)            # Direct JSON
    except (json.JSONDecodeError, TypeError):
        pass
    # Try extracting JSON from ```json ... ``` block
    if "```json" in text:
        start = text.index("```json") + 7
        end = text.index("```", start)
        return json.loads(text[start:end].strip())
    # Fallback: no revision needed
    return {"needs_revision": False, "feedback": text, "confidence_score": 0.5}
```

---

## Pipeline Status Updates

The pipeline updates job status in the in-memory store as each agent completes, enabling the frontend to show real-time progress via 3-second polling:

```python
# Pipeline execution with status tracking (runs in background thread)
def run_pipeline(job_id: str, requirement_text: str) -> None:
    store = get_job_store()

    store.update(job_id, status="analyzing")
    analysis = str(crew.kickoff().tasks_output[0])
    store.update(job_id, stage_output={"analyzer": analysis})

    store.update(job_id, status="researching")
    research = str(crew.kickoff().tasks_output[0])
    store.update(job_id, stage_output={"researcher": research})

    store.update(job_id, status="estimating")
    estimation = str(crew.kickoff().tasks_output[0])
    store.update(job_id, stage_output={"estimator": estimation})

    store.update(job_id, status="reviewing")
    review_raw = str(crew.kickoff().tasks_output[0])
    review_decision = _parse_review_output(review_raw)
    store.update(job_id, stage_output={"reviewer": review_summary})

    # Reflection loop — re-run estimation if reviewer finds issues
    if review_decision["needs_revision"]:
        store.update(job_id, status="estimating")
        estimation = run_estimator_with_feedback(review_decision["feedback"])
        # Re-review...

    store.update(job_id, status="writing")
    proposal = str(crew.kickoff().tasks_output[0])
    store.update(job_id, status="completed", final_proposal=proposal)
```
