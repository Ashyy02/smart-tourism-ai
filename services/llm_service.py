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
            model="meta-llama/llama-3.1-8b-instruct",
            temperature=0.3,
        )

        self.rag = RAGLoader()
        self.rag.build_database()

        self.planner = PlannerAgent()
        self.hotel = HotelAgent()
        self.weather = WeatherAgent()
        self.knowledge = KnowledgeAgent()

    def ask(self, question):

        # -------------------------
        # Agent Selection
        # -------------------------

        if self.planner.run(question):

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

        elif self.hotel.run(question):

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

        elif self.weather.run(question):

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

        # -------------------------
        # RAG Search
        # -------------------------

        knowledge = self.rag.search(question)

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
"""

        response = self.llm.invoke(prompt)

        return category, knowledge, response.content