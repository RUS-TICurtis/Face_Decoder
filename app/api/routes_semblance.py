from fastapi import APIRouter, HTTPException
from app.schemas.face import (
    FaceAnalysisResponse,
    SemblanceComparisonRequest,
    SemblanceComparisonResponse,
)
from app.services.semblance_service import semblance_service

router = APIRouter(prefix="/semblance", tags=["Semblance & Affect Analysis"])

@router.get("/detect/{file_id}", response_model=FaceAnalysisResponse)
async def detect_face_and_affect(file_id: str):
    """
    Detects faces and extracts emotional affect / feeling scores from a previously uploaded image.
    """
    try:
        return semblance_service.detect_faces(file_id)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/compare", response_model=SemblanceComparisonResponse)
async def compare_facial_semblance(payload: SemblanceComparisonRequest):
    """
    Evaluates both geometric semblance and affective human feeling resonance
    between two facial subjects.
    """
    try:
        return semblance_service.compare_semblance(
            source_file_id=payload.source_file_id,
            target_file_id=payload.target_file_id,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")
