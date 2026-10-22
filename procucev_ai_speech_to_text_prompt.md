# AI Coding Agent Prompt --- Procucev Real-Time Multilingual Speech-to-Text Assignment

Build a complete, clean, responsive, production-minded web application
named **Speech to Text** for the Procucev AI Tech Hiring Assignment,
using **React.js with Vite and plain CSS (do not use Tailwind CSS)** for
the frontend, **Python FastAPI** for the backend, and **PostgreSQL with
SQLAlchemy and Alembic** for persistent storage; first inspect the
existing repository and preserve any working code, then implement the
application end to end rather than only generating a plan, and create a
polished dashboard where users can start and stop microphone recording,
see speech transcription appear incrementally in near real time, choose
or auto-detect supported languages where the speech engine allows it,
and handle multilingual or code-switched speech such as Hindi mixed with
English as accurately as the selected provider supports; use a practical
speech-to-text integration with a clearly isolated provider/service
layer, preferring a self-hosted open-source speech recognition option
that supports streaming where feasible, or a currently supported
real-time speech API if required, and verify the provider's actual API,
model name, language support, streaming behavior, limits, and setup
requirements before implementing it rather than assuming an API or model
exists; keep all provider credentials on the backend in environment
variables and never expose secrets in frontend code, provide a mock/demo
transcription mode only as a clearly labelled fallback when credentials
or a compatible speech service are unavailable, and do not falsely
present mock text as real recognition; persist each completed
transcription in PostgreSQL with fields such as id, title, transcript
text, detected or selected language when available, created_at,
updated_at, and optional duration, and implement validated REST
endpoints for creating, listing with pagination or search, retrieving,
editing title or transcript, and deleting records, with appropriate HTTP
status codes, error handling, request validation, database sessions,
migrations, and safe configuration; build a dashboard that displays
saved transcription history with readable timestamps, transcript
previews, search, loading and empty states, error messages, confirmation
before deletion, view/edit functionality, and clear success feedback,
while ensuring the live partial transcript is not repeatedly saved as
duplicate records and a completed recording is saved once unless the
user intentionally saves again; request microphone permission only after
the user initiates recording, show recording and connection status,
handle denied permissions, unsupported browsers, network failures, empty
audio, and stop/cleanup tracks and streaming connections correctly, and
explain any browser or provider limitations in the UI; organize the code
into maintainable components and modules, use sensible typing and
comments where helpful, add CORS configuration restricted through
environment settings, avoid hard-coded secrets, include an example
environment file containing placeholders only, and add automated tests
for the backend's CRUD routes and core validation plus basic frontend
checks where practical; provide a README with prerequisites, exact local
setup and run commands, PostgreSQL setup, migration instructions,
environment-variable descriptions, speech provider configuration, API
endpoint documentation, testing commands, known limitations, and
step-by-step deployment instructions; include a Dockerfile and Docker
Compose configuration if practical for running the frontend, backend,
and PostgreSQL locally, and make the app deployable using a suitable
cloud platform with a managed PostgreSQL database or documented
equivalent; ensure the app has a consistent visual design, responsive
layout, accessible labels, keyboard-friendly controls, and no broken
buttons or placeholder features presented as complete; run the available
tests and build commands, fix errors that can be reproduced, inspect the
final file structure, and summarize what was implemented, what remains
incomplete, the exact commands to run locally, the environment variables
that must be supplied, and the steps to publish the repository to GitHub
and deploy it; never claim that the app is deployed, tests pass, or a
speech provider works unless that has actually been verified, and
prioritize a working end-to-end core flow of microphone input → live
transcription → save to PostgreSQL → history dashboard → edit/delete
over unnecessary extra features.
