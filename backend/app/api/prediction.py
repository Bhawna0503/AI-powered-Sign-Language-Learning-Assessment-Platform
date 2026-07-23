from fastapi import APIRouter

from app.services.gesture_service import GestureService
from app.schemas.prediction_schema import PredictionResponse

router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"]
)

gesture_service = GestureService()


@router.get("/")
def prediction_home():

    return {
        "message": "Prediction API Working"
    }


@router.post(
    "/predict",
    response_model=PredictionResponse
)
def predict():

    gesture_service.open_camera()

    gesture_service.extract_landmarks()

    result = gesture_service.predict()

    gesture_service.finish_session()

    return result