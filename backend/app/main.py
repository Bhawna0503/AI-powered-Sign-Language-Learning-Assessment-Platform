from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routers.gesture import router as gesture_router
from app.routers.assessment import router as assessment_router
from app.routers.lessons import router as lessons_router
from app.routers.session import router as session_router
from app.routers import preprocessing
from app.ai_engine.logger import logger

app = FastAPI(title="AI Sign Language API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    logger.warning(
        f"Validation error on {request.method} {request.url}: {exc.errors()}"
    )

    return JSONResponse(
        status_code=422,
        content={
            "status": "validation_error",
            "message": "Invalid request data.",
            "details": exc.errors()
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    logger.warning(
        f"HTTP error {exc.status_code} on {request.method} {request.url}: {exc.detail}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        f"Internal server error on {request.method} {request.url}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error."
        }
    )

app.include_router(gesture_router)
app.include_router(assessment_router)
app.include_router(lessons_router)
app.include_router(session_router)
app.include_router(preprocessing.router)