import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

class LLMService:

    def __init__(self):
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            model="meta-llama/llama-3.1-8b-instruct",
            temperature=0.3,
        )

    def ask(self, question):
        response = self.llm.invoke(question)
        return response.content