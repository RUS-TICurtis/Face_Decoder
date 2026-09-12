from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from typing import Optional

from app.schemas.face import FaceAnalysisResponse, ImageUploadResponse
from app.services.face_detection_service import face_detection_service
from app.services.file_service import save_upload_file, resolve_file_path
from app.utils.image_utils import validate_image

router = APIRouter(prefix="/faces", tags=["Face Detection & Cropping"])

@router.post("/detect/{file_id}", response_model=FaceAnalysisResponse)
async def detect_faces_by_id(
    file_id: str,
    padding_ratio: float = Query(0.15, ge=0.0, le=0.5, description="Padding percentage around face crop"),
    score_threshold: float = Query(0.6, ge=0.1, le=1.0, description="Minimum confidence threshold"),
):
    """
    Detect all faces within an already uploaded image.
    Extracts 5 facial landmarks (eyes, nose, mouth corners) and saves cropped faces
    into the storage/processed_faces/ directory.
    """
    image_path = resolve_file_path(file_id)
    if not image_path:
        raise HTTPException(status_code=404, detail=f"Image with id '{file_id}' not found.")

    try:
        return face_detection_service.detect_and_crop(
            image_path=image_path,
            file_id=file_id,
            padding_ratio=padding_ratio,
            score_threshold=score_threshold,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Face detection failed: {str(e)}")

@router.post("/detect-and-crop", response_model=FaceAnalysisResponse)
async def upload_and_detect(
    file: UploadFile = File(...),
    padding_ratio: float = Query(0.15, ge=0.0, le=0.5),
    score_threshold: float = Query(0.6, ge=0.1, le=1.0),
):
    """
    Convenience endpoint: Ingests an image and immediately runs face detection,
    landmark extraction, and face cropping in a single step.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="A valid filename is required.")

    if not validate_image(file.file):
        raise HTTPException(status_code=400, detail="Invalid or unsupported image binary.")

    file.file.seek(0)
    file_id, _, file_path, _, _, _ = save_upload_file(file)

    try:
        return face_detection_service.detect_and_crop(
            image_path=file_path,
            file_id=file_id,
            padding_ratio=padding_ratio,
            score_threshold=score_threshold,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection pipeline failed: {str(e)}")
