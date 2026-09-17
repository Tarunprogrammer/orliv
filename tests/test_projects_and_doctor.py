"""Unit and Integration tests for Crop Project Tracking, Database Persistence, and AI Disease Doctor."""

import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import CropProject, CropTask, ProjectLog
from app.services.crop_engine import get_crop_realtime_status

client = TestClient(app)


def setup_module(module):
    """Ensure tables exist before tests."""
    Base.metadata.create_all(bind=engine)


def test_crop_engine_tomato_lifecycle():
    """Verify real-time day calculation and stage identification for Tomato."""
    planted_date = date.today() - timedelta(days=20)
    rt = get_crop_realtime_status("tomato", planted_date)

    assert rt["crop_name"] == "Tomato"
    assert rt["crop_age_days"] == 21
    assert "Hardening" in rt["current_stage"] or "Transplanting" in rt["current_stage"]
    assert rt["today_water_ml"] > 0
    assert "water_tip" in rt
    assert "feed_tip" in rt
    assert "roof_tip" in rt


def test_create_and_fetch_crop_project():
    """Test creating a new crop project and fetching its detailed care hub."""
    payload = {
        "crop_type": "tomato",
        "crop_name": "My Terrace Tomato Test",
        "variety": "Arka Rakshak",
        "planted_date": str(date.today() - timedelta(days=15)),
        "container_type": "12x12 HDPE Grow Bag",
        "container_count": 3,
        "soil_mix": "3:1:1 Cocopeat Mix",
    }
    response = client.post("/api/projects", json=payload)
    assert response.status_code == 200
    data = response.json()
    project_id = data["id"]
    assert data["crop_name"] == "My Terrace Tomato Test"
    assert data["crop_age_days"] == 16

    # Fetch detail hub
    detail_res = client.get(f"/api/projects/{project_id}")
    assert detail_res.status_code == 200
    detail_data = detail_res.json()
    assert len(detail_data["tasks"]) > 0
    assert len(detail_data["logs"]) > 0
    assert detail_data["realtime_care"]["today_water_ml"] > 0

    # Toggle first task
    first_task = detail_data["tasks"][0]
    toggle_res = client.patch(f"/api/tasks/{first_task['id']}/toggle")
    assert toggle_res.status_code == 200
    assert toggle_res.json()["is_completed"] is True

    # Add a custom log
    log_res = client.post(f"/api/projects/{project_id}/logs", json={"log_type": "watering", "note": "Watered 500ml"})
    assert log_res.status_code == 200

    # Delete project
    del_res = client.delete(f"/api/projects/{project_id}")
    assert del_res.status_code == 200
