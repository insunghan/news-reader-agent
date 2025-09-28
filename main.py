import dotenv
import os

dotenv.load_dotenv()

from crewai import Crew, Agent, Task, LLM
from crewai.project import CrewBase, agent, task, crew, llm


@CrewBase
class TranslatorCrew:
    # 🚀 LLM 정의 메서드 추가
    @llm
    def openai_llm(self):
        return LLM(
            model='openai/gpt-5-nano',
            base_url=os.getenv("OPENAI_API_BASE", 'https://api.openai.com/v1'),
        )

    @agent
    def translator_agent(self):
        return Agent(
            config=self.agents_config["translator_agent"],
            llm=self.openai_llm(),  # LLM 인스턴스를 직접 참조
        )

    @task
    def translate_task(self):
        return Task(
            config=self.tasks_config["translate_task"],
        )

    @task
    def retranslate_task(self):
        return Task(
            config=self.tasks_config["retranslate_task"],
        )

    @crew
    def assemble_crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )


TranslatorCrew().assemble_crew().kickoff(
    inputs={
        "sentence": "I'm Nico and I like to ride my bicicle in Napoli",
    }
)