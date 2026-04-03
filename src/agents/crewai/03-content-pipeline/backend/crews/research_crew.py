from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
import os


def create_research_crew():
    llm = LLM(
        model="openrouter/openai/gpt-4o-mini",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    researcher = Agent(
        role="Content Researcher",
        goal="Find comprehensive, accurate information and data to support content creation on {topic}",
        backstory=(
            "You are a meticulous researcher who always finds the most relevant, "
            "up-to-date information. You verify facts, find statistics, and identify "
            "expert opinions to create a solid research foundation for content."
        ),
        tools=[SerperDevTool(), ScrapeWebsiteTool()],
        llm=llm,
        verbose=True,
    )

    research_task = Task(
        description=(
            "Research the topic '{topic}' thoroughly for a {content_type} targeting {target_audience}. "
            "Find: 1) Key facts and statistics, 2) Recent developments, "
            "3) Expert opinions or quotes, 4) Real-world examples or case studies, "
            "5) Common questions the audience has about this topic."
        ),
        expected_output=(
            "A comprehensive research brief with: key facts with sources, "
            "3-5 statistics, 2-3 expert perspectives, 2 case studies or examples, "
            "and 5 common audience questions. All information should be accurate and recent."
        ),
        agent=researcher,
    )

    return Crew(
        agents=[researcher],
        tasks=[research_task],
        process=Process.sequential,
        verbose=True,
    )
