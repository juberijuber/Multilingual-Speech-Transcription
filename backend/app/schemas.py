"""
schemas.py — Pydantic v2 request/response schemas for the REST API.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ── Transcription ─────────────────────────────────────────────────────────────

class TranscriptionCreate(BaseModel):
    title: str = Field(default="Untitled Recording", max_length=255)
    transcript: str = Field(default="")
    language: Optional[str] = Field(default=None, max_length=20)
    duration_seconds: Optional[float] = Field(default=None, ge=0)
    provider: str = Field(default="faster_whisper", max_length=50)


class TranscriptionUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=255)
    transcript: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default=None, max_length=20)


class TranscriptionOut(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    title: str
    transcript: str
    language: Optional[str]
    duration_seconds: Optional[float]
    provider: str
    created_at: datetime
    updated_at: datetime


class TranscriptionPage(BaseModel):
    """Paginated list of transcriptions."""
    items: list[TranscriptionOut]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool


# ── Speech Processing ─────────────────────────────────────────────────────────

class TranscribeResponse(BaseModel):
    """Response from the /transcribe endpoint (file upload)."""
    transcript: str
    language: str | None
    duration_seconds: float | None
    provider: str
    is_mock: bool = False
