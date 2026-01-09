from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

llm=LLM(
#   api_key=os.getenv("MISTRAL_API_KEY"),
#   base_url="https://api.mistral.ai/v1",
  model="mistral/mistral-large-2512",
  temperature=0.1,
)

@CrewBase
class KubeInvestAi():
    """KubeInvestAi crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'], # type: ignore[index]
            verbose=True,
            llm=llm
        )
    
    @agent
    def reporter(self) -> Agent:
        return Agent(
            config=self.agents_config['reporter'], # type: ignore[index]
            verbose=True,
            llm=llm
        )
    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def analyze_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_task'], # type: ignore[index]
        )

    @task
    def report_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_task'], # type: ignore[index]
            output_file='report.md'
        )
    @crew
    def crew(self) -> Crew:
        """Creates the KubeInvestAi crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
