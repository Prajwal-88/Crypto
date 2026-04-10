# tests/test_integration.py
# Integration Test
# Tests that the frontend and backend work together correctly

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from pipeline.transformer import transform_all
from pipeline.loader import save_processed_coins, get_processed_coins


# ── Sample Data ──
# We use fake coin data so we dont need to call CoinGecko API during testing
SAMPLE_COINS = [
    {
        "id": "bitcoin",
        "name": "Bitcoin",
        "symbol": "btc",
        "current_price": 65000,
        "market_cap": 1200000000000,
        "total_volume": 30000000000,
        "high_24h": 66000,
        "low_24h": 64000,
        "atl": 67.81,
        "price_change_percentage_24h": 2.5,
        "price_change_percentage_7d_in_currency": 8.0
    }
]


# ── Flask Test Client ──
# This lets us test Flask routes without running the server
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ─────────────────────────────────────────────
# Test 1: Does the homepage load?
# Frontend → Backend interaction
# ─────────────────────────────────────────────
def test_homepage_loads(client):
    """
    When user visits the website
    Flask should return the homepage successfully
    Status code 200 means OK
    """
    response = client.get("/")
    assert response.status_code == 200
    print(" Homepage loaded successfully")


# ─────────────────────────────────────────────
# Test 2: Does the full pipeline work?
# Transform → Save to MongoDB → Flask returns it
# ─────────────────────────────────────────────
def test_pipeline_saves_and_returns_data(client):
    """
    This is the main integration test:
    Step 1 — Transform sample coins
    Step 2 — Save to MongoDB
    Step 3 — Flask GET /api/coins returns them
    This proves frontend and backend interact correctly
    """
    # Step 1: Transform
    transformed = transform_all(SAMPLE_COINS)
    assert len(transformed) == 1

    # Step 2: Save to MongoDB
    save_processed_coins(transformed)

    # Step 3: Ask Flask for the coins
    response = client.get("/api/coins")

    # Check Flask returned OK
    assert response.status_code == 200

    # Check the data came back correctly
    data = response.get_json()
    assert data["status"] == "success"
    assert len(data["data"]) >= 1
    print(" Pipeline saves and Flask returns data correctly")


# ─────────────────────────────────────────────
# Test 3: Does the refresh button work?
# Frontend clicks Refresh → Backend runs pipeline
# ─────────────────────────────────────────────
def test_refresh_endpoint(client):
    """
    When user clicks Refresh button on the dashboard
    Flask should trigger the pipeline and return success
    """
    response = client.post("/api/refresh")
    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "success"
    print(" Refresh endpoint works correctly")