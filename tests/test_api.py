"""Unit and Integration tests for Urban Rooftop Organic Farming Assistant API."""

import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from pydantic import ValidationError
from app.main import app
from app.schemas import AskRequest, AskResponse, HealthResponse, IngestResponse
from app.services.rag_chain import format_docs
from langchain_core.documents import Document

client = TestClient(app)


def test_schema_ask_request_validation():
    """Test AskRequest validation rules."""
    req = AskRequest(question="What is the 3:1:1 lightweight potting mix recipe?")
    assert req.question == "What is the 3:1:1 lightweight potting mix recipe?"
    assert req.include_sources is True

    # Empty/short string should fail validation
    with pytest.raises(ValidationError):
        AskRequest(question="a")


def test_schema_health_response():
    """Test HealthResponse serialization."""
    health = HealthResponse(
        status="healthy",
        app_name="Urban Rooftop Organic Farming Assistant",
        version="1.0.0",
        environment="test",
        gemini_api_configured=True,
        pinecone_configured=True,
        vector_store_stats={"total_vectors": 100},
    )
    assert health.status == "healthy"
    assert health.gemini_api_configured is True


def test_format_docs_utility():
    """Test document context formatting helper."""
    docs = [
        Document(
            page_content="3:1:1 potting mix recipe: 3 parts cocopeat, 1 part vermicompost, 1 part perlite.",
            metadata={"title": "Potting Mix Guide", "source": "01_mix.md", "section": "Recipe"},
        )
    ]
    formatted = format_docs(docs)
    assert "Potting Mix Guide" in formatted
    assert "3:1:1 potting mix recipe" in formatted


def test_web_ui_root_endpoint():
    """Test that GET / returns the interactive Web UI HTML page."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Rooftop Organic Farm Hub" in response.text or "Urban Rooftop" in response.text


def test_health_endpoint():
    """Test the /health status endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "app_name" in data
    assert "gemini_api_configured" in data
