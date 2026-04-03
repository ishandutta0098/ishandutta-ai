from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
import os


def create_enrichment_crew():
    llm = LLM(
        model="openrouter/openai/gpt-4o-mini",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    company_researcher = Agent(
        role="Company Intelligence Specialist",
        goal="Research and enrich company data for {company}, finding key details that help personalize sales outreach",
        backstory=(
            "You are a B2B sales intelligence expert who specializes in company research. "
            "You can quickly find company descriptions, industry, size, funding, tech stack, "
            "and recent news that reveal pain points and opportunities for engagement."
        ),
        tools=[SerperDevTool(), ScrapeWebsiteTool()],
        llm=llm,
        verbose=True,
    )

    person_researcher = Agent(
        role="Contact Intelligence Specialist",
        goal="Research the contact person {name} at {company} to understand their background and decision-making authority",
        backstory=(
            "You are an expert at finding professional background information about business contacts. "
            "You identify their career history, areas of responsibility, and potential pain points "
            "based on their role and industry."
        ),
        tools=[SerperDevTool()],
        llm=llm,
        verbose=True,
    )

    company_task = Task(
        description=(
            "Research {company} thoroughly. Find: "
            "1) Company description, 2) Industry and market segment, "
            "3) Company size, 4) Funding stage, "
            "5) Technology stack, 6) Recent news from last 3 months, "
            "7) Likely pain points or challenges. "
            "Additional context: {notes}"
        ),
        expected_output="A comprehensive company profile with all requested fields filled in.",
        agent=company_researcher,
    )

    person_task = Task(
        description=(
            "Research {name}, {title} at {company}. "
            "Find: 1) Professional background summary, "
            "2) Whether they are a decision maker for software/service purchases, "
            "3) Any recent posts, talks, or articles. "
            "LinkedIn URL if available: {linkedin_url}"
        ),
        expected_output="A person profile with background summary and decision-maker assessment.",
        agent=person_researcher,
    )

    return Crew(
        agents=[company_researcher, person_researcher],
        tasks=[company_task, person_task],
        process=Process.sequential,
        verbose=True,
    )
