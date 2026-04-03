from crewai import Agent, Crew, Process, Task, LLM
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from guardrails import validate_email_quality


def create_outreach_crew():
    llm = LLM(
        model="openrouter/openai/gpt-4o-mini",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    email_writer = Agent(
        role="Sales Email Copywriter",
        goal="Write highly personalized, compelling outreach emails that get responses",
        backstory=(
            "You are an elite sales copywriter who specializes in cold outreach. "
            "Your emails have a 40%+ open rate and 15%+ response rate. You never "
            "use generic templates — every email is deeply personalized based on "
            "the prospect's company, role, pain points, and recent activities."
        ),
        llm=llm,
        verbose=True,
        memory=True,
    )

    email_task = Task(
        description=(
            "Write a personalized sales outreach email for:\n\n"
            "Contact: {name}, {title} at {company}\n"
            "Company details:\n{enrichment_data}\n"
            "Lead score: {overall_score}/100\n"
            "Scoring rationale: {scoring_rationale}\n\n"
            "{revision_instructions}\n\n"
            "Requirements:\n"
            "- Start with 'Subject: [compelling subject line]'\n"
            "- Personalize based on their specific company and role\n"
            "- Reference a specific pain point or recent news\n"
            "- Keep it under 150 words (body only)\n"
            "- Include a clear, low-friction call-to-action\n"
            "- Sound human, not like a template\n"
            "- List 2-3 personalization hooks used"
        ),
        expected_output=(
            "Subject: [subject line]\n\n"
            "[email body - personalized, under 150 words]\n\n"
            "Personalization hooks used:\n1. [hook 1]\n2. [hook 2]\n3. [hook 3]"
        ),
        agent=email_writer,
        guardrails=[validate_email_quality],
    )

    return Crew(
        agents=[email_writer],
        tasks=[email_task],
        process=Process.sequential,
        verbose=True,
        memory=True,
    )
