"""
main.py — FastAPI application entry point.

Registers:
  - CORS middleware (origins from environment)
  - All API routers
  - /health endpoint
  - Startup event: create database tables if they don't exist yet
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import speech, transcriptions

logging.basicConfig(
    level=settings.LOG_LEVEL.upper(),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Multilingual Speech Transcription API",
    description=(
        "REST API for the Multilingual Speech-to-Text application. "
        "Transcribes audio using Faster-Whisper and stores results in PostgreSQL."
    ),
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(transcriptions.router)
app.include_router(speech.router)


# ── Startup ───────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def on_startup():
    logger.info("Creating database tables (if they don't already exist)...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database ready.")

    # ── Print service URLs to the terminal ────────────────────────────────────
    banner = """
╔══════════════════════════════════════════════════════════════╗
║           🎙  VoiceLens — Multilingual Speech AI  🎙         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   🌐  Frontend (App)     →   http://localhost                ║
║   ⚙️   Backend (API)      →   http://localhost:8000          ║
║   📖  API Docs           →   http://localhost:8000/api/docs  ║
║   ❤️   Health Check       →   http://localhost:8000/health   ║
║                                                              ║
║   🗄️   PostgreSQL          →   localhost:5432                 ║
║        Database: speech_transcription                        ║
║        Username: postgres                                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner, flush=True)


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health_check():
    """Returns 200 OK when the server is running."""
    return {"status": "ok", "environment": settings.APP_ENV}
