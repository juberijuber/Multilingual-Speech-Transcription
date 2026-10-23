"""
config.py — Central application configuration.
All settings are loaded from environment variables (never hard-coded).
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

_BACKEND_DIR = Path(__file__).resolve().parent.parent
_ENV_PATH = _BACKEND_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_PATH) if _ENV_PATH.exists() else ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Database ──────────────────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql+psycopg2://postgres:1234@localhost:5433/speech_transcription"

    # ── CORS ──────────────────────────────────────────────────────────────────
    # Comma-separated list of allowed origins, e.g. "http://localhost:5173,https://myapp.com"
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # ── Speech Provider ───────────────────────────────────────────────────────
    # Options: "faster_whisper" | "mock"
    SPEECH_PROVIDER: str = "faster_whisper"

    # Faster-Whisper model size: tiny | base | small | medium | large-v2 | large-v3
    WHISPER_MODEL_SIZE: str = "base"

    # Device for Faster-Whisper: "cpu" | "cuda" | "auto"
    WHISPER_DEVICE: str = "cpu"

    # Compute type for Faster-Whisper: "int8" | "float16" | "float32"
    WHISPER_COMPUTE_TYPE: str = "int8"

    # ── App ───────────────────────────────────────────────────────────────────
    APP_ENV: str = "development"
    LOG_LEVEL: str = "info"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()
