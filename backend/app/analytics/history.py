"""
history.py

Returns recent learning attempts.
"""

from typing import List, Dict


class History:
    """Handles recent practice history."""

    def __init__(self, attempts: List[Dict]):
        self.attempts = attempts

    def recent(self, limit: int = 10):
        """Return the most recent attempts."""
        return self.attempts[-limit:]

    def all(self):
        """Return all attempts."""
        return self.attempts