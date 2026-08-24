class PersonalizedFeedbackService:

    def __init__(self, progress_service, error_analysis):
        self.progress = progress_service
        self.error_analysis = error_analysis

    def generate(self):
        feedback = []

        return feedback

    def generate(self):
        feedback = []

        analysis = self.error_analysis.generate_analysis()

        for pair in analysis["most_confused_pairs"]:
            feedback.append(
                f"You often confuse {pair['pair']}. Practice this gesture again."
            )

        for letter in analysis["needs_revision"]:
            feedback.append(
                f"Revise alphabet {letter}. Your confidence is consistently low."
            )

        trend = analysis["performance_trend"]["trend"]

        if trend == "Improving":
            feedback.append("Great job! Your performance is improving.")

        elif trend == "Declining":
            feedback.append("Your recent performance has declined. Practice more before moving on.")

        else:
            feedback.append("Your performance is stable.")

        return feedback