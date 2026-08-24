from datetime import datetime
from collections import Counter


class ProgressService:
    def __init__(self):
        print("ProgressService initialized")
        self.history = []

    def add_attempt(
        self,
        expected,
        predicted,
        correct,
        confidence,
        inference_time
    ):
        self.history.append({
            "expected": expected,
            "predicted": predicted,
            "correct": correct,
            "confidence": confidence,
            "inference_time": inference_time,
            "timestamp": datetime.now()
        })

    def total_attempts(self):
        return len(self.history)

    def accuracy(self):
        if not self.history:
            return 0

        correct = sum(item["correct"] for item in self.history)
        return (correct / len(self.history)) * 100

    def average_confidence(self):
        if not self.history:
            return 0

        return sum(item["confidence"] for item in self.history) / len(self.history)

    def average_response_time(self):
        if not self.history:
            return 0

        return sum(item["inference_time"] for item in self.history) / len(self.history)

    def strongest_alphabet(self):
        if not self.history:
            return "N/A"

        best = max(self.history, key=lambda item: item["confidence"])
        return best["expected"]

    def weakest_alphabet(self):
        if not self.history:
            return "N/A"

        worst = min(self.history, key=lambda item: item["confidence"])
        return worst["expected"]

    def most_mistaken(self):
        mistakes = [
            item["expected"]
            for item in self.history
            if not item["correct"]
        ]

        if not mistakes:
            return "None"

        return Counter(mistakes).most_common(1)[0][0]

    def correct_attempts(self):
        return sum(item["correct"] for item in self.history)

    def incorrect_attempts(self):
        return self.total_attempts() - self.correct_attempts()
    def recent_history(self, limit=5):
        """
        Return the most recent assessment attempts.
        """
        return self.history[-limit:]