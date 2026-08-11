"""
statistics.py

Calculates statistics for the Student Progress Dashboard.
"""

from collections import Counter


class Statistics:
    """Calculates learning statistics."""

    def __init__(self, attempts):
        self.attempts = attempts

    def total_attempts(self):
        return len(self.attempts)

    def correct_attempts(self):
        return sum(1 for a in self.attempts if a["correct"])

    def incorrect_attempts(self):
        return self.total_attempts() - self.correct_attempts()

    def accuracy(self):
        if self.total_attempts() == 0:
            return 0.0

        return round(
            (self.correct_attempts() / self.total_attempts()) * 100,
            2
        )

    def average_confidence(self):
        if not self.attempts:
            return 0.0

        return round(
            sum(a["confidence"] for a in self.attempts)
            / len(self.attempts),
            2
        )

    def strongest_letters(self):
        correct = [
            a["expected_letter"]
            for a in self.attempts
            if a["correct"]
        ]

        return Counter(correct).most_common(5)

    def weakest_letters(self):
        incorrect = [
            a["expected_letter"]
            for a in self.attempts
            if not a["correct"]
        ]

        return Counter(incorrect).most_common(5)

    def dashboard(self):
        return {
            "total_attempts": self.total_attempts(),
            "correct_attempts": self.correct_attempts(),
            "incorrect_attempts": self.incorrect_attempts(),
            "accuracy": self.accuracy(),
            "average_confidence": self.average_confidence(),
            "strongest_letters": self.strongest_letters(),
            "weakest_letters": self.weakest_letters(),
        }