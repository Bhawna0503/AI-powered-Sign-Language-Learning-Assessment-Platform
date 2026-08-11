"""
lesson_manager.py

Manages the learning lesson flow using the AlphabetProvider.
"""

from app.learning.alphabet_provider import AlphabetProvider


class LessonManager:
    """Controls the current learning lesson."""

    def __init__(self):
        self.provider = AlphabetProvider()
        self.practice_started = False

    def start_practice(self):
        """Start a new practice session."""
        self.practice_started = True
        self.provider.reset()

    def get_current_letter(self):
        """Return the current alphabet."""
        return self.provider.get_current_letter()

    def next_letter(self):
        """Move to the next alphabet."""
        return self.provider.get_next_letter()

    def previous_letter(self):
        """Move to the previous alphabet."""
        return self.provider.get_previous_letter()

    def select_letter(self, letter: str):
        """Select a specific alphabet."""
        return self.provider.select_letter(letter)

    def restart(self):
        """Restart the lesson from A."""
        self.provider.reset()

    def lesson_completed(self):
        """Check if the lesson reached the last alphabet."""
        return self.provider.is_last_letter()

    def get_status(self):
        """Return current lesson information."""
        return {
            "practice_started": self.practice_started,
            "current_letter": self.provider.get_current_letter(),
            "completed": self.provider.is_last_letter()
        }