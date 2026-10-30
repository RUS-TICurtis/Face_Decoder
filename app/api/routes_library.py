from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from typing import List, Dict, Any
from app.services.face_library_service import face_library_service
from app.services.insightface_service import insightface_service
from app.services.file_service import save_upload_file
from app.utils.image_utils import validate_image
from app.models.face_record import FaceRecord

router = APIRouter(prefix="/library", tags=["Face Library"])

@router.get("/", response_model=List[FaceRecord])
async def list_faces(limit: int = 50, offset: int = 0):
    """List paginated faces from the Face Library."""
    try:
        return face_library_service.get_all_faces(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search")
async def search_lookalikes(file: UploadFile = File(...), top_k: int = 12):
    """Upload a face and find top_k most similar faces in the Face Library."""
    if not validate_image(file.file):
        raise HTTPException(status_code=400, detail="Invalid image.")
        
    file.file.seek(0)
    file_id, _, file_path, _, _, _ = save_upload_file(file)
    
    try:
        # Detect and extract embedding
        detect_res = insightface_service.detect_and_embed(file_path, file_id)
        if not detect_res.faces:
            raise HTTPException(status_code=400, detail="No face detected in the image.")
            
        target_face = detect_res.faces[0]
        
        # Search Library
        results = face_library_service.search_lookalikes(target_face.embedding, top_k=top_k)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
