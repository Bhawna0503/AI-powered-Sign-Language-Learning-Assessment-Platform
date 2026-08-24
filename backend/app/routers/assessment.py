from fastapi import UploadFile, File, HTTPException
import cv2
import numpy as np
from fastapi import APIRouter

from app.ai_engine.logger import logger
from app.services.assessment_service import AssessmentService

router = APIRouter(
    prefix="/assessment",
    tags=["Assessment"]
)

assessment_service = AssessmentService()


@router.post("/start/{lesson_id}")
def start_assessment(lesson_id: int):
    return assessment_service.start_practice(lesson_id)


@router.get("/camera")
def open_camera():
    return assessment_service.open_camera()


@router.get("/landmarks")
def extract_landmarks():
    return assessment_service.extract_landmarks()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    logger.info(f"Assessment prediction request received: {file.filename}")

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG and PNG images are allowed."
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    image = cv2.imdecode(
        np.frombuffer(contents, np.uint8),
        cv2.IMREAD_COLOR
    )

    if image is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid image format."
        )
    logger.info(f"Running assessment prediction for: {file.filename}")
    return assessment_service.predict(image)


@router.post("/end")
def end_session():
    return assessment_service.end_session()