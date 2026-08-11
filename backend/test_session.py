from app.learning.session_manager import SessionManager

session = SessionManager()

session.record_attempt(True)
session.record_attempt(True)
session.record_attempt(False)
session.record_attempt(True)

print(session.get_statistics())

session.end_session()

print(session.get_statistics())