import re


class HotelAgent:

    def run(self, question):
        question = question.lower()

        english_keywords = [
            "hotel",
            "hotels",
            "stay",
            "staying",
            "accommodation",
            "resort",
            "resorts",
            "guest house",
            "guesthouse",
            "hostel",
            "hostels",
            "lodging",
        ]

        sinhala_tamil_keywords = [
            "හෝටල්",
            "හොටෙල්",
            "නවාතැන්",
            "නවාතැන",
            "නවතින්න",
            "නැවතීමට",
            "හෝස්ටල්",
            "ගෙස්ට් හවුස්",
            "ஹோட்டல்",
            "விடுதி",
            "தங்குமிடம்",
            "தங்குமிட",
            "தங்குவதற்கு",
            "தங்குவதற்கான",
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
