"""
routers/transcriptions.py — CRUD REST API for transcription records.

Endpoints:
  GET    /api/transcriptions           → paginated list with optional search
  POST   /api/transcriptions           → create new record
  GET    /api/transcriptions/{id}      → retrieve single record
  PATCH  /api/transcriptions/{id}      → update title or transcript
  DELETE /api/transcriptions/{id}      → delete record
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Transcription
from app.schemas import (
    TranscriptionCreate,
    TranscriptionOut,
    TranscriptionPage,
    TranscriptionUpdate,
)

router = APIRouter(prefix="/api/transcriptions", tags=["Transcriptions"])


# ── List / Search ─────────────────────────────────────────────────────────────

@router.get("", response_model=TranscriptionPage)
def list_transcriptions(
    search: str = Query(default="", description="Full-text search in title or transcript"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Return a paginated, optionally-searched list of transcriptions."""
    query = db.query(Transcription)

    if search.strip():
        pattern = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Transcription.title.ilike(pattern),
                Transcription.transcript.ilike(pattern),
            )
        )

    total = query.count()
    items = (
        query.order_by(Transcription.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return TranscriptionPage(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        has_next=(page * page_size) < total,
        has_prev=page > 1,
    )


# ── Create ────────────────────────────────────────────────────────────────────

@router.post("", response_model=TranscriptionOut, status_code=status.HTTP_201_CREATED)
def create_transcription(
    body: TranscriptionCreate,
    db: Session = Depends(get_db),
):
    """Save a completed transcription to the database."""
    record = Transcription(
        title=body.title,
        transcript=body.transcript,
        language=body.language,
        duration_seconds=body.duration_seconds,
        provider=body.provider,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


# ── Retrieve ──────────────────────────────────────────────────────────────────

@router.get("/{transcription_id}", response_model=TranscriptionOut)
def get_transcription(
    transcription_id: str,
    db: Session = Depends(get_db),
):
    """Return a single transcription by ID."""
    record = db.get(Transcription, transcription_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Transcription not found.")
    return record


# ── Update ────────────────────────────────────────────────────────────────────

@router.patch("/{transcription_id}", response_model=TranscriptionOut)
def update_transcription(
    transcription_id: str,
    body: TranscriptionUpdate,
    db: Session = Depends(get_db),
):
    """Partially update a transcription's title or text."""
    record = db.get(Transcription, transcription_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Transcription not found.")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)
    return record


# ── Delete ────────────────────────────────────────────────────────────────────

@router.delete("/{transcription_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transcription(
    transcription_id: str,
    db: Session = Depends(get_db),
):
    """Permanently delete a transcription."""
    record = db.get(Transcription, transcription_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Transcription not found.")
    db.delete(record)
    db.commit()
