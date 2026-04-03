from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from callbacks import step_callback, task_callback
import os

@CrewBase
class FinancialResearchCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self):
        self.llm = LLM(
            model="openrouter/openai/gpt-4o-mini",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

    @agent
    def data_collector(self) -> Agent:
        return Agent(
            config=self.agents_config["data_collector"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            llm=self.llm,
        )

    @agent
    def financial_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["financial_analyst"],
            llm=self.llm,
        )

    @agent
    def report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["report_writer"],
            llm=self.llm,
        )

    @task
    def collect_data_task(self) -> Task:
        return Task(
            config=self.tasks_config["collect_data_task"],
            callback=task_callback,
        )

    @task
    def analyze_data_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_data_task"],
            callback=task_callback,
        )

    @task
    def write_report_task(self) -> Task:
        return Task(
            config=self.tasks_config["write_report_task"],
            callback=task_callback,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            planning=True,
            output_log_file="crew_execution.log",
            step_callback=step_callback,
        )
