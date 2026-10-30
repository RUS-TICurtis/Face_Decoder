from typing import Optional
from sqlmodel import Field, SQLModel
import json

class Baseline(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    
    # Store lists/dicts as JSON strings in SQLite
    # 512-D float list
    archetype_centroid_json: str = Field(default="[]")
    
    # e.g., {"Regal": 70, "Approachable": 30}
    ground_truth_archetypes_json: str = Field(default="{}")
    
    # e.g., {"Cute": 80}
    ground_truth_aesthetics_json: str = Field(default="{}")
    
    @property
    def archetype_centroid(self) -> list[float]:
        return json.loads(self.archetype_centroid_json)
        
    @archetype_centroid.setter
    def archetype_centroid(self, value: list[float]):
        self.archetype_centroid_json = json.dumps(value)

    @property
    def ground_truth_archetypes(self) -> dict[str, int]:
        return json.loads(self.ground_truth_archetypes_json)
        
    @ground_truth_archetypes.setter
    def ground_truth_archetypes(self, value: dict[str, int]):
        self.ground_truth_archetypes_json = json.dumps(value)

    @property
    def ground_truth_aesthetics(self) -> dict[str, int]:
        return json.loads(self.ground_truth_aesthetics_json)
        
    @ground_truth_aesthetics.setter
    def ground_truth_aesthetics(self, value: dict[str, int]):
        self.ground_truth_aesthetics_json = json.dumps(value)
