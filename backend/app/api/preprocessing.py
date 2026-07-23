from fastapi import APIRouter
from app.services.preprocessing_service import PreprocessingService

router = APIRouter()

@router.post("/preprocess")
def preprocess_dataset():

    service = PreprocessingService()

    result = service.run_preprocessing()

    return {
        "success": True,
        "message": "Dataset preprocessing completed.",
        "data": result
    }