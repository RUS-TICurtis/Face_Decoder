import json
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from datetime import datetime

from app.core.database import get_session
from app.models.scan_history import ScanHistory

router = APIRouter(prefix="/history", tags=["Scan History"])

class CreateScanHistoryRequest(BaseModel):
    person_name: str = Field(default="Anonymous Subject", description="Name of the scanned individual")
    avatar_crop_filename: str = Field(description="Filename of the cropped face avatar chip")
    source_filename: str = Field(default="live_capture.jpg", description="Original uploaded or captured image filename")
    vibe_data: Dict[str, Any] = Field(description="Full vibe analysis and regional drivers")
    affinity_data: Optional[Dict[str, Any]] = Field(default=None, description="Optional Score 4 affinity results")
    notes: Optional[str] = Field(default=None, description="Optional user notes")

class ScanHistoryResponse(BaseModel):
    id: str
    person_name: str
    avatar_crop_filename: str
    source_filename: str
    vibe_data: Dict[str, Any]
    affinity_data: Optional[Dict[str, Any]]
    notes: Optional[str]
    created_at: datetime

@router.post("/", response_model=ScanHistoryResponse)
def save_scan_history(payload: CreateScanHistoryRequest, session: Session = Depends(get_session)):
    """Save an analyzed face scan record with stats, avatar, and subject details."""
    record = ScanHistory(
        person_name=payload.person_name.strip() or "Anonymous Subject",
        avatar_crop_filename=payload.avatar_crop_filename,
        source_filename=payload.source_filename,
        vibe_data_json=json.dumps(payload.vibe_data),
        affinity_data_json=json.dumps(payload.affinity_data) if payload.affinity_data else None,
        notes=payload.notes,
        created_at=datetime.utcnow()
    )
    session.add(record)
    session.commit()
    session.refresh(record)

    return ScanHistoryResponse(
        id=record.id,
        person_name=record.person_name,
        avatar_crop_filename=record.avatar_crop_filename,
        source_filename=record.source_filename,
        vibe_data=record.vibe_data,
        affinity_data=record.affinity_data,
        notes=record.notes,
        created_at=record.created_at
    )

@router.get("/", response_model=List[ScanHistoryResponse])
def get_scan_history(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session)
):
    """Retrieve chronologically ordered scan history of analyzed individuals."""
    statement = select(ScanHistory).order_by(ScanHistory.created_at.desc()).offset(offset).limit(limit)
    records = session.exec(statement).all()

    return [
        ScanHistoryResponse(
            id=r.id,
            person_name=r.person_name,
            avatar_crop_filename=r.avatar_crop_filename,
            source_filename=r.source_filename,
            vibe_data=r.vibe_data,
            affinity_data=r.affinity_data,
            notes=r.notes,
            created_at=r.created_at
        )
        for r in records
    ]

@router.delete("/{record_id}")
def delete_scan_record(record_id: str, session: Session = Depends(get_session)):
    """Delete a scan record from history."""
    statement = select(ScanHistory).where(ScanHistory.id == record_id)
    record = session.exec(statement).first()
    if not record:
        raise HTTPException(status_code=404, detail="Scan record not found")
    session.delete(record)
    session.commit()
    return {"message": "Scan record deleted", "id": record_id}
