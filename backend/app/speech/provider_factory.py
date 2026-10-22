"""
speech/provider_factory.py — Returns the active speech provider singleton.

Selection order:
  1. SPEECH_PROVIDER env var → "faster_whisper" | "mock"
  2. If faster_whisper is selected but the package is not installed → falls back
     to MockSpeechProvider with a warning rather than crashing at startup.
"""

import logging

from app.config import settings
from app.speech.base import BaseSpeechProvider

logger = logging.getLogger(__name__)

_provider_instance: BaseSpeechProvider | None = None


def get_speech_provider() -> BaseSpeechProvider:
    """FastAPI dependency that returns the configured speech provider."""
    global _provider_instance

    if _provider_instance is not None:
        return _provider_instance

    provider_name = settings.SPEECH_PROVIDER.lower()

    if provider_name == "faster_whisper":
        try:
            import faster_whisper  # noqa: F401 — just a presence check
            from app.speech.faster_whisper_provider import FasterWhisperProvider
            _provider_instance = FasterWhisperProvider()
            logger.info("Speech provider: Faster-Whisper ✓")
        except ImportError:
            logger.warning(
                "faster-whisper package not found → falling back to MockSpeechProvider. "
                "Install with: pip install faster-whisper"
            )
            from app.speech.mock_provider import MockSpeechProvider
            _provider_instance = MockSpeechProvider()
    elif provider_name == "mock":
        from app.speech.mock_provider import MockSpeechProvider
        _provider_instance = MockSpeechProvider()
        logger.info("Speech provider: Mock (demo mode) ✓")
    else:
        logger.error("Unknown SPEECH_PROVIDER=%r, using mock.", provider_name)
        from app.speech.mock_provider import MockSpeechProvider
        _provider_instance = MockSpeechProvider()

    return _provider_instance
