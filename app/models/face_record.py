from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
import uuid

class FaceRecord(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    filename: str = Field(description="The unique filename of the cropped face chip (e.g. uuid.jpg)")
    source_image: str = Field(description="The filename of the original uploaded image")
    phash: str = Field(index=True, description="Perceptual hash (phash) for duplicate detection")
    created_at: datetime = Field(default_factory=datetime.utcnow)
