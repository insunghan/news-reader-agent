import dotenv
# import os

dotenv.load_dotenv()

from crewai import Crew, Agent, Task, LLM
from crewai.project import CrewBase, agent, task, crew, llm
from tools import count_letters
from tools import search_tool, scrape_tool

@CrewBase
class TranslatorCrew:
    # 🚀 LLM 정의 메서드 추가
    # @llm
    # def openai_llm(self):
    #     return LLM(
    #         model='openai/gpt-5-nano',
    #         base_url=os.getenv("OPENAI_API_BASE", 'https://api.openai.com/v1'),
    #     )

    @agent
    def translator_agent(self):
        return Agent(
            config=self.agents_config["translator_agent"],
            #llm=self.openai_llm(),  # LLM 인스턴스를 직접 참조
        )

    @agent
    def counter_agent(self):
        return Agent(
            config=self.agents_config["counter_agent"],
            tools=[count_letters],
            # llm=self.openai_llm(),  # LLM 인스턴스를 직접 참조
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

    @task
    def count_task(self):
        return Task(
            config=self.tasks_config["count_task"],
        )

    @crew
    def assemble_crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )

@CrewBase
class NewsReaderAgent:
    @agent
    def news_hunter_agent(self):
        return Agent(
            config=self.agents_config["news_hunter_agent"],
            tools=[search_tool, scrape_tool],
        )
    
    @agent
    def summarizer_agent(self):
        return Agent(
            config=self.agents_config["summarizer_agent"],
            tools=[scrape_tool],
        )

    @agent
    def curator_agent(self):
        return Agent(
            config=self.agents_config["curator_agent"],
        )
    
    @task
    def content_harvesting_task(self):
        return Task(
            config=self.tasks_config["content_harvesting_task"],
        )

    @task
    def summarization_task(self):
        return Task(
            config=self.tasks_config["summarization_task"],
        )

    @task
    def final_report_assembly_task(self):
        return Task(
            config=self.tasks_config["final_report_assembly_task"],
        )

    @crew
    def crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )

result = NewsReaderAgent().crew().kickoff(inputs={"topic": "Son Heung-min"})

for task_output in result.tasks_output:
    print(task_output)

# TranslatorCrew().assemble_crew().kickoff(
#     inputs={
#         "sentence": "I'm Nico and I like to ride my bicicle in Napoli",
#     }
# )