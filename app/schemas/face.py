from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

class ImageDimensions(BaseModel):
    width: int
    height: int

class ImageUploadResponse(BaseModel):
    file_id: str
    original_filename: str
    stored_filename: str
    file_path: str
    format: str
    dimensions: ImageDimensions
    size_bytes: int
    status: str = "uploaded successfully"

class FaceBoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)

class EmotionAffectProfile(BaseModel):
    """
    Affective and emotional sentiment breakdown representing human feelings
    and micro-expressions.
    """
    primary_feeling: str
    valence: float = Field(
        default=0.0,
        ge=-1.0,
        le=1.0,
        description="Intrinsic attractiveness (+1) or aversiveness (-1) of the expression"
    )
    arousal: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Intensity/activation level of the emotion"
    )
    scores: Dict[str, float] = Field(
        default_factory=dict,
        description="Confidence scores per emotion archetype (e.g., joy, serenity, sorrow, tension, wonder, neutral)"
    )

class DetectedFace(BaseModel):
    face_id: str
    bbox: FaceBoundingBox
    crop_path: Optional[str] = None
    affect: Optional[EmotionAffectProfile] = None

class FaceAnalysisResponse(BaseModel):
    file_id: str
    total_faces: int
    faces: List[DetectedFace]

class SemblanceComparisonRequest(BaseModel):
    source_file_id: str
    target_file_id: str

class SemblanceComparisonResponse(BaseModel):
    source_file_id: str
    target_file_id: str
    structural_semblance: float = Field(
        description="Visual / geometric likeness score between faces (0.0 to 1.0)"
    )
    emotional_semblance: float = Field(
        description="Emotional and feeling semblance score between expressions (0.0 to 1.0)"
    )
    composite_semblance: float = Field(
        description="Combined semblance score weighting structural and emotional likeness (0.0 to 1.0)"
    )
    source_affect: Optional[EmotionAffectProfile] = None
    target_affect: Optional[EmotionAffectProfile] = None
    verdict: str
    notes: str
