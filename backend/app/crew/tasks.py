from crewai import Task
from app.utils.helpers import truncate_text


def create_analyze_task(agent, requirement_text: str) -> Task:
    return Task(
        description=(
            "Analyze the following requirement document and produce a structured "
            "analysis. Your output must include:\n"
            "1. **Project Overview** — Brief summary of what is being built\n"
            "2. **Functional Requirements** — Numbered list of features/capabilities\n"
            "3. **Non-Functional Requirements** — Performance, security, scalability, etc.\n"
            "4. **Constraints & Assumptions** — Budget, timeline, technology constraints\n"
            "5. **Ambiguities & Questions** — Things that are unclear or need clarification\n"
            "6. **Stakeholders** — Key roles involved\n\n"
            f"Requirement Document:\n```\n{truncate_text(requirement_text)}\n```"
        ),
        agent=agent,
        expected_output="A structured requirement analysis with sections for overview, functional/non-functional requirements, constraints, ambiguities, and stakeholders.",
    )


def create_research_task(agent, *, analysis: str) -> Task:
    return Task(
        description=(
            "Based on the requirement analysis below, research and "
            "recommend an appropriate technology stack. Your output must include:\n"
            "1. **Recommended Tech Stack** — Frontend, backend, database, infrastructure\n"
            "2. **Justification** — Why each technology choice fits the requirements\n"
            "3. **Alternatives Considered** — Other options evaluated and why they were rejected\n"
            "4. **Compatibility Notes** — How the recommended technologies work together\n"
            "5. **Third-Party Services** — APIs, payment gateways, hosting, etc. if applicable\n\n"
            f"--- REQUIREMENT ANALYSIS ---\n{truncate_text(analysis)}\n--- END ---"
        ),
        agent=agent,
        expected_output="A technology research report with recommendations, justification, alternatives, and compatibility notes.",
    )


def create_estimate_task(
    agent, *, analysis: str, research: str, feedback: str = None
) -> Task:
    description = (
        "Based on the requirement analysis and technology research below, create a "
        "detailed project estimation. Your output must include:\n"
        "1. **Effort Matrix** — Breakdown by module/feature in person-hours\n"
        "2. **Timeline** — Phases with durations (in weeks)\n"
        "3. **Team Composition** — Roles and number of people needed\n"
        "4. **Risk Factors** — Top risks with likelihood, impact, and mitigation\n"
        "5. **Assumptions for Estimation** — What assumptions underpin these numbers\n\n"
        f"--- REQUIREMENT ANALYSIS ---\n{truncate_text(analysis)}\n--- END ---\n\n"
        f"--- TECHNOLOGY RESEARCH ---\n{truncate_text(research)}\n--- END ---"
    )
    if feedback:
        description += (
            f"\n\n**IMPORTANT REVISION FEEDBACK from Reviewer:**\n{feedback}\n\n"
            "Please revise your estimation to address the above feedback."
        )

    return Task(
        description=description,
        agent=agent,
        expected_output="A detailed project estimation with effort matrix, timeline, team composition, risks, and assumptions.",
    )


def create_review_task(
    agent, *, analysis: str, research: str, estimation: str
) -> Task:
    return Task(
        description=(
            "Review the project estimation below for quality, completeness, and realism. "
            "Evaluate the following:\n"
            "- Are there any missing phases (e.g., testing, deployment, DevOps)?\n"
            "- Are the person-hour estimates realistic for the scope?\n"
            "- Is the timeline achievable?\n"
            "- Are there overlooked risks?\n"
            "- Is the team composition adequate?\n\n"
            "You MUST output your review in the following structured JSON format:\n"
            "```json\n"
            "{\n"
            '  "needs_revision": true/false,\n'
            '  "feedback": "Detailed feedback explaining what needs to change",\n'
            '  "confidence_score": 0.0-1.0\n'
            "}\n"
            "```\n\n"
            "Set needs_revision to true ONLY if there are significant gaps or unrealistic "
            "estimates. Minor suggestions can be included in feedback with needs_revision=false.\n\n"
            f"--- REQUIREMENT ANALYSIS ---\n{truncate_text(analysis)}\n--- END ---\n\n"
            f"--- TECHNOLOGY RESEARCH ---\n{truncate_text(research)}\n--- END ---\n\n"
            f"--- PROJECT ESTIMATION ---\n{truncate_text(estimation)}\n--- END ---"
        ),
        agent=agent,
        expected_output="A structured review decision JSON with needs_revision (boolean), feedback (string), and confidence_score (0.0-1.0).",
    )


def create_write_task(
    agent, *, analysis: str, research: str, estimation: str, review: str
) -> Task:
    return Task(
        description=(
            "Compile all the agent outputs below into a single, polished, "
            "client-ready project proposal in Markdown format. The proposal must include:\n\n"
            "# Project Proposal: [Project Name]\n\n"
            "## Executive Summary\n"
            "## Project Scope & Objectives\n"
            "## Requirement Analysis\n"
            "### Functional Requirements\n"
            "### Non-Functional Requirements\n"
            "## Proposed Technology Stack\n"
            "## Project Estimation\n"
            "### Effort Breakdown\n"
            "### Timeline\n"
            "### Team Composition\n"
            "## Risk Assessment & Mitigation\n"
            "## Assumptions & Dependencies\n"
            "## Next Steps\n\n"
            "Format the proposal with clean Markdown including headers, tables, and bullet points. "
            "Make it professional and suitable for presenting to a client.\n\n"
            f"--- REQUIREMENT ANALYSIS ---\n{truncate_text(analysis)}\n--- END ---\n\n"
            f"--- TECHNOLOGY RESEARCH ---\n{truncate_text(research)}\n--- END ---\n\n"
            f"--- PROJECT ESTIMATION ---\n{truncate_text(estimation)}\n--- END ---\n\n"
            f"--- REVIEWER FEEDBACK ---\n{truncate_text(review)}\n--- END ---"
        ),
        agent=agent,
        expected_output="A complete, well-formatted Markdown project proposal with all sections filled in from the previous agent outputs.",
    )
