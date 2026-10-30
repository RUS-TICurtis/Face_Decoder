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

class LandmarkPoint(BaseModel):
    x: float
    y: float

class FacialLandmarks(BaseModel):
    right_eye: LandmarkPoint
    left_eye: LandmarkPoint
    nose_tip: LandmarkPoint
    mouth_right: LandmarkPoint
    mouth_left: LandmarkPoint

class FaceBoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)

class RegionalContributions(BaseModel):
    eyes: int = Field(default=0, ge=0, le=100)
    nose: int = Field(default=0, ge=0, le=100)
    mouth: int = Field(default=0, ge=0, le=100)
    jawline_symmetry: int = Field(default=0, ge=0, le=100)
    proportions: int = Field(default=0, ge=0, le=100)

class EmotionAffectProfile(BaseModel):
    """
    Affective and emotional sentiment breakdown representing human feelings
    and micro-expressions, as well as the new Explanation Engine components.
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
    # New Phase 5 fields
    perceptual_appeal: int = Field(
        default=50,
        ge=0,
        le=100,
        description="Score 3: Overall Perceptual Appeal (proxy for SCUT-FBP5500)"
    )
    explanation: str = Field(
        default="",
        description="Natural language summary of the similarity or aesthetic drivers."
    )
    regional_contributions: Optional[RegionalContributions] = None

class DetectedFace(BaseModel):
    face_id: str
    index: int = 0
    bbox: FaceBoundingBox
    landmarks: Optional[FacialLandmarks] = None
    confidence: float = 1.0
    crop_filename: Optional[str] = None
    crop_path: Optional[str] = None
    affect: Optional[EmotionAffectProfile] = None
    embedding: Optional[List[float]] = Field(default=None, description="512-D ArcFace embedding")

class FaceAnalysisResponse(BaseModel):
    file_id: str
    image_dimensions: Optional[ImageDimensions] = None
    total_faces: int
    faces: List[DetectedFace]

class SemblanceComparisonRequest(BaseModel):
    source_file_id: str
    target_file_id: str

class IdentitySimilarityScore(BaseModel):
    score: float = Field(ge=0.0, le=1.0, description="Normalized score 0-1, where 1 means exact match")
    distance: float = Field(description="Cosine distance between embeddings")
    is_same_person: bool = Field(description="True if score > 0.85 threshold")

class ResemblanceScore(BaseModel):
    score: float = Field(ge=0.0, le=1.0, description="Normalized visual resemblance score 0-1")
    distance: float = Field(description="Euclidean distance between embeddings")

class SemblanceComparisonResponse(BaseModel):
    source_file_id: str
    target_file_id: str
    identity: IdentitySimilarityScore
    resemblance: ResemblanceScore
