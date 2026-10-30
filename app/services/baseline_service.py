from typing import List, Dict, Optional
import numpy as np
from sqlmodel import Session, select
from fastapi import HTTPException
import uuid

from app.core.database import engine
from app.models.baseline import Baseline
from app.services.insightface_service import insightface_service
from app.schemas.face import DetectedFace

class BaselineService:
    def create_baseline(
        self, 
        name: str, 
        image_paths: List[str], 
        archetypes: Dict[str, int], 
        aesthetics: Dict[str, int]
    ) -> Baseline:
        """
        Process images to extract embeddings, compute the centroid,
        and save the baseline profile to the database.
        """
        embeddings = []
        for path in image_paths:
            # We generate a unique ID for each file for saving the cropped face
            file_id = f"baseline_{uuid.uuid4().hex[:8]}"
            res = insightface_service.detect_and_embed(path, file_id)
            if res.faces and len(res.faces) > 0:
                # We assume the first detected face is the primary subject
                if res.faces[0].embedding:
                    embeddings.append(res.faces[0].embedding)
        
        if not embeddings:
            raise ValueError("No faces detected in the provided baseline reference images.")
            
        # Compute centroid (mean of all embeddings)
        embeddings_array = np.array(embeddings)
        centroid = np.mean(embeddings_array, axis=0)
        centroid_list = centroid.tolist()
        
        # Save to database
        new_baseline = Baseline(
            name=name,
            archetype_centroid=centroid_list,
            ground_truth_archetypes=archetypes,
            ground_truth_aesthetics=aesthetics
        )
        
        with Session(engine) as session:
            session.add(new_baseline)
            session.commit()
            session.refresh(new_baseline)
            
        return new_baseline

    def get_all_baselines(self) -> List[Baseline]:
        with Session(engine) as session:
            statement = select(Baseline)
            results = session.exec(statement)
            return list(results)

    def get_baseline_by_id(self, baseline_id: int) -> Optional[Baseline]:
        with Session(engine) as session:
            return session.get(Baseline, baseline_id)

baseline_service = BaselineService()
