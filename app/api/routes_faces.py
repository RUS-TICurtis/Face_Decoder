from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from typing import Optional

from app.schemas.face import FaceAnalysisResponse, ImageUploadResponse, SemblanceComparisonResponse
from app.services.insightface_service import insightface_service
from app.services.resemblance_service import resemblance_service
from app.services.file_service import save_upload_file, resolve_file_path
from app.utils.image_utils import validate_image

router = APIRouter(prefix="/faces", tags=["Face Detection & Embeddings"])

@router.post("/detect/{file_id}", response_model=FaceAnalysisResponse)
async def detect_faces_by_id(
    file_id: str,
    padding_ratio: float = Query(0.15, ge=0.0, le=0.5, description="Padding percentage around face crop"),
):
    """
    Detect all faces within an already uploaded image using InsightFace.
    Extracts 5 facial landmarks, ArcFace embeddings, and saves cropped faces.
    """
    image_path = resolve_file_path(file_id)
    if not image_path:
        raise HTTPException(status_code=404, detail=f"Image with id '{file_id}' not found.")

    try:
        return insightface_service.detect_and_embed(
            image_path=image_path,
            file_id=file_id,
            padding_ratio=padding_ratio,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Face detection failed: {str(e)}")

from app.services.face_library_service import face_library_service

@router.post("/detect-and-crop", response_model=FaceAnalysisResponse)
async def upload_and_detect(
    file: UploadFile = File(...),
    padding_ratio: float = Query(0.15, ge=0.0, le=0.5),
):
    """
    Convenience endpoint: Ingests an image and immediately runs face detection,
    landmark extraction, and embedding generation in a single step.
    Also indexes detected faces into the Face Library.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="A valid filename is required.")

    if not validate_image(file.file):
        raise HTTPException(status_code=400, detail="Invalid or unsupported image binary.")

    file.file.seek(0)
    file_id, _, file_path, _, _, _ = save_upload_file(file)

    try:
        res = insightface_service.detect_and_embed(
            image_path=file_path,
            file_id=file_id,
            padding_ratio=padding_ratio,
        )
        
        # Automatically index faces into the library
        for face in res.faces:
            try:
                face_img_path = str(face.crop_path)
                if face_img_path and Path(face_img_path).exists():
                    face_library_service.index_face(face, file.filename, face_img_path)
            except Exception as index_err:
                print(f"Warning: Failed to index face {face.face_id}: {index_err}")
                
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection pipeline failed: {str(e)}")

@router.post("/compare", response_model=SemblanceComparisonResponse)
async def compare_faces(
    source_file: UploadFile = File(...),
    target_file: UploadFile = File(...)
):
    """
    Upload two images, extract embeddings for the primary face in each,
    and compare them to produce Score 1 (Identity) and Score 2 (Resemblance).
    """
    if not validate_image(source_file.file) or not validate_image(target_file.file):
        raise HTTPException(status_code=400, detail="Invalid image binary.")

    source_file.file.seek(0)
    target_file.file.seek(0)
    
    src_id, _, src_path, _, _, _ = save_upload_file(source_file)
    tgt_id, _, tgt_path, _, _, _ = save_upload_file(target_file)

    try:
        src_res = insightface_service.detect_and_embed(src_path, src_id)
        tgt_res = insightface_service.detect_and_embed(tgt_path, tgt_id)

        if not src_res.faces or not tgt_res.faces:
            raise HTTPException(status_code=400, detail="Could not detect a face in one or both images.")
            
        return resemblance_service.compare_faces(src_res.faces[0], tgt_res.faces[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")
