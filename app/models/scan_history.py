import uuid
import json
from datetime import datetime
from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field

class ScanHistory(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    person_name: str = Field(default="Anonymous Subject", index=True)
    avatar_crop_filename: str = Field(description="Filename of the cropped face avatar chip")
    source_filename: str = Field(description="Original uploaded image filename")
    
    # Store complete stats payload as JSON
    vibe_data_json: str = Field(default="{}", description="Vibe & Archetype scores from Explanation Engine")
    affinity_data_json: Optional[str] = Field(default=None, description="Optional Score 4 baseline affinity result")
    
    notes: Optional[str] = Field(default=None, description="Optional user annotation or tags")
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    @property
    def vibe_data(self) -> Dict[str, Any]:
        try:
            return json.loads(self.vibe_data_json)
        except Exception:
            return {}

    @vibe_data.setter
    def vibe_data(self, value: Dict[str, Any]):
        self.vibe_data_json = json.dumps(value)

    @property
    def affinity_data(self) -> Optional[Dict[str, Any]]:
        if not self.affinity_data_json:
            return None
        try:
            return json.loads(self.affinity_data_json)
        except Exception:
            return None

    @affinity_data.setter
    def affinity_data(self, value: Optional[Dict[str, Any]]):
        self.affinity_data_json = json.dumps(value) if value is not None else None
