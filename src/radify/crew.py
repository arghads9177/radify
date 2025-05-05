from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from dotenv import load_dotenv
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

load_dotenv()

@CrewBase
class Radify():
    """Radify crew"""

    # agents: List[BaseAgent]
    # tasks: List[Task]
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def project_classifier(self) -> Agent:
        return Agent(
            config=self.agents_config['project_classifier'], # type: ignore[index]
            verbose=True
        )

    @agent
    def job_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['job_analyzer'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def rad_writer(self) -> Agent:
        return Agent(
            config = self.agents_config['rad_writer'],
            verbose=True
        )
    
    @agent
    def quality_reviewer(self) -> Agent:
        return Agent(
            config = self.agents_config['quality_reviewer'],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def classify_project(self) -> Task:
        return Task(
            config=self.tasks_config['classify_project'], # type: ignore[index]
            agent = self.project_classifier()
        )
    
    @task
    def analyze_job(self) -> task:
        return Task(
            config= self.tasks_config['analyze_job'],
            agent = self.job_analyzer()
        )
    
    @task
    def write_rad(self) -> task:
        return Task(
            config= self.tasks_config['write_rad'],
            agent= self.rad_writer()
        )

    @task
    def review_rad(self) -> Task:
        return Task(
            config=self.tasks_config['review_rad'], # type: ignore[index]
            output_file='rad.md',
            agent= self.quality_reviewer()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Radify crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
