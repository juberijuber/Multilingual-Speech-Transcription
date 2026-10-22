"""
speech/base.py — Abstract interface that every speech provider must implement.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class TranscriptionResult:
    """Normalised result returned by any speech provider."""
    transcript: str
    language: Optional[str]
    duration_seconds: Optional[float]
    provider: str
    is_mock: bool = False


class BaseSpeechProvider(ABC):
    """All speech providers must implement this interface."""

    @abstractmethod
    async def transcribe_audio(
        self,
        audio_bytes: bytes,
        *,
        language: Optional[str] = None,
        audio_format: str = "webm",
    ) -> TranscriptionResult:
        """
        Transcribe raw audio bytes and return a TranscriptionResult.

        Parameters
        ----------
        audio_bytes : bytes
            Raw audio data (e.g. WebM/Opus from the browser MediaRecorder).
        language : str, optional
            BCP-47 language code hint (e.g. "hi", "en").
            Pass None for auto-detection.
        audio_format : str
            Container format string for logging/debugging purposes.
        """
