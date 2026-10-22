"""
models.py — SQLAlchemy ORM model for Transcription records.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Float, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Transcription(Base):
    """Represents one completed speech transcription session."""

    __tablename__ = "transcriptions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, default="Untitled Recording")
    transcript: Mapped[str] = mapped_column(Text, nullable=False, default="")
    language: Mapped[str | None] = mapped_column(String(20), nullable=True)
    duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    provider: Mapped[str] = mapped_column(String(50), nullable=False, default="faster_whisper")

    created_at: Mapped[datetime] = mapped_column(
        default=_utcnow,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Transcription id={self.id!r} title={self.title!r}>"
