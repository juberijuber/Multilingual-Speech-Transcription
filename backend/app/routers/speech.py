"""
routers/speech.py — Speech transcription endpoint.

POST /api/speech/transcribe
  Accepts a multipart audio file upload, passes it to the configured
  speech provider, and returns the transcript text.

  The frontend records audio via the browser MediaRecorder API (WebM/Opus),
  stops the recording, then POSTs the complete blob here. The transcript
  is returned and the frontend may then call POST /api/transcriptions to
  persist it.
"""

import logging
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.schemas import TranscribeResponse
from app.speech.base import BaseSpeechProvider
from app.speech.provider_factory import get_speech_provider

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/speech", tags=["Speech"])

# Maximum accepted upload size: 50 MB
MAX_AUDIO_BYTES = 50 * 1024 * 1024


@router.get("/provider-info")
def provider_info(provider: BaseSpeechProvider = Depends(get_speech_provider)):
    """Return metadata about the currently active speech provider."""
    is_mock = provider.__class__.__name__ == "MockSpeechProvider"
    return {
        "provider": "mock" if is_mock else "faster_whisper",
        "is_mock": is_mock,
        "supported_languages": _get_supported_languages(),
        "note": (
            "⚠️ Demo mode — no real speech recognition."
            if is_mock
            else "Faster-Whisper is active. 99 languages supported."
        ),
    }


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(
    audio: Annotated[UploadFile, File(description="Audio file recorded by the browser")],
    language: Annotated[
        Optional[str],
        Form(description="BCP-47 language hint, e.g. 'hi' or 'en'. Omit for auto-detect."),
    ] = None,
    provider: BaseSpeechProvider = Depends(get_speech_provider),
):
    """
    Transcribe an uploaded audio file.

    - **audio**: WebM/Opus blob from MediaRecorder (other formats accepted too).
    - **language**: Optional language hint. Leave blank for auto-detection.
    """
    audio_bytes = await audio.read()

    if not audio_bytes:
        raise HTTPException(status_code=422, detail="Uploaded audio file is empty.")

    if len(audio_bytes) > MAX_AUDIO_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Audio file too large. Maximum allowed size is {MAX_AUDIO_BYTES // (1024*1024)} MB.",
        )

    # Determine container format from content-type header
    content_type = audio.content_type or ""
    audio_format = "webm"
    if "ogg" in content_type:
        audio_format = "ogg"
    elif "mp4" in content_type or "mpeg" in content_type:
        audio_format = "mp4"
    elif "wav" in content_type:
        audio_format = "wav"

    logger.info(
        "Transcribing audio: size=%d bytes, format=%s, language_hint=%s",
        len(audio_bytes),
        audio_format,
        language,
    )

    try:
        result = await provider.transcribe_audio(
            audio_bytes,
            language=language or None,
            audio_format=audio_format,
        )
    except Exception as exc:
        logger.exception("Speech provider error: %s", exc)
        raise HTTPException(
            status_code=502,
            detail=f"Speech provider error: {exc}",
        )

    return TranscribeResponse(
        transcript=result.transcript,
        language=result.language,
        duration_seconds=result.duration_seconds,
        provider=result.provider,
        is_mock=result.is_mock,
    )


def _get_supported_languages() -> list[dict]:
    """Return the list of languages supported by Faster-Whisper / Whisper."""
    return [
        {"code": "auto", "label": "Auto-detect"},
        {"code": "en", "label": "English"},
        {"code": "hi", "label": "Hindi (हिन्दी)"},
        {"code": "fr", "label": "French"},
        {"code": "de", "label": "German"},
        {"code": "es", "label": "Spanish"},
        {"code": "zh", "label": "Chinese (中文)"},
        {"code": "ar", "label": "Arabic"},
        {"code": "pt", "label": "Portuguese"},
        {"code": "ru", "label": "Russian"},
        {"code": "ja", "label": "Japanese"},
        {"code": "ko", "label": "Korean"},
        {"code": "it", "label": "Italian"},
        {"code": "nl", "label": "Dutch"},
        {"code": "pl", "label": "Polish"},
        {"code": "tr", "label": "Turkish"},
        {"code": "bn", "label": "Bengali"},
        {"code": "ur", "label": "Urdu"},
        {"code": "ta", "label": "Tamil"},
        {"code": "te", "label": "Telugu"},
        {"code": "mr", "label": "Marathi"},
        {"code": "gu", "label": "Gujarati"},
    ]
