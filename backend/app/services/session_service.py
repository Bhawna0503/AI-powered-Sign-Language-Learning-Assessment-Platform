from datetime import datetime
import uuid


class SessionService:
    def __init__(self):
        self.sessions = {}

    def start_session(self, lesson_id: int):
        session_id = str(uuid.uuid4())

        self.sessions[session_id] = {
            "session_id": session_id,
            "lesson_id": lesson_id,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "attempts": 0,
        }

        return self.sessions[session_id]

    def record_attempt(self, session_id: str):
        if session_id in self.sessions:
            self.sessions[session_id]["attempts"] += 1
            return self.sessions[session_id]

        return None

    def end_session(self, session_id: str):
        if session_id in self.sessions:
            self.sessions[session_id]["end_time"] = datetime.now().isoformat()
            return self.sessions[session_id]

        return None

    def get_session(self, session_id: str):
        return self.sessions.get(session_id)