"""Unit tests for the 8 Specialized Organic Farming Knowledge APIs and Calculators."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_organic_remedies_endpoint():
    """Test remedies library retrieval and search filtering."""
    # Full list
    res = client.get("/api/organic/remedies")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 5
    assert any("Neem" in r["name"] for r in data["remedies"])

    # Search filter
    search_res = client.get("/api/organic/remedies?search=mildew")
    assert search_res.status_code == 200
    search_data = search_res.json()
    assert search_data["total"] >= 1
    assert any("Powdery Mildew" in p for r in search_data["remedies"] for p in r["target_pests"])


def test_organic_fertilizers_endpoint():
    """Test bio-fertilizer recipes and NPK formulations."""
    res = client.get("/api/organic/fertilizers")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 4
    assert any("Jeevamrut" in f["name"] for f in data["fertilizers"])

    # Search filter
    search_res = client.get("/api/organic/fertilizers?search=potassium")
    assert search_res.status_code == 200
    search_data = search_res.json()
    assert search_data["total"] >= 1


def test_companion_guide_endpoint():
    """Test companion planting matrix lookup."""
    res = client.get("/api/organic/companion-guide?crop=tomato")
    assert res.status_code == 200
    data = res.json()
    assert data["crop"] == "tomato"
    assert "best_companions" in data["data"]
    assert any("Basil" in c["name"] for c in data["data"]["best_companions"])
    assert any("Potato" in a["name"] for a in data["data"]["antagonists"])


def test_seed_treatment_endpoint():
    """Test thermal hot water seed treatment chart."""
    res = client.get("/api/organic/seed-treatment")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 4
    assert any(t["temp_celsius"] == 50 for t in data["seed_treatments"])


def test_roof_calculator_endpoint():
    """Test rooftop structural load and potting mix volume calculation."""
    payload = {
        "container_count": 10,
        "container_size_liters": 20.0,
        "terrace_area_sqm": 10.0,
        "soil_type": "3:1:1_cocopeat_mix",
    }
    res = client.post("/api/organic/roof-calculator", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "SAFE"
    assert data["is_safe"] is True
    assert data["load_kg_per_sqm"] < 150.0
    assert data["total_mix_volume_liters"] == 200.0
    assert data["potting_mix_breakdown_liters"]["cocopeat"] == 120.0
    assert data["potting_mix_breakdown_liters"]["vermicompost"] == 40.0
    assert data["potting_mix_breakdown_liters"]["perlite_or_pumice"] == 40.0


def test_government_schemes_endpoint():
    """Test government organic schemes & subsidies endpoint."""
    res = client.get("/api/organic/schemes")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 3
    assert any("PKVY" in s["id"].upper() for s in data["schemes"])


def test_crops_catalog_endpoint():
    """Test rooftop crop catalog & calendar."""
    res = client.get("/api/organic/crops")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 6
    assert any(c["id"] == "tomato" for c in data["crops"])


def test_weather_advisor_endpoint():
    """Test dynamic microclimate and heatwave advisor."""
    # Test heatwave conditions
    payload = {
        "temp_celsius": 38.0,
        "humidity_pct": 50.0,
        "wind_kmh": 28.0,
        "uv_index": 9.0,
    }
    res = client.post("/api/organic/weather-advisor", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["alerts"]) >= 2
    assert any("Heatwave" in a for a in data["alerts"])
    assert any("Wind" in a for a in data["alerts"])
    assert any("Shade Net" in s for s in data["actionable_care_steps"])
