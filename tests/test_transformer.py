# tests/test_transformer.py

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipeline.transformer import (
    calculate_price_change,
    calculate_moving_average,
    calculate_volatility,
    calculate_volume_market_cap_ratio,
    calculate_momentum_label,
    calculate_fear_index,
    transform_coin
)


# ── Feature 1: Price Change % ──
def test_price_increase():
    assert calculate_price_change(110, 100) == 10.0

def test_price_decrease():
    assert calculate_price_change(90, 100) == -10.0

def test_price_change_zero_previous():
    """Should return 0.0 to avoid division by zero"""
    assert calculate_price_change(100, 0) == 0.0


# ── Feature 2: Moving Average ──
def test_moving_average_basic():
    assert calculate_moving_average([10, 20, 30]) == 20.0

def test_moving_average_empty():
    """Empty list should return 0.0 safely"""
    assert calculate_moving_average([]) == 0.0


# ── Feature 3: Volatility ──
def test_volatility_high():
    """Widely spread prices = high volatility"""
    assert calculate_volatility([10, 100, 200, 300]) > 50

def test_volatility_empty():
    assert calculate_volatility([]) == 0.0

def test_volatility_always_positive():
    assert calculate_volatility([50, 60, 40, 70, 30]) >= 0


# ── Feature 4: Volume/MarketCap Ratio ──
def test_volume_ratio_basic():
    assert calculate_volume_market_cap_ratio(1000, 10000) == 0.1

def test_volume_ratio_zero_marketcap():
    """Zero market cap should return 0.0 safely"""
    assert calculate_volume_market_cap_ratio(1000, 0) == 0.0


# ── Feature 5: Momentum Label ──
def test_momentum_bullish():
    assert calculate_momentum_label(10.0) == "Bullish"

def test_momentum_bearish():
    assert calculate_momentum_label(-10.0) == "Bearish"

def test_momentum_neutral():
    assert calculate_momentum_label(3.0) == "Neutral"

def test_momentum_none():
    """None value should return Neutral safely"""
    assert calculate_momentum_label(None) == "Neutral"


# ── Bonus: Fear Index ──
def test_fear_condition():
    """Price drop + volume spike = Fear"""
    assert calculate_fear_index(-5.0, 25.0) == "Fear"

def test_calm_condition():
    assert calculate_fear_index(5.0, 25.0) == "Calm"


# ── Master Transform Function ──
@pytest.fixture
def sample_coin():
    return {
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

def test_transform_returns_dict(sample_coin):
    assert isinstance(transform_coin(sample_coin), dict)

def test_transform_has_all_features(sample_coin):
    result = transform_coin(sample_coin)
    for feature in ["price_change_24h_pct", "moving_average_7d",
                    "volatility_score", "volume_market_cap_ratio",
                    "momentum_label", "fear_index"]:
        assert feature in result

def test_transform_momentum_bullish(sample_coin):
    assert transform_coin(sample_coin)["momentum_label"] == "Bullish"

def test_transform_preserves_id(sample_coin):
    assert transform_coin(sample_coin)["id"] == "bitcoin"