from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple

class VectorStoreAdapter(ABC):
    """
    Abstract Base Class for Vector Store implementations.
    Guarantees swappability between FAISS, Qdrant, Milvus, etc.
    """

    @abstractmethod
    def add_embedding(self, face_id: str, embedding: List[float], metadata: Dict[str, Any] = None) -> None:
        """Add a single embedding vector to the store with an associated ID and metadata."""
        pass

    @abstractmethod
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Search for the top_k most similar vectors.
        Returns a list of tuples containing (face_id, distance).
        """
        pass

    @abstractmethod
    def delete(self, face_id: str) -> None:
        """Remove a face embedding from the store."""
        pass

    @abstractmethod
    def save(self) -> None:
        """Persist the index to disk if applicable."""
        pass
