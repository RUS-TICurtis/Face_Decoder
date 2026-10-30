import os
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
import faiss

from app.core.config import settings
from .base import VectorStoreAdapter

class FaissAdapter(VectorStoreAdapter):
    """
    Local FAISS index implementation of VectorStoreAdapter.
    Uses L2 distance by default.
    """

    def __init__(self, index_path: Optional[str] = None, dim: int = 512):
        self.dim = dim
        self.index_path = index_path or str(settings.BASE_DIR / "storage" / "embeddings" / "faiss.index")
        self.mapping_path = str(self.index_path) + ".mapping.json"
        
        # FAISS only supports integer IDs natively, so we maintain a string -> int mapping
        self.id_to_int: Dict[str, int] = {}
        self.int_to_id: Dict[int, str] = {}
        self.current_max_id = 0
        
        self.index = None
        self._load_or_create_index()

    def _load_or_create_index(self):
        Path(self.index_path).parent.mkdir(parents=True, exist_ok=True)
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            if os.path.exists(self.mapping_path):
                with open(self.mapping_path, 'r') as f:
                    self.int_to_id = {int(k): v for k, v in json.load(f).items()}
                    self.id_to_int = {v: k for k, v in self.int_to_id.items()}
                    self.current_max_id = max(self.int_to_id.keys()) if self.int_to_id else 0
        else:
            # Create a flat L2 index wrapped in an IDMap to store our custom int IDs
            base_index = faiss.IndexFlatL2(self.dim)
            self.index = faiss.IndexIDMap(base_index)

    def add_embedding(self, face_id: str, embedding: List[float], metadata: Dict[str, Any] = None) -> None:
        if face_id in self.id_to_int:
            # FAISS doesn't support easy update, so we delete and re-add
            self.delete(face_id)
            
        self.current_max_id += 1
        internal_id = self.current_max_id
        self.id_to_int[face_id] = internal_id
        self.int_to_id[internal_id] = face_id
        
        vec = np.array([embedding], dtype=np.float32)
        faiss.normalize_L2(vec) # Normalize for cosine similarity approximation
        ids = np.array([internal_id], dtype=np.int64)
        
        self.index.add_with_ids(vec, ids)
        self.save()

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        if self.index.ntotal == 0:
            return []
            
        vec = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(vec)
        
        distances, indices = self.index.search(vec, top_k)
        
        results = []
        for i in range(len(indices[0])):
            internal_id = int(indices[0][i])
            if internal_id != -1 and internal_id in self.int_to_id:
                face_id = self.int_to_id[internal_id]
                dist = float(distances[0][i])
                results.append((face_id, dist))
                
        return results

    def delete(self, face_id: str) -> None:
        if face_id in self.id_to_int:
            internal_id = self.id_to_int[face_id]
            self.index.remove_ids(np.array([internal_id], dtype=np.int64))
            del self.id_to_int[face_id]
            del self.int_to_id[internal_id]
            self.save()

    def save(self) -> None:
        faiss.write_index(self.index, self.index_path)
        with open(self.mapping_path, 'w') as f:
            json.dump(self.int_to_id, f)

# Global singleton
faiss_adapter = FaissAdapter()
