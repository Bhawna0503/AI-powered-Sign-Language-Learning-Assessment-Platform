class FeedbackGenerator:

    def generate(self, rules):
        if not rules:
            return {
                "status": "Correct",
                "messages": [
                    "Excellent! Your gesture was performed correctly."
                ]
            }

        return {
            "status": "Needs Improvement",
            "messages": [rule["message"] for rule in rules]
        }