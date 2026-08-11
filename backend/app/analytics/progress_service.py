"""
progress_service.py

Provides progress information from the learning module.
"""

from app.learning.assessment_service import AssessmentService


class ProgressService:
    """Returns student progress information."""

    def __init__(self, assessment_service: AssessmentService):
        self.assessment = assessment_service

    def get_progress(self):
        """Return session progress."""

        session = self.assessment.get_session_statistics()
        attempts = self.assessment.get_attempt_history()

        return {
            "session": session,
            "attempts": attempts,
            "total_attempts": len(attempts)
        }