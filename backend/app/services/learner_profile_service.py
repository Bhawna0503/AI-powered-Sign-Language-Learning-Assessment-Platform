from collections import defaultdict
from datetime import datetime


class LearnerProfileService:

    def __init__(self):
        self.sessions = 0
        self.total_attempts = 0

        self.mastery = defaultdict(float)
        self.correct_streak = defaultdict(int)
        self.incorrect_streak = defaultdict(int)
        self.confidence = defaultdict(list)
        self.last_practice = {}

    def update(self, expected, correct, confidence):
        self.total_attempts += 1

        if correct:
            self.correct_streak[expected] += 1
            self.incorrect_streak[expected] = 0
            self.mastery[expected] += 1
        else:
            self.incorrect_streak[expected] += 1
            self.correct_streak[expected] = 0
            self.mastery[expected] -= 1

        self.confidence[expected].append(confidence)
        self.last_practice[expected] = datetime.now()

    def average_confidence(self, letter):
        values = self.confidence[letter]
        if not values:
            return 0
        return sum(values) / len(values)

    def profile(self):
        return {
            "sessions": self.sessions,
            "total_attempts": self.total_attempts,
            "mastery": dict(self.mastery),
            "correct_streak": dict(self.correct_streak),
            "incorrect_streak": dict(self.incorrect_streak),
            "average_confidence": {
                letter: self.average_confidence(letter)
                for letter in self.confidence
            },
            "last_practice": {
                letter: str(time)
                for letter, time in self.last_practice.items()
            }
        }