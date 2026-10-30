import math
from typing import List, Dict, Optional, Tuple, Any
import numpy as np
from scipy.spatial.distance import cosine, euclidean
from pydantic import BaseModel, Field

from app.schemas.face import DetectedFace, IdentitySimilarityScore, ResemblanceScore, SemblanceComparisonResponse
from app.services.vector_store.qdrant_adapter import qdrant_adapter
from app.services.baseline_service import BaselineService
from app.core.database import get_session

class PersonalAffinityScore(BaseModel):
    score: float = Field(ge=0.0, le=1.0, description="Normalized score 0-1 against Baseline Centroid")
    distance: float = Field(description="Cosine distance between embedding and baseline centroid")

class ResemblanceService:
    """
    Service to calculate the 4-score model components.
    Currently implements Score 1 (Identity Similarity), Score 2 (Resemblance),
    and Score 4 (Personal Affinity).
    """

    def calculate_identity_similarity(self, emb1: List[float], emb2: List[float]) -> IdentitySimilarityScore:
        """
        Calculates Identity Similarity (Score 1) using cosine similarity on ArcFace embeddings.
        Returns a normalized score (0-1) where 1 means identical.
        """
        # scipy.spatial.distance.cosine returns distance, so similarity is 1 - distance
        dist = cosine(emb1, emb2)
        score = max(0.0, 1.0 - dist)
        
        # Generally, ArcFace cosine similarity > 0.4 to 0.5 indicates same person. 
        # But we normalized dist to 0-1. Let's use 0.5 as threshold for "same person"
        # in the raw distance, which corresponds to score > 0.5.
        return IdentitySimilarityScore(
            score=round(score, 4),
            distance=round(dist, 4),
            is_same_person=bool(score > 0.5)
        )

    def calculate_resemblance(self, emb1: List[float], emb2: List[float], face1: DetectedFace, face2: DetectedFace) -> ResemblanceScore:
        """
        Calculates Resemblance (Score 2) using Euclidean distance on embeddings 
        and optionally incorporating structural landmarks later.
        """
        # Convert to numpy arrays
        v1 = np.array(emb1)
        v2 = np.array(emb2)
        
        dist = euclidean(v1, v2)
        
        # Max euclidean distance between normalized vectors is 2.
        # So we can normalize to 0-1 scale.
        score = max(0.0, 1.0 - (dist / 2.0))
        
        return ResemblanceScore(
            score=round(score, 4),
            distance=round(dist, 4)
        )

    def calculate_affinity(self, face_embedding: List[float], baseline_centroid: List[float]) -> PersonalAffinityScore:
        """
        Calculates Personal Affinity (Score 4) using cosine similarity
        against a predefined baseline centroid.
        """
        dist = cosine(face_embedding, baseline_centroid)
        score = max(0.0, 1.0 - dist)
        
        return PersonalAffinityScore(
            score=round(score, 4),
            distance=round(dist, 4)
        )

    def compare_faces(self, face1: DetectedFace, face2: DetectedFace) -> SemblanceComparisonResponse:
        """
        Compare two faces and generate the SemblanceComparisonResponse.
        """
        if not face1.embedding or not face2.embedding:
            raise ValueError("Both faces must have embeddings generated to compare them.")
            
        identity = self.calculate_identity_similarity(face1.embedding, face2.embedding)
        resemblance = self.calculate_resemblance(face1.embedding, face2.embedding, face1, face2)
        
        return SemblanceComparisonResponse(
            source_file_id=face1.face_id,
            target_file_id=face2.face_id,
            identity=identity,
            resemblance=resemblance
        )

# Global singleton
resemblance_service = ResemblanceService()
