from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class Debate:
    """Debate crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @before_kickoff
    def pre_kickoff(self, inputs):
        print("Before kickoff", inputs)
        return inputs

    @after_kickoff
    def post_kickoff(self, output):
        print("After kickoff")
        return output

    @agent
    def foreign_policy_expert(self) -> Agent:
        return Agent(
            config=self.agents_config["foreign_policy_expert"],
            verbose=True,
        )

    @agent
    def pro_american_citizen(self) -> Agent:
        return Agent(
            config=self.agents_config["pro_american_citizen"],
            verbose=True,
        )

    @agent
    def debate_analyst(self) -> Agent:
        return Agent(config=self.agents_config["debate_analyst"], verbose=True)

    @agent
    def judge(self) -> Agent:
        return Agent(config=self.agents_config["judge"], verbose=True)

    @task
    def foreign_policy_expert_task(self) -> Task:
        """Creates a foreign policy expert task"""
        return Task(
            config=self.tasks_config["foreign_policy_expert_task"],
        )

    @task
    def pro_american_citizen_task(self) -> Task:
        """Creates a pro-american citizen task"""
        return Task(
            config=self.tasks_config["pro_american_citizen_task"],
        )

    @task
    def analyst_task(self) -> Task:
        """Creates an analyst task"""
        return Task(
            config=self.tasks_config["debate_analyst_task"],
        )

    @task
    def judge_task(self) -> Task:
        """Creates a judge task"""
        return Task(
            config=self.tasks_config["judge_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Debate crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical,
        )
