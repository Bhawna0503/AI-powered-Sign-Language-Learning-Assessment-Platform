from fastapi import APIRouter, HTTPException
from app.services.session_service import SessionService

router = APIRouter(
    prefix="/session",
    tags=["Session"]
)

session_service = SessionService()


@router.post("/start/{lesson_id}")
def start_session(lesson_id: int):
    return session_service.start_session(lesson_id)


@router.post("/attempt/{session_id}")
def record_attempt(session_id: str):
    session = session_service.record_attempt(session_id)

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


@router.post("/end/{session_id}")
def end_session(session_id: str):
    session = session_service.end_session(session_id)

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


@router.get("/{session_id}")
def get_session(session_id: str):
    session = session_service.get_session(session_id)

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return session