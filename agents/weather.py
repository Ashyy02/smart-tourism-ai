class WeatherAgent:

    def run(self, question):

        keywords = [
            "weather",
            "temperature",
            "rain",
            "forecast",
            "climate"
        ]

        question = question.lower()

        return any(word in question for word in keywords)