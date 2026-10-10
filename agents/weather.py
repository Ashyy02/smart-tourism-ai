import re


class WeatherAgent:

    def run(self, question):
        pattern = r"\b(?:weather|temperature|rain|forecast|climate)\b"
        return bool(re.search(pattern, question, re.IGNORECASE))