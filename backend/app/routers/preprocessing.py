from fastapi import APIRouter
from app.services.preprocessing_service import PreprocessingService

router = APIRouter()


@router.post("/preprocess")
def preprocess_dataset():
    return PreprocessingService.start_preprocessing()