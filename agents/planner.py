import re


class PlannerAgent:

    def run(self, question):
        question = question.lower()

        english_keywords = [
            "plan",
            "planning",
            "trip",
            "itinerary",
            "itineraries",
            "travel plan",
        ]

        sinhala_tamil_keywords = [
            "ගමන් සැලැස්ම",
            "සංචාරක සැලැස්ම",
            "සංචාර සැලැස්ම",
            "චාරිකා සැලැස්ම",
            "ගමනක් සැලසුම්",
            "සංචාරයක් සැලසුම්",
            "பயணத் திட்டம்",
            "பயண திட்டம்",
            "சுற்றுலா திட்டம்",
            "சுற்றுலாத் திட்டம்",
            "பயணத்திட்டம்",
        ]

        english_match = any(
            re.search(
                r"\b" + re.escape(keyword) + r"\b",
                question,
            )
            for keyword in english_keywords
        )

        sinhala_tamil_match = any(
            keyword in question
            for keyword in sinhala_tamil_keywords
        )

        return english_match or sinhala_tamil_match
