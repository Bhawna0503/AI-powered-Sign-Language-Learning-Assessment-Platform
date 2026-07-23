import uuid
from datetime import datetime


class SessionService:

    def __init__(self):
        self.sessions = []

    def start_session(self, lesson_id: int):

        session = {
            "session_id": str(uuid.uuid4()),
            "lesson_id": lesson_id,
            "start_time": str(datetime.now()),
            "end_time": None,
            "attempts": 0
        }

        self.sessions.append(session)

        return session

    def end_session(self, session_id: str):

        for session in self.sessions:

            if session["session_id"] == session_id:
                session["end_time"] = str(datetime.now())
                return session

        return None

    def increase_attempt(self, session_id: str):

        for session in self.sessions:

            if session["session_id"] == session_id:
                session["attempts"] += 1
                return session

        return None

    def get_all_sessions(self):
        return self.sessions