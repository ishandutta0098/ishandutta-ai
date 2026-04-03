from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
from tools import ResumeParserTool, parse_job_description
from models import CompanyProfile, TailoredResume, CoverLetter
import os


def on_task_complete(output):
    print(f"[Callback] Task completed | Output preview: {str(output.raw)[:200]}")


@CrewBase
class JobApplicationCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self):
        self.llm = LLM(
            model="openrouter/openai/gpt-4o-mini",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

    @agent
    def company_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["company_researcher"],
            tools=[ScrapeWebsiteTool()],
            llm=self.llm,
        )

    @agent
    def resume_tailor(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_tailor"],
            tools=[ResumeParserTool(), parse_job_description],
            llm=self.llm,
        )

    @agent
    def cover_letter_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["cover_letter_writer"],
            llm=self.llm,
        )

    @task
    def research_company_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_company_task"],
            output_pydantic=CompanyProfile,
            callback=on_task_complete,
        )

    @task
    def tailor_resume_task(self) -> Task:
        return Task(
            config=self.tasks_config["tailor_resume_task"],
            output_pydantic=TailoredResume,
            context=[self.research_company_task()],
            callback=on_task_complete,
        )

    @task
    def write_cover_letter_task(self) -> Task:
        return Task(
            config=self.tasks_config["write_cover_letter_task"],
            output_pydantic=CoverLetter,
            context=[self.research_company_task(), self.tailor_resume_task()],
            callback=on_task_complete,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_llm=self.llm,
            verbose=True,
        )
