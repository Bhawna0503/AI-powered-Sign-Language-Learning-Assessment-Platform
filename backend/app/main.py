from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.prediction import router as prediction_router
from app.api.lessons import router as lessons_router
from app.api.preprocessing import router as preprocessing_router

app = FastAPI(
    title="AI Sign Language Learning Assessment Platform",
    version="1.0.0",
    description="Backend API for Sign Language Learning Platform"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(health_router)
app.include_router(prediction_router)
app.include_router(lessons_router)
app.include_router(preprocessing_router)

# Root Endpoint
@app.get("/", tags=["Root"])
def root():
    return {
        "status": "running",
        "message": "AI Sign Language Learning Assessment Platform API",
        "documentation": "/docs"
    }