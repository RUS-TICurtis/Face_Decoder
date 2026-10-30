import os
import uuid
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

from app.core.config import settings
from .base import VectorStoreAdapter

class QdrantAdapter(VectorStoreAdapter):
    """
    Qdrant implementation of VectorStoreAdapter using local disk mode.
    """

    def __init__(self, collection_name: str = "faces", dim: int = 512):
        self.collection_name = collection_name
        self.dim = dim
        self.storage_path = str(settings.BASE_DIR / "storage" / "qdrant")
        
        # Ensure directory exists
        Path(self.storage_path).mkdir(parents=True, exist_ok=True)
        
        # Initialize local Qdrant
        self.client = QdrantClient(path=self.storage_path)
        
        self._ensure_collection()

    def _ensure_collection(self):
        # Check if collection exists
        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)
        
        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.dim, distance=Distance.COSINE),
            )

    def _ensure_valid_uuid(self, point_id: str) -> str:
        """Convert arbitrary string IDs to a valid RFC 4122 UUID format for Qdrant."""
        try:
            return str(uuid.UUID(point_id))
        except (ValueError, AttributeError):
            return str(uuid.uuid5(uuid.NAMESPACE_DNS, point_id))

    def add_embedding(self, face_id: str, embedding: List[float], metadata: Dict[str, Any] = None) -> None:
        """
        Add an embedding to Qdrant. Ensures ID is a compliant UUID format.
        """
        valid_id = self._ensure_valid_uuid(face_id)
        point_payload = dict(metadata or {})
        point_payload["original_face_id"] = face_id

        point = PointStruct(
            id=valid_id,
            vector=embedding,
            payload=point_payload
        )
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Search for top_k similar vectors. Returns list of (face_id, score).
        Qdrant returns similarity score directly, where higher is better for COSINE.
        """
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k
        )
        
        results = []
        for hit in search_result:
            orig_id = (hit.payload or {}).get("original_face_id", str(hit.id))
            results.append((orig_id, hit.score))
        return results

    def delete(self, face_id: str) -> None:
        """
        Delete an embedding by its ID.
        """
        valid_id = self._ensure_valid_uuid(face_id)
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=[valid_id]
        )

    def save(self) -> None:
        """
        No-op. Qdrant saves automatically in local disk mode.
        """
        pass

# Global singleton
qdrant_adapter = QdrantAdapter()
