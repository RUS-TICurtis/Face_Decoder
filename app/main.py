from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes_upload import router as upload_router
from app.api.routes_semblance import router as semblance_router
from app.services.file_service import ensure_storage_directories

# Ensure filing system hierarchy exists on startup
ensure_storage_directories()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "An intelligent computer vision platform for Facial Recognition, "
        "Human Emotion & Affect Decomposition, and Semblance Likeness Analysis."
    )
)

# CORS configuration for web integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(upload_router, prefix=settings.API_V1_PREFIX)
app.include_router(semblance_router, prefix=settings.API_V1_PREFIX)
# Backward-compatibility for raw /upload
app.include_router(upload_router)

@app.get("/", tags=["System"])
async def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "docs_url": "/docs",
        "filing_system": {
            "raw_images": str(settings.RAW_IMAGES_DIR),
            "processed_faces": str(settings.PROCESSED_FACES_DIR),
            "embeddings": str(settings.EMBEDDINGS_DIR),
            "reports": str(settings.REPORTS_DIR),
        }
    }

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy"}