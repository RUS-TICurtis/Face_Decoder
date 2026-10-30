from typing import List, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
import json

from app.services.baseline_service import baseline_service
from app.services.resemblance_service import resemblance_service, PersonalAffinityScore
from app.services.insightface_service import insightface_service
from app.services.file_service import save_upload_file
from app.utils.image_utils import validate_image

from pydantic import BaseModel

router = APIRouter(prefix="/baselines", tags=["Baselines & Ground Truth"])

class BaselineResponse(BaseModel):
    id: int
    name: str
    ground_truth_archetypes: dict
    ground_truth_aesthetics: dict

class BaselineAnalysisResponse(BaseModel):
    baseline: BaselineResponse
    affinity: PersonalAffinityScore

@router.post("/", response_model=BaselineResponse)
async def create_baseline(
    name: str = Form(...),
    archetypes: str = Form(..., description="JSON string of archetypes"),
    aesthetics: str = Form(..., description="JSON string of aesthetics"),
    files: List[UploadFile] = File(...)
):
    try:
        archetypes_dict = json.loads(archetypes)
        aesthetics_dict = json.loads(aesthetics)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON for archetypes or aesthetics")

    image_paths = []
    for file in files:
        if not validate_image(file.file):
            continue
        file.file.seek(0)
        _, _, file_path, _, _, _ = save_upload_file(file)
        image_paths.append(file_path)

    if not image_paths:
        raise HTTPException(status_code=400, detail="No valid images uploaded.")

    try:
        new_baseline = baseline_service.create_baseline(
            name=name,
            image_paths=image_paths,
            archetypes=archetypes_dict,
            aesthetics=aesthetics_dict
        )
        
        return BaselineResponse(
            id=new_baseline.id,
            name=new_baseline.name,
            ground_truth_archetypes=new_baseline.ground_truth_archetypes,
            ground_truth_aesthetics=new_baseline.ground_truth_aesthetics
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[BaselineResponse])
async def get_baselines():
    baselines = baseline_service.get_all_baselines()
    return [
        BaselineResponse(
            id=b.id,
            name=b.name,
            ground_truth_archetypes=b.ground_truth_archetypes,
            ground_truth_aesthetics=b.ground_truth_aesthetics
        ) for b in baselines
    ]

@router.post("/{baseline_id}/analyze", response_model=BaselineAnalysisResponse)
async def analyze_against_baseline(
    baseline_id: int,
    file: UploadFile = File(...)
):
    """
    Takes a new face image and compares it to the specified Baseline's centroid
    to produce Score 4 (Personal Affinity).
    """
    if not validate_image(file.file):
        raise HTTPException(status_code=400, detail="Invalid image binary.")
        
    baseline = baseline_service.get_baseline_by_id(baseline_id)
    if not baseline:
        raise HTTPException(status_code=404, detail="Baseline not found.")

    file.file.seek(0)
    file_id, _, file_path, _, _, _ = save_upload_file(file)

    try:
        res = insightface_service.detect_and_embed(file_path, file_id)
        if not res.faces or not res.faces[0].embedding:
            raise HTTPException(status_code=400, detail="No face detected in image.")
            
        face_emb = res.faces[0].embedding
        affinity = resemblance_service.calculate_affinity(face_emb, baseline.archetype_centroid)
        
        return BaselineAnalysisResponse(
            baseline=BaselineResponse(
                id=baseline.id,
                name=baseline.name,
                ground_truth_archetypes=baseline.ground_truth_archetypes,
                ground_truth_aesthetics=baseline.ground_truth_aesthetics
            ),
            affinity=affinity
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
