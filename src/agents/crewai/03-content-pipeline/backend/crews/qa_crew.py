from crewai import Agent, Crew, Process, Task, LLM
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from guardrails import validate_word_count, validate_no_placeholders


def create_qa_crew():
    llm = LLM(
        model="openrouter/openai/gpt-4o-mini",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    qa_reviewer = Agent(
        role="Content Quality Reviewer",
        goal="Ensure all content meets brand standards, is factually sound, and ready for publication",
        backstory=(
            "You are a senior editor with an eye for detail. You check content for "
            "quality, accuracy, brand alignment, readability, and engagement. "
            "You score content on a scale of 1-100 and provide specific feedback "
            "for any issues found."
        ),
        llm=llm,
        verbose=True,
    )

    qa_task = Task(
        description=(
            "Review the following content for quality and brand alignment:\n\n"
            "{draft}\n\n"
            "Evaluate on: 1) Brand voice alignment, 2) Factual accuracy, "
            "3) Structure and readability, 4) Engagement and hook quality, "
            "5) Call-to-action clarity. "
            "Provide a score from 1-100 and specific feedback."
        ),
        expected_output=(
            "A quality review with: overall score (1-100) on the FIRST line as just a number, "
            "followed by detailed feedback on each criterion, and specific suggestions "
            "for improvement if score < 80."
        ),
        agent=qa_reviewer,
        guardrails=[validate_word_count, validate_no_placeholders],
    )

    return Crew(
        agents=[qa_reviewer],
        tasks=[qa_task],
        process=Process.sequential,
        verbose=True,
    )
