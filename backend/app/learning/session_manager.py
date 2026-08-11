"""
session_manager.py

Tracks the current learning session statistics.
"""

from datetime import datetime


class SessionManager:
    """Stores statistics for the current learning session."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset the session."""
        self.total_attempts = 0
        self.correct_attempts = 0
        self.incorrect_attempts = 0
        self.session_start = datetime.now()
        self.session_end = None

    def record_attempt(self, correct: bool):
        """Update statistics after each prediction."""
        self.total_attempts += 1

        if correct:
            self.correct_attempts += 1
        else:
            self.incorrect_attempts += 1

    def end_session(self):
        """Mark the session as finished."""
        self.session_end = datetime.now()

    def get_accuracy(self):
        """Return current accuracy percentage."""
        if self.total_attempts == 0:
            return 0.0

        return round(
            (self.correct_attempts / self.total_attempts) * 100,
            2
        )

    def get_statistics(self):
        """Return all session statistics."""
        return {
            "total_attempts": self.total_attempts,
            "correct_attempts": self.correct_attempts,
            "incorrect_attempts": self.incorrect_attempts,
            "accuracy": self.get_accuracy(),
            "session_start": self.session_start,
            "session_end": self.session_end
        }