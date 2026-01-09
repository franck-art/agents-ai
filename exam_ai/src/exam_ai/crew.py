from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
import yaml
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

from dotenv import load_dotenv



load_dotenv(override=True)

eleve1=LLM(
#   api_key=os.getenv("MISTRAL_API_KEY"),
#   base_url="https://api.mistral.ai/v1",
  model="mistral/mistral-large-2512",
  temperature=0.1,
)
eleve2=LLM(
#   api_key=os.getenv("MISTRAL_API_KEY"),
#   base_url="https://api.mistral.ai/v1",
  model="mistral/mistral-small-2506",
  temperature=0.1,
)
prof=LLM(
#   api_key=os.getenv("MISTRAL_API_KEY"),
#   base_url="https://api.mistral.ai/v1",
  model="mistral/ministral-8b-2512",
  temperature=0.1,
)

@CrewBase
class ExamAi():
    """ExamAi crew"""
    
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def eleve1(self) -> Agent:
        return Agent(
            config=self.agents_config['eleve1'], # type: ignore[index]
            verbose=True,
            llm=eleve1
        )

    @agent
    def eleve2(self) -> Agent:
        return Agent(
            config=self.agents_config['eleve2'], # type: ignore[index]
            verbose=True,
            llm=eleve2
        )
    @agent
    def professeur(self) -> Agent:
        return Agent(
            config=self.agents_config['professeur'], # type: ignore[index]
            verbose=True,
            llm=prof
        )
    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def eleve1_task(self) -> Task:
        return Task(
            config=self.tasks_config['eleve1_task'], # type: ignore[index]
            output_file='eleve1.md'
        )

    @task
    def eleve2_task(self) -> Task:
        return Task(
            config=self.tasks_config['eleve2_task'], # type: ignore[index]
            output_file='eleve2.md'
        )

    @task
    def prof_task(self) -> Task:
        return Task(
            config=self.tasks_config['prof_task'], # type: ignore[index]
            output_file='prof.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ExamAi crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
