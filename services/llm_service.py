import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from rag.rag_loader import RAGLoader
from agents.planner import PlannerAgent
from agents.hotel import HotelAgent
from agents.weather import WeatherAgent
from agents.knowledge import KnowledgeAgent

load_dotenv()


class LLMService:

    def __init__(self):
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            model="google/gemini-2.5-flash",
            temperature=0.3,
            max_tokens=1000,
        )

        self.rag = RAGLoader()
        self.rag.build_database()

        self.planner = PlannerAgent()
        self.hotel = HotelAgent()
        self.weather = WeatherAgent()
        self.knowledge = KnowledgeAgent()

    def prepare_search_question(self, question):
        # Limited aliases, not a general translation system.
        replacements = {
            "ඇල්ලට": "Ella",
            "ඇල්ල": "Ella",
            "ගමන් සැලැස්මක්": "travel plan",
            "ගමන් සැලැස්ම": "travel plan",
            "கண்டியில்": "Kandy",
            "ஹோட்டலை": "hotel",
            "ஹோட்டல்": "hotel",
        }

        search_question = question

        for original, english in replacements.items():
            search_question = search_question.replace(original, english)

        return search_question

    def ask(self, question):
        search_question = self.prepare_search_question(question)

        if self.planner.run(search_question):
            category = "Planner Agent"

            system_prompt = """
You are an expert Sri Lanka Travel Planner.

Create detailed travel itineraries.

Always include:
- Day by Day Plan
- Attractions
- Transportation
- Food Recommendations
- Estimated Budget
- Travel Tips

Respond professionally.
"""

        elif self.hotel.run(search_question):
            category = "Hotel Agent"

            system_prompt = """
You are a Sri Lanka Hotel Expert.

Recommend hotels based on the user's destination.

Include:
- Best Hotels
- Budget / Mid-range / Luxury
- Nearby Attractions
- Booking Tips

Respond professionally.
"""

        elif self.weather.run(search_question):
            category = "Weather Agent"

            system_prompt = """
You are a Sri Lanka Weather Assistant.

Answer only weather-related questions.

If live weather is unavailable,
clearly mention that you are providing general weather guidance.

Respond professionally.
"""

        else:
            category = "Knowledge Agent"

            system_prompt = """
You are a Sri Lanka Tourism Expert.

Answer questions about:
- Tourist Attractions
- History
- Culture
- Transportation
- Food
- Activities

Respond professionally.
"""

        # Retrieve using the normalized question.
        knowledge = self.rag.search(search_question)

        # Preserve the original question and its language.
        prompt = f"""
{system_prompt}

Relevant Tourism Knowledge:

{knowledge}

User Question:

{question}

Instructions:

1. Use the tourism knowledge whenever relevant.
2. If the knowledge is insufficient, use your own knowledge.
3. Keep the answer clear and well structured.
4. Use bullet points where appropriate.
5. Answer in the same language as the user's original question.
   If the question is in Sinhala, write the entire answer in clear Sinhala.
   If the question is in Tamil, write the entire answer in clear Tamil.
   If the question is in English, write the answer in English.
   Keep proper place names in English where helpful.
"""

        response = self.llm.invoke(prompt)

        return category, knowledge, response.content
