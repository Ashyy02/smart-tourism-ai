import re


class WeatherAgent:

    def run(self, question):
        question = question.lower()

        english_pattern = (
            r"\b(?:weather|temperature|temperatures|"
            r"rain|raining|rainy|rainfall|"
            r"forecast|forecasts|climate|humidity)\b"
        )

        sinhala_tamil_keywords = [
            "කාලගුණ",
            "උෂ්ණත්ව",
            "වැස්ස",
            "වහින",
            "වර්ෂාව",
            "වර්ෂාපතන",
            "ආර්ද්‍රතාව",
            "வானிலை",
            "வெப்பநிலை",
            "மழை",
            "காலநிலை",
            "ஈரப்பதம்",
        ]

        english_match = bool(
            re.search(english_pattern, question)
        )

        sinhala_tamil_match = any(
            keyword in question
            for keyword in sinhala_tamil_keywords
        )

        return english_match or sinhala_tamil_match
