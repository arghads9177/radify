from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

# Uncomment the following line to use an example of a custom tool
# from radify_api.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

load_dotenv()

@CrewBase
class RadifyApiCrew():
	"""RadifyApi crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def project_classifier(self) -> Agent:
		print(f"Loading config: {self.agents_config['project_classifier']}")
		return Agent(
			config=self.agents_config['project_classifier'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def job_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['job_analyzer'],
			verbose=True
		)
	
	@agent
	def rad_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['rad_writer'],
			verbose=True
		)
	
	@agent
	def quality_reviewer(self) -> Agent:
		return Agent(
			config=self.agents_config['quality_reviewer'],
			verbose=True
		)

	@task
	def classify_project(self) -> Task:
		return Task(
			config=self.tasks_config['classify_project'],
			agent=self.project_classifier()
		)

	@task
	def analyze_job(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_job'],
			agent = self.job_analyzer()
		)
	
	@task
	def write_rad(self) -> Task:
		return Task(
			config=self.tasks_config['write_rad'],
			agent = self.rad_writer()
		)
	
	@task
	def review_rad(self) -> Task:
		return Task(
			config=self.tasks_config['review_rad'],
			agent= self.quality_reviewer()
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the RadifyApi crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)