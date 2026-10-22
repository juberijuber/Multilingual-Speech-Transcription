"""
speech/faster_whisper_provider.py
—————————————————————————————————
Faster-Whisper speech provider.

Faster-Whisper is a reimplementation of OpenAI Whisper using CTranslate2,
offering 4× faster inference on CPU and GPU.

Requirements:
  pip install faster-whisper

Supported languages include English, Hindi, and 97 other languages.
For code-switched speech (e.g. Hinglish), use model size "small" or larger
and pass language=None so Whisper detects automatically per segment.

Model sizes vs accuracy/speed trade-off:
  tiny   → fastest, lowest accuracy
  base   → good balance for demos
  small  → better multilingual, ~2× slower than base
  medium → near-production quality
  large-v3 → best accuracy, requires ~10 GB RAM / VRAM
"""

import asyncio
import io
import logging
import os
import tempfile
from typing import Optional

from app.config import settings
from app.speech.base import BaseSpeechProvider, TranscriptionResult

logger = logging.getLogger(__name__)

# Lazy-loaded model — loaded once on first request, not at import time.
_model = None
_model_lock = asyncio.Lock()


async def _get_model():
    global _model
    async with _model_lock:
        if _model is None:
            try:
                from faster_whisper import WhisperModel  # type: ignore

                logger.info(
                    "Loading Faster-Whisper model '%s' on device='%s' compute_type='%s'",
                    settings.WHISPER_MODEL_SIZE,
                    settings.WHISPER_DEVICE,
                    settings.WHISPER_COMPUTE_TYPE,
                )
                _model = WhisperModel(
                    settings.WHISPER_MODEL_SIZE,
                    device=settings.WHISPER_DEVICE,
                    compute_type=settings.WHISPER_COMPUTE_TYPE,
                )
                logger.info("Faster-Whisper model loaded successfully.")
            except ImportError:
                logger.error(
                    "faster-whisper is not installed. "
                    "Run: pip install faster-whisper"
                )
                raise
    return _model


class FasterWhisperProvider(BaseSpeechProvider):
    """
    Transcribes audio using the locally-running Faster-Whisper model.

    The browser sends WebM/Opus audio; we write it to a temporary file
    because Faster-Whisper's decode() requires a file path.
    """

    async def transcribe_audio(
        self,
        audio_bytes: bytes,
        *,
        language: Optional[str] = None,
        audio_format: str = "webm",
    ) -> TranscriptionResult:
        if not audio_bytes:
            return TranscriptionResult(
                transcript="",
                language=language,
                duration_seconds=0.0,
                provider="faster_whisper",
            )

        model = await _get_model()

        # Write to a temp file — Faster-Whisper needs a path, not bytes
        suffix = f".{audio_format}"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        try:
            # Run the CPU-bound transcription in a thread pool
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                self._run_transcription,
                model,
                tmp_path,
                language,
            )
            return result
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    @staticmethod
    def _run_transcription(model, audio_path: str, language: Optional[str]) -> TranscriptionResult:
        """Blocking call to Faster-Whisper — runs in a thread executor."""
        segments, info = model.transcribe(
            audio_path,
            language=language,        # None → auto-detect
            beam_size=5,
            vad_filter=True,          # skip silence
            vad_parameters={"min_silence_duration_ms": 300},
        )

        transcript_parts: list[str] = []
        last_end = 0.0
        for segment in segments:
            transcript_parts.append(segment.text.strip())
            last_end = segment.end

        transcript = " ".join(transcript_parts).strip()
        detected_language = info.language if info.language else language

        logger.info(
            "Transcription complete: language=%s, duration=%.1fs, chars=%d",
            detected_language,
            last_end,
            len(transcript),
        )

        return TranscriptionResult(
            transcript=transcript,
            language=detected_language,
            duration_seconds=round(last_end, 2),
            provider="faster_whisper",
        )
