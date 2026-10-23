# 🎙 VoiceLens — Multilingual Speech Transcription

> **Real-time AI-powered speech-to-text for 22+ languages, built with React + FastAPI + PostgreSQL + Faster-Whisper.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://docker.com)

---

## 📌 What Is This?

VoiceLens is a full-stack web application that lets you:

1. **Record audio** directly in your browser via the microphone.
2. **Transcribe** the recording using [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) — a local, free, offline-capable AI model supporting **99+ languages** including Hindi, English, and **code-switched speech** (e.g. Hinglish).
3. **Save, search, edit, and delete** transcription records from a polished dashboard.

The entire stack runs locally with one `docker compose up` command, or can be deployed to the cloud.

---

## 📸 Preview

### 🏠 Application Dashboard
![VoiceLens Dashboard](./Preview.png)

### 📜 Application History
![VoiceLens History](./History_Page.png)

## 🏗️ Architecture

```
Browser (React + Vite)
    │
    │  HTTP / REST API
    ▼
FastAPI Backend (Python)
    ├── POST /api/speech/transcribe   → Faster-Whisper model (local)
    └── /api/transcriptions/*        → CRUD → PostgreSQL
```

| Layer     | Technology                         | Purpose                        |
|-----------|------------------------------------|--------------------------------|
| Frontend  | React 19 · Vite · Plain CSS        | Recording UI, history dashboard |
| Backend   | Python 3.11 · FastAPI · Uvicorn    | REST API, speech processing     |
| Speech    | Faster-Whisper (CTranslate2)       | Local multilingual ASR          |
| Database  | PostgreSQL 16 · SQLAlchemy · Alembic | Persistent transcription store |
| Container | Docker · Docker Compose            | Local & cloud deployment        |

---

## ✨ Features

- 🎙 **One-click recording** — microphone permission requested only on user action
- 🌐 **22+ language support** — auto-detect or manual language selection (Hindi, English, French, Chinese, Arabic, and more)
- 🔀 **Code-switching support** — accurately handles mixed languages like Hindi+English (Hinglish) with the `small` or larger Whisper model
- ⚡ **Audio level visualizer** — live waveform bars while recording
- 💾 **PostgreSQL persistence** — each transcription saved with title, language, duration
- 🔍 **Full-text search** — search across title and transcript content
- ✏️ **Inline editing** — edit title and transcript from the dashboard
- 🗑️ **Delete with confirmation** — no accidental deletions
- 📋 **Copy to clipboard** — one click to copy any transcript
- ⚠️ **Mock/demo fallback** — clearly labelled demo mode when Whisper isn't installed
- 🐳 **Docker Compose** — one command to run everything
- 🧪 **12 backend tests** — covering all CRUD routes, validation, and pagination

---

## 📋 Prerequisites

