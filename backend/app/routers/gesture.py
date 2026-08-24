from fastapi import APIRouter, UploadFile, File, HTTPException

import cv2
import numpy as np

from app.schemas.prediction import PredictionResponse
from app.services.gesture_service import GestureService


router = APIRouter(
    prefix="/gesture",
    tags=["Gesture"]
)


gesture_service = GestureService()


@router.post(
    "/predict",
    response_model=PredictionResponse
)
async def predict(
    file: UploadFile = File(...)
):

    # ==========================================================
    # 1. VALIDATE FILE TYPE
    # ==========================================================

    if file.content_type not in [
        "image/jpeg",
        "image/png"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Only JPEG and PNG images are allowed."
        )

    # ==========================================================
    # 2. READ IMAGE
    # ==========================================================

    contents = await file.read()

    if not contents:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # ==========================================================
    # 3. CONVERT BYTES -> NUMPY ARRAY
    # ==========================================================

    image_array = np.frombuffer(
        contents,
        dtype=np.uint8
    )

    # ==========================================================
    # 4. DECODE IMAGE
    # ==========================================================

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if image is None:

        raise HTTPException(
            status_code=400,
            detail="Invalid image format."
        )

    # ==========================================================
    # 5. RUN AI PREDICTION
    # ==========================================================

    try:

        result = gesture_service.predict(
            image
        )

        return result

    except Exception as exc:

        print(
            "GESTURE PREDICTION ERROR:",
            repr(exc)
        )

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(exc)}"
        )