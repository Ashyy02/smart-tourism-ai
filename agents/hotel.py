class HotelAgent:

    def run(self, question):

        keywords = [
            "hotel",
            "stay",
            "accommodation",
            "resort",
            "guest house"
        ]

        question = question.lower()

        return any(word in question for word in keywords)