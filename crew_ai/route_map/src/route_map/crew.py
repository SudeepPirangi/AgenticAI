import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from typing import List

try:
    PERPLEXITY_API_KEY = os.environ["PERPLEXITY_API_KEY"]
    PERPLEXITY_MODEL = os.environ["PERPLEXITY_MODEL"]
    PERPLEXITY_BASE_URL = os.environ["PERPLEXITY_BASE_URL"]

    print("PERPLEXITY environment variables are found")
except KeyError:
    print("Error: 'PERPLEXITY_XXX' environment variable not set.")

perplexity_llm = LLM(
    model=PERPLEXITY_MODEL,
    base_url=PERPLEXITY_BASE_URL,
    api_key=PERPLEXITY_API_KEY,
)


@CrewBase
class RouteMap:
    """RouteMap crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def professional_guide(self) -> Agent:
        return Agent(
            config=self.agents_config["professional_guide"],
            verbose=True,
            llm=perplexity_llm,
            tools=[SerperDevTool()],
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["reporting_analyst"],
            verbose=True,
            llm=perplexity_llm,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config["reporting_task"],
            output_file="output/road_map.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the RouteMap crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
