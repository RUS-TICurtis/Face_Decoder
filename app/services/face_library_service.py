import uuid
import imagehash
from PIL import Image
from typing import List, Optional, Tuple, Dict, Any
from sqlmodel import Session, select
from datetime import datetime

from app.core.database import engine
from app.models.face_record import FaceRecord
from app.schemas.face import DetectedFace
from app.services.vector_store.qdrant_adapter import qdrant_adapter

class FaceLibraryService:
    def __init__(self):
        self.vector_store = qdrant_adapter

    def compute_phash(self, image_path: str) -> str:
        """Compute perceptual hash of an image."""
        try:
            img = Image.open(image_path)
            return str(imagehash.phash(img))
        except Exception as e:
            print(f"Error computing phash for {image_path}: {e}")
            # Fallback to a random string if hashing fails (shouldn't happen on valid images)
            return str(uuid.uuid4())

    def index_face(self, face: DetectedFace, source_image_name: str, face_image_path: str) -> FaceRecord:
        """
        Check if a face is a duplicate. If not, index it in Qdrant and save to SQLite.
        Returns the FaceRecord.
        """
        if not face.embedding:
            raise ValueError("Face must have an embedding to be indexed.")

        # 1. Deduplication using phash
        phash_val = self.compute_phash(face_image_path)
        
        with Session(engine) as session:
            # Check if this phash already exists
            statement = select(FaceRecord).where(FaceRecord.phash == phash_val)
            existing = session.exec(statement).first()
            if existing:
                # Already indexed, return existing
                return existing

            # 2. Not a duplicate. Save to SQLite
            record = FaceRecord(
                id=face.face_id,
                filename=face.crop_filename,
                source_image=source_image_name,
                phash=phash_val
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            
            # 3. Add to Qdrant
            metadata = {
                "source_image": source_image_name,
                "filename": face.crop_filename
            }
            self.vector_store.add_embedding(face.face_id, face.embedding, metadata)
            
            return record

    def get_all_faces(self, limit: int = 50, offset: int = 0) -> List[FaceRecord]:
        """Retrieve paginated face records from SQLite."""
        with Session(engine) as session:
            statement = select(FaceRecord).order_by(FaceRecord.created_at.desc()).offset(offset).limit(limit)
            return session.exec(statement).all()

    def search_lookalikes(self, query_embedding: List[float], top_k: int = 12) -> List[Dict[str, Any]]:
        """
        Search for lookalikes in Qdrant, and join with SQLite data.
        Returns a list of dicts with score and record data.
        """
        # Search Qdrant
        results = self.vector_store.search(query_embedding, top_k=top_k)
        
        if not results:
            return []
            
        # Get face_ids
        face_ids = [res[0] for res in results]
        score_map = {res[0]: res[1] for res in results}
        
        # Fetch records from SQLite
        with Session(engine) as session:
            statement = select(FaceRecord).where(FaceRecord.id.in_(face_ids))
            records = session.exec(statement).all()
            
            # Combine and sort
            combined = []
            for record in records:
                combined.append({
                    "record": record,
                    "similarity": round(score_map[record.id] * 100, 2) # Convert to percentage
                })
                
            # Sort by similarity descending
            combined.sort(key=lambda x: x["similarity"], reverse=True)
            return combined

face_library_service = FaceLibraryService()