### Local Development (without Docker)

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.11+ | [python.org](https://python.org) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) |
| PostgreSQL | 14+ | [postgresql.org](https://postgresql.org) |
| ffmpeg | any | Required by Faster-Whisper for audio decoding |

**Install ffmpeg:**
- **Windows:** `choco install ffmpeg` or download from [ffmpeg.org](https://ffmpeg.org/download.html)
- **macOS:** `brew install ffmpeg`
- **Linux:** `apt install ffmpeg`

### Docker (all-in-one)

- [Docker Desktop](https://docker.com/products/docker-desktop) (includes Docker Compose)

---

## 🚀 Quick Start — Local Development

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Multilingual-Speech-Transcription.git
cd Multilingual-Speech-Transcription
```

### 2. Set up the backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Faster-Whisper (real speech recognition)
pip install faster-whisper

# Copy example environment file
copy .env.example .env    # Windows
cp .env.example .env      # macOS/Linux
```

### 3. Configure environment variables

Edit `backend/.env`:

```ini
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/speech_transcription
SPEECH_PROVIDER=faster_whisper
WHISPER_MODEL_SIZE=base
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=int8
CORS_ORIGINS=http://localhost:5173
```

### 4. Set up PostgreSQL

```sql
-- Run in psql or pgAdmin:
CREATE DATABASE speech_transcription;
```

### 5. Run database migrations

```bash
# From the backend/ directory:
alembic upgrade head
```

> **Note:** The app also auto-creates tables on startup via SQLAlchemy if migrations are skipped. Migrations are preferred for production.

### 5b. (Optional) Seed demo data

Populate the database with 14 multilingual demo transcription records (English, Hindi, Hinglish, Spanish, French, German, Japanese, Tamil, Arabic, Chinese, Portuguese):

```bash
# On the host (uses REST API fallback if SQLAlchemy isn't in local environment):
python backend/seed.py

# Or directly inside the running Docker backend container:
docker exec voicelens_backend python seed.py

# Or import directly into PostgreSQL via SQL script:
docker exec -i voicelens_postgres psql -U postgres -d speech_transcription < backend/seed.sql

# Optional flags:
python backend/seed.py --clear    # Clear and re-seed
python backend/seed.py --api      # Force REST API seeding
```

### 6. Start the backend

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at: [http://localhost:8000](http://localhost:8000)  
Interactive API docs: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

### 7. Set up and start the frontend

```bash
cd ../frontend
npm install
npm run dev
```

The app will be available at: [http://localhost:5173](http://localhost:5173)

---

## 🐳 Quick Start — Docker Compose

```bash
# From the project root:
cp backend/.env.example backend/.env

docker compose up --build
```

| Service   | URL                         |
|-----------|-----------------------------|
| Frontend  | http://localhost            |
| Backend   | http://localhost:8000       |
| API Docs  | http://localhost:8000/api/docs |
| PostgreSQL | localhost:5432             |

> **Note:** The first run downloads the Whisper model (~150 MB for `base`). Subsequent runs use the cached model.

---

## 🔑 Environment Variables

All backend configuration lives in `backend/.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+psycopg2://postgres:postgres@localhost:5432/speech_transcription` | PostgreSQL connection string |
| `CORS_ORIGINS` | `http://localhost:5173,http://localhost:3000` | Comma-separated allowed frontend origins |
| `SPEECH_PROVIDER` | `faster_whisper` | Speech engine: `faster_whisper` or `mock` |
| `WHISPER_MODEL_SIZE` | `base` | Model: `tiny` / `base` / `small` / `medium` / `large-v3` |
| `WHISPER_DEVICE` | `cpu` | Inference device: `cpu` / `cuda` / `auto` |
| `WHISPER_COMPUTE_TYPE` | `int8` | Precision: `int8` (CPU) / `float16` (GPU) |
| `APP_ENV` | `development` | Environment name |
| `LOG_LEVEL` | `info` | Logging level |

---

## 🎯 Speech Provider Configuration

### Faster-Whisper (Recommended — Free, Local, No API Key)

Faster-Whisper runs **entirely on your machine**. No API keys, no usage limits, no internet connection required after first model download.

```ini
SPEECH_PROVIDER=faster_whisper
WHISPER_MODEL_SIZE=base      # Change to 'small' for better Hindi/Hinglish accuracy
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=int8
```

**Model sizes and trade-offs:**

| Model | Size | Speed (CPU) | Accuracy | Hindi/Hinglish |
|-------|------|-------------|----------|----------------|
| `tiny` | 75 MB | Very fast | Low | Poor |
| `base` | 145 MB | Fast | Good | Fair |
| `small` | 466 MB | Moderate | Better | Good ✓ |
| `medium` | 1.5 GB | Slow | Very good | Very good ✓✓ |
| `large-v3` | 3 GB | Slow | Best | Excellent ✓✓✓ |

> For code-switched speech (Hindi+English), use `small` or larger.

### Mock / Demo Mode

When `faster-whisper` is not installed, the app automatically falls back to **clearly-labelled demo mode** that returns placeholder text:

```ini
SPEECH_PROVIDER=mock
```

⚠️ Mock responses are always marked as demo text and never presented as real transcriptions.

---

## 📡 API Endpoints

Base URL: `http://localhost:8000`

### Health

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Returns `{"status": "ok"}` |

### Speech

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/speech/provider-info` | Active provider info and supported languages |
| POST | `/api/speech/transcribe` | Upload audio blob → get transcript |

**POST `/api/speech/transcribe`**
- Content-Type: `multipart/form-data`
- Fields: `audio` (file), `language` (optional string, e.g. `"hi"`)
- Returns: `{ transcript, language, duration_seconds, provider, is_mock }`

### Transcriptions

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/transcriptions` | Paginated list with optional search |
| POST | `/api/transcriptions` | Create new record |
| GET | `/api/transcriptions/{id}` | Get single record |
| PATCH | `/api/transcriptions/{id}` | Update title/transcript |
| DELETE | `/api/transcriptions/{id}` | Delete record |

**Query parameters for GET `/api/transcriptions`:**
- `search` — full-text search in title and transcript
- `page` — page number (default 1)
- `page_size` — items per page (default 10, max 100)

Full interactive docs: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

---

## 🗄️ Database Migrations

This project uses **Alembic** for schema migrations.

```bash
cd backend

# Apply all pending migrations
alembic upgrade head

# Downgrade one step
alembic downgrade -1

# Create a new migration (after changing models.py)
alembic revision --autogenerate -m "describe_your_change"

# View migration history
alembic history
```

---

## 🧪 Running Tests

```bash
cd backend

# Activate your virtual environment first
pip install pytest httpx

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --tb=short
```

The test suite uses an **in-memory SQLite database** — no PostgreSQL required for testing.

**Tests cover:**
- Health endpoint
- Create transcription (201 response, field validation)
- List with pagination
- Full-text search filtering
- Get single record
- Get nonexistent record (404)
- Update title and transcript
- Partial update (only title)
- Delete record
- Delete nonexistent (404)
- Pagination `has_next` / `has_prev` logic
- Title max-length validation (422)
- Empty list state

---

## 📁 Project Structure

```
Multilingual-Speech-Transcription/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── config.py                  # Settings from env vars
│   │   ├── database.py                # SQLAlchemy engine + session
│   │   ├── models.py                  # Transcription ORM model
│   │   ├── schemas.py                 # Pydantic request/response schemas
│   │   ├── routers/
│   │   │   ├── transcriptions.py      # CRUD REST routes
│   │   │   └── speech.py              # Transcription upload endpoint
│   │   └── speech/
│   │       ├── base.py                # Abstract provider interface
│   │       ├── faster_whisper_provider.py  # Faster-Whisper integration
│   │       ├── mock_provider.py        # Demo mode provider
│   │       └── provider_factory.py    # Provider selection logic
│   ├── alembic/
│   │   ├── env.py                     # Alembic config (reads DATABASE_URL)
│   │   └── versions/
│   │       └── 0001_initial.py        # Initial migration
│   ├── tests/
│   │   └── test_transcriptions.py     # 12 pytest tests
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── index.css                  # Complete design system (CSS variables, components)
│   │   ├── main.jsx                   # React entry point
│   │   ├── App.jsx                    # Root component (tabs, nav, toasts)
│   │   ├── api.js                     # Centralized API client
│   │   ├── hooks/
│   │   │   ├── useRecorder.js         # MediaRecorder hook with state machine
│   │   │   └── useToast.js            # Toast notification hook
│   │   ├── components/
│   │   │   ├── WaveformVisualizer.jsx # Animated audio level bars
│   │   │   ├── Toast.jsx              # Toast notification display
│   │   │   └── ConfirmDialog.jsx      # Modal confirmation dialog
│   │   └── pages/
│   │       ├── RecorderPage.jsx       # Main recording + transcription UI
│   │       └── HistoryPage.jsx        # Dashboard: search, list, edit, delete
│   ├── index.html
│   ├── vite.config.js                 # Vite + dev proxy config
│   ├── package.json
│   ├── nginx.conf                     # Nginx config for production
│   └── Dockerfile
│
├── docker-compose.yml                 # Orchestrates all 3 services
├── .gitignore
└── README.md
```

---

## ⚠️ Known Limitations

| Limitation | Details |
|------------|---------|
| **No live streaming transcription** | Audio is captured as a complete blob and sent after recording stops. True word-by-word streaming would require WebSockets + a streaming-capable provider. |
| **CPU speed on large models** | `large-v3` can take 30–60s for a 1-minute clip on CPU. Use `base` or `small` for demo, GPU for production. |
| **Browser compatibility** | The MediaRecorder API is not supported in Safari < 14.1. The app shows a clear warning in unsupported browsers. |
| **File size limit** | Maximum audio upload is 50 MB (configurable in `routers/speech.py`). |
| **ffmpeg required** | Faster-Whisper uses ffmpeg internally. If ffmpeg is missing, it falls back to mock mode with a warning. |
| **Single user** | No authentication is implemented. All transcriptions are visible to all users. |

---

## ☁️ Deployment Guide

### Option A — Render.com (Recommended)

**Backend (FastAPI):**
1. Create a new **Web Service** on Render.
2. Set **Root Directory** to `backend`.
3. Set **Build Command**: `pip install -r requirements.txt && pip install faster-whisper`
4. Set **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables from your `.env` file.
6. Add a **PostgreSQL** database (free tier available).
7. Set `DATABASE_URL` to the Render-provided connection string.

**Frontend (React):**
1. Create a new **Static Site** on Render.
2. Set **Root Directory** to `frontend`.
3. Set **Build Command**: `npm install && npm run build`
4. Set **Publish Directory**: `dist`
5. Set environment variable `VITE_API_BASE_URL` if using a separate domain.

> **Note:** Free Render instances sleep after 15 minutes of inactivity. The first request after sleep may be slow.

### Option B — Railway.app

1. Connect your GitHub repository.
2. Railway auto-detects the `docker-compose.yml`.
3. Add environment variables via the Railway dashboard.
4. Railway provisions managed PostgreSQL automatically.

### Option C — Docker VPS Deployment

```bash
# On your server:
git clone https://github.com/YOUR_USERNAME/Multilingual-Speech-Transcription.git
cd Multilingual-Speech-Transcription
cp backend/.env.example backend/.env
# Edit .env with your production values

docker compose up -d --build

# Run migrations
docker compose exec backend alembic upgrade head
```

---

## 📤 Publishing to GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: VoiceLens — Multilingual Speech Transcription"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/Multilingual-Speech-Transcription.git
git branch -M main
git push -u origin main
```

---

## 🤝 Development Notes

- The speech provider is **isolated behind an interface** (`BaseSpeechProvider`) — adding a new provider (e.g. OpenAI Whisper API, Google Cloud Speech) requires only creating a new class in `backend/app/speech/` and registering it in `provider_factory.py`.
- The frontend proxy in `vite.config.js` forwards `/api` requests to `http://localhost:8000` during development, so no CORS configuration is needed locally.
- CORS is restricted via the `CORS_ORIGINS` environment variable — set this to your production domain before deploying.

---

## 📄 License

MIT
