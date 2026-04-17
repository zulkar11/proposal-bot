import json
import logging
import traceback
from crewai import Crew, Process

from app.agents import (
    create_analyzer,
    create_researcher,
    create_estimator,
    create_reviewer,
    create_writer,
)
from app.crew.tasks import (
    create_analyze_task,
    create_research_task,
    create_estimate_task,
    create_review_task,
    create_write_task,
)
from app.config import MAX_REVISION_ROUNDS
from app.models import ProposalStatus
from app.services.job_store import get_job_store

logger = logging.getLogger(__name__)


def _parse_review_output(review_raw: str) -> dict:
    """Parse the reviewer's output to extract the structured review decision."""
    try:
        # Try direct JSON parse
        return json.loads(review_raw)
    except (json.JSONDecodeError, TypeError):
        pass

    # Try extracting JSON from markdown code block
    text = str(review_raw)
    if "```json" in text:
        start = text.index("```json") + 7
        end = text.index("```", start)
        try:
            return json.loads(text[start:end].strip())
        except (json.JSONDecodeError, ValueError):
            pass
    elif "```" in text:
        start = text.index("```") + 3
        end = text.index("```", start)
        try:
            return json.loads(text[start:end].strip())
        except (json.JSONDecodeError, ValueError):
            pass

    # Fallback: treat as no revision needed with raw text as feedback
    return {
        "needs_revision": False,
        "feedback": text,
        "confidence_score": 0.5,
    }


def run_pipeline(job_id: str, requirement_text: str) -> None:
    """Run the full 5-agent pipeline with reflection loop."""
    store = get_job_store()

    try:
        # Create agents
        analyzer = create_analyzer()
        researcher = create_researcher()
        estimator = create_estimator()
        reviewer = create_reviewer()
        writer = create_writer()

        # --- Stage 1: Analyze ---
        store.update(job_id, status=ProposalStatus.ANALYZING)
        analyze_task = create_analyze_task(analyzer, requirement_text)
        crew = Crew(
            agents=[analyzer],
            tasks=[analyze_task],
            process=Process.sequential,
            verbose=True,
        )
        result = crew.kickoff()
        analysis_output = str(result.tasks_output[0]) if result.tasks_output else str(result)
        store.update(job_id, stage_output={"analyzer": analysis_output})

        # --- Stage 2: Research ---
        store.update(job_id, status=ProposalStatus.RESEARCHING)
        research_task = create_research_task(researcher, analysis=analysis_output)
        crew = Crew(
            agents=[researcher],
            tasks=[research_task],
            process=Process.sequential,
            verbose=True,
        )
        result = crew.kickoff()
        research_output = str(result.tasks_output[0]) if result.tasks_output else str(result)
        store.update(job_id, stage_output={"researcher": research_output})

        # --- Stage 3: Estimate ---
        store.update(job_id, status=ProposalStatus.ESTIMATING)
        estimate_task = create_estimate_task(
            estimator, analysis=analysis_output, research=research_output
        )
        crew = Crew(
            agents=[estimator],
            tasks=[estimate_task],
            process=Process.sequential,
            verbose=True,
        )
        result = crew.kickoff()
        estimation_output = str(result.tasks_output[0]) if result.tasks_output else str(result)
        store.update(job_id, stage_output={"estimator": estimation_output})

        # --- Stage 4: Review (Reflection) ---
        revision_rounds = 0
        while revision_rounds <= MAX_REVISION_ROUNDS:
            store.update(job_id, status=ProposalStatus.REVIEWING)
            review_task = create_review_task(
                reviewer,
                analysis=analysis_output,
                research=research_output,
                estimation=estimation_output,
            )
            crew = Crew(
                agents=[reviewer],
                tasks=[review_task],
                process=Process.sequential,
                verbose=True,
            )
            result = crew.kickoff()
            review_raw = str(result.tasks_output[0]) if result.tasks_output else str(result)
            review_decision = _parse_review_output(review_raw)

            review_summary = (
                f"**Confidence:** {review_decision.get('confidence_score', 'N/A')}\n\n"
                f"**Feedback:** {review_decision.get('feedback', 'No feedback')}\n\n"
                f"**Needs Revision:** {review_decision.get('needs_revision', False)}"
            )
            store.update(job_id, stage_output={"reviewer": review_summary})

            needs_revision = review_decision.get("needs_revision", False)

            if needs_revision and revision_rounds < MAX_REVISION_ROUNDS:
                logger.info(f"Revision triggered for job {job_id}, round {revision_rounds + 1}")
                store.update(job_id, revision_triggered=True)

                # Re-run estimation with feedback
                store.update(job_id, status=ProposalStatus.ESTIMATING)
                feedback = review_decision.get("feedback", "")
                estimate_task = create_estimate_task(
                    estimator,
                    analysis=analysis_output,
                    research=research_output,
                    feedback=feedback,
                )
                crew = Crew(
                    agents=[estimator],
                    tasks=[estimate_task],
                    process=Process.sequential,
                    verbose=True,
                )
                result = crew.kickoff()
                estimation_output = str(result.tasks_output[0]) if result.tasks_output else str(result)
                store.update(job_id, stage_output={"estimator": estimation_output})

                revision_rounds += 1
            else:
                break

        # --- Stage 5: Write ---
        store.update(job_id, status=ProposalStatus.WRITING)
        write_task = create_write_task(
            writer,
            analysis=analysis_output,
            research=research_output,
            estimation=estimation_output,
            review=review_summary,
        )
        crew = Crew(
            agents=[writer],
            tasks=[write_task],
            process=Process.sequential,
            verbose=True,
        )
        result = crew.kickoff()
        proposal_output = str(result.tasks_output[0]) if result.tasks_output else str(result)
        store.update(
            job_id,
            status=ProposalStatus.COMPLETED,
            final_proposal=proposal_output,
        )

        logger.info(f"Pipeline completed for job {job_id}")

    except Exception as e:
        logger.error(f"Pipeline failed for job {job_id}: {traceback.format_exc()}")
        store.update(
            job_id,
            status=ProposalStatus.FAILED,
            error=str(e),
        )
