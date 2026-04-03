from crewai import Agent, Crew, Process, Task, LLM
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from guardrails import validate_score_range


def create_scoring_crew():
    llm = LLM(
        model="openrouter/openai/gpt-4o-mini",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    scoring_agent = Agent(
        role="Lead Scoring Analyst",
        goal="Score leads based on fit, intent, and engagement potential to prioritize sales outreach",
        backstory=(
            "You are a data-driven lead scoring specialist who evaluates leads "
            "based on company fit (ICP match), buying intent signals, and "
            "engagement potential. You use a 0-100 scale and provide clear rationale."
        ),
        llm=llm,
        verbose=True,
    )

    scoring_task = Task(
        description=(
            "Score the following lead based on the enrichment data:\n\n"
            "Lead: {name}, {title} at {company}\n"
            "Enrichment data:\n{enrichment_data}\n\n"
            "Score on three dimensions (0-100 each):\n"
            "1) FIT SCORE: How well does this company match our ideal customer profile?\n"
            "2) INTENT SCORE: How likely are they to be in a buying cycle?\n"
            "3) ENGAGEMENT SCORE: How likely is this person to respond?\n\n"
            "Provide each score as a number, then an overall score (weighted average), "
            "a rationale paragraph, and a recommended action (pursue/nurture/archive)."
        ),
        expected_output=(
            "Scores in this format:\n"
            "Fit Score: [0-100]\nIntent Score: [0-100]\n"
            "Engagement Score: [0-100]\nOverall Score: [0-100]\n"
            "Rationale: [paragraph]\nRecommended Action: [pursue/nurture/archive]"
        ),
        agent=scoring_agent,
        guardrails=[validate_score_range],
    )

    return Crew(
        agents=[scoring_agent],
        tasks=[scoring_task],
        process=Process.sequential,
        verbose=True,
    )
