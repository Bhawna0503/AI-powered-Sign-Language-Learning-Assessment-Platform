"""
attempt_tracker.py

Stores every assessment attempt and provides
statistics for the learning session.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List


@dataclass
class Attempt:
    attempt_number: int
    expected_letter: str
    predicted_letter: str
    confidence: float
    gesture_accuracy: float
    inference_time_ms: float
    session_accuracy: float
    correct: bool
    timestamp: str


class AttemptTracker:

    def __init__(self):
        self.attempts: List[Attempt] = []

    # -----------------------------------------
    # Add Attempt
    # -----------------------------------------

    def add_attempt(
        self,
        expected_letter,
        predicted_letter,
        confidence,
        inference_time_ms,
        session_accuracy,
    ):

        attempt = Attempt(
            attempt_number=len(self.attempts) + 1,
            expected_letter=expected_letter,
            predicted_letter=predicted_letter,
            confidence=round(confidence, 3),
            gesture_accuracy=round(confidence * 100, 2),
            inference_time_ms=round(inference_time_ms, 2),
            session_accuracy=round(session_accuracy, 2),
            correct=(expected_letter == predicted_letter),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        self.attempts.append(attempt)

    # -----------------------------------------
    # Get All Attempts
    # -----------------------------------------

    def get_attempts(self):
        return [asdict(attempt) for attempt in self.attempts]

    # -----------------------------------------
    # Get Last Attempt
    # -----------------------------------------

    def get_last_attempt(self):

        if not self.attempts:
            return None

        return asdict(self.attempts[-1])

    # -----------------------------------------
    # Total Attempts
    # -----------------------------------------

    def total_attempts(self):
        return len(self.attempts)

    # -----------------------------------------
    # Correct Attempts
    # -----------------------------------------

    def correct_attempts(self):
        return sum(
            1 for attempt in self.attempts
            if attempt.correct
        )

    # -----------------------------------------
    # Incorrect Attempts
    # -----------------------------------------

    def incorrect_attempts(self):
        return self.total_attempts() - self.correct_attempts()

    # -----------------------------------------
    # Average Confidence
    # -----------------------------------------

    def average_confidence(self):

        if not self.attempts:
            return 0.0

        return round(

            sum(
                attempt.confidence
                for attempt in self.attempts
            )

            / len(self.attempts),

            3
        )

    # -----------------------------------------
    # Average Gesture Accuracy
    # -----------------------------------------

    def average_gesture_accuracy(self):

        if not self.attempts:
            return 0.0

        return round(

            sum(
                attempt.gesture_accuracy
                for attempt in self.attempts
            )

            / len(self.attempts),

            2
        )

    # -----------------------------------------
    # Average Response Time
    # -----------------------------------------

    def average_response_time(self):

        if not self.attempts:
            return 0.0

        return round(

            sum(
                attempt.inference_time_ms
                for attempt in self.attempts
            )

            / len(self.attempts),

            2
        )

    # -----------------------------------------
    # Accuracy Percentage
    # -----------------------------------------

    def accuracy_percentage(self):

        if not self.attempts:
            return 0.0

        return round(

            (self.correct_attempts() /
             self.total_attempts()) * 100,

            2
        )

    # -----------------------------------------
    # Clear Session
    # -----------------------------------------

    def clear(self):
        self.attempts.clear()

    # -----------------------------------------
    # Export Attempts
    # -----------------------------------------

    def export(self):

        return {

            "total_attempts": self.total_attempts(),

            "correct_attempts": self.correct_attempts(),

            "incorrect_attempts": self.incorrect_attempts(),

            "accuracy": self.accuracy_percentage(),

            "average_confidence": self.average_confidence(),

            "average_gesture_accuracy":
                self.average_gesture_accuracy(),

            "average_response_time":
                self.average_response_time(),

            "attempts": self.get_attempts()
        }