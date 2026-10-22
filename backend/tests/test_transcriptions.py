"""
Tests for transcription CRUD routes.
Run with: pytest tests/ -v
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

# ── In-memory SQLite for tests ─────────────────────────────────────────────────
TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestHealth:
    def test_health_returns_ok(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"


class TestTranscriptionCRUD:
    def _create(self, client, **kwargs):
        payload = {
            "title": "Test Recording",
            "transcript": "Hello world",
            "language": "en",
            "provider": "mock",
            **kwargs,
        }
        return client.post("/api/transcriptions", json=payload)

    def test_create_returns_201(self, client):
        resp = self._create(client)
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "Test Recording"
        assert data["transcript"] == "Hello world"
        assert "id" in data

    def test_list_returns_paginated_results(self, client):
        self._create(client, title="First")
        self._create(client, title="Second")
        resp = client.get("/api/transcriptions?page=1&page_size=10")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2

    def test_search_filters_by_title(self, client):
        self._create(client, title="Morning Meeting")
        self._create(client, title="Evening Notes")
        resp = client.get("/api/transcriptions?search=Morning")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "Morning Meeting"

    def test_get_single_transcription(self, client):
        created = self._create(client).json()
        resp = client.get(f"/api/transcriptions/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]

    def test_get_nonexistent_returns_404(self, client):
        resp = client.get("/api/transcriptions/does-not-exist")
        assert resp.status_code == 404

    def test_update_title_and_transcript(self, client):
        created = self._create(client).json()
        resp = client.patch(
            f"/api/transcriptions/{created['id']}",
            json={"title": "Updated Title", "transcript": "Updated text"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "Updated Title"
        assert data["transcript"] == "Updated text"

    def test_partial_update_only_title(self, client):
        created = self._create(client).json()
        resp = client.patch(
            f"/api/transcriptions/{created['id']}",
            json={"title": "Only Title Changed"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "Only Title Changed"
        assert data["transcript"] == "Hello world"  # unchanged

    def test_delete_removes_record(self, client):
        created = self._create(client).json()
        del_resp = client.delete(f"/api/transcriptions/{created['id']}")
        assert del_resp.status_code == 204
        get_resp = client.get(f"/api/transcriptions/{created['id']}")
        assert get_resp.status_code == 404

    def test_delete_nonexistent_returns_404(self, client):
        resp = client.delete("/api/transcriptions/ghost-id")
        assert resp.status_code == 404

    def test_pagination_works(self, client):
        for i in range(5):
            self._create(client, title=f"Recording {i}")
        resp = client.get("/api/transcriptions?page=1&page_size=3")
        data = resp.json()
        assert len(data["items"]) == 3
        assert data["has_next"] is True
        assert data["has_prev"] is False

    def test_title_max_length_validation(self, client):
        resp = self._create(client, title="x" * 300)
        assert resp.status_code == 422

    def test_list_empty_returns_zero(self, client):
        resp = client.get("/api/transcriptions")
        data = resp.json()
        assert data["total"] == 0
        assert data["items"] == []
