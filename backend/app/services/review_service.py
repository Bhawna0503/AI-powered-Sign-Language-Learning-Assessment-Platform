class ReviewService:

    def __init__(self, progress):
        self.progress = progress

    def generate_review(self):
        return {
            "overall_score": round(self.progress.accuracy(), 2),
            "correct": self.progress.correct_attempts(),
            "incorrect": self.progress.incorrect_attempts(),
            "average_confidence": round(self.progress.average_confidence(), 2),
            "strongest_gesture": self.progress.strongest_alphabet(),
            "weakest_gesture": self.progress.weakest_alphabet(),
            "most_common_mistake": self.progress.most_mistaken(),
            "history": self.progress.recent_history()
        }