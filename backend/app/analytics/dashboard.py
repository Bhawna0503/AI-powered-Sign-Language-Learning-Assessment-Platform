"""
dashboard.py

Builds the complete analytics dashboard.
"""

from app.analytics.statistics import Statistics
from app.analytics.history import History


class Dashboard:
    """Combines statistics and history."""

    def __init__(self, attempts):
        self.statistics = Statistics(attempts)
        self.history = History(attempts)

    def generate(self):
        return {
            "statistics": self.statistics.dashboard(),
            "recent_history": self.history.recent(10),
        }