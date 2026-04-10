# pipeline/transformer.py

import numpy as np
from datetime import datetime

def calculate_price_change(current_price, previous_price):
    """
    Feature 1: Daily Price Change %
    How much did the price change compared to yesterday?
    """
    if previous_price == 0 or previous_price is None:
        return 0.0
    return round(((current_price - previous_price) / previous_price) * 100, 2)


def calculate_moving_average(prices):
    """
    Feature 2: 7-Day Moving Average
    Average price over last 7 days to smooth out trend
    """
    if not prices or len(prices) == 0:
        return 0.0
    return round(sum(prices) / len(prices), 2)


def calculate_volatility(prices):
    """
    Feature 3: Volatility Score
    Standard deviation of prices — higher means more volatile
    """
    if not prices or len(prices) < 2:
        return 0.0
    return round(float(np.std(prices)), 2)


def calculate_volume_market_cap_ratio(volume, market_cap):
    """
    Feature 4: Volume to Market Cap Ratio
    High ratio means coin is being actively traded
    """
    if market_cap == 0 or market_cap is None:
        return 0.0
    return round(volume / market_cap, 4)


def calculate_momentum_label(price_change_7d):
    """
    Feature 5: Momentum Label
    Classify coin as Bullish, Bearish or Neutral
    based on 7 day price change
    """
    if price_change_7d is None:
        return "Neutral"
    if price_change_7d > 5:
        return "Bullish"
    elif price_change_7d < -5:
        return "Bearish"
    else:
        return "Neutral"


def calculate_fear_index(price_change, volume_change_pct):
    """
    Bonus Feature: Simple Fear Index
    If price drops and volume spikes = Fear
    """
    if price_change < 0 and volume_change_pct > 20:
        return "Fear"
    return "Calm"


def transform_coin(coin):
    """
    Master function — takes one raw coin from CoinGecko
    and returns enriched coin with all features added
    """
    current_price = coin.get("current_price", 0)
    previous_price = coin.get("atl", current_price)  # fallback
    volume = coin.get("total_volume", 0)
    market_cap = coin.get("market_cap", 0)
    price_change_7d = coin.get("price_change_percentage_7d_in_currency", 0)
    price_change_24h = coin.get("price_change_percentage_24h", 0)

    # Simulate 7 day prices using high/low range
    high = coin.get("high_24h", current_price)
    low = coin.get("low_24h", current_price)
    simulated_prices = [
        low, low * 1.01, current_price * 0.98,
        current_price, current_price * 1.01,
        high * 0.99, high
    ]

    return {
        "id": coin.get("id"),
        "name": coin.get("name"),
        "symbol": coin.get("symbol"),
        "current_price": current_price,
        "market_cap": market_cap,
        "total_volume": volume,
        "high_24h": high,
        "low_24h": low,
        "price_change_24h_pct": calculate_price_change(current_price, previous_price),
        "moving_average_7d": calculate_moving_average(simulated_prices),
        "volatility_score": calculate_volatility(simulated_prices),
        "volume_market_cap_ratio": calculate_volume_market_cap_ratio(volume, market_cap),
        "momentum_label": calculate_momentum_label(price_change_7d),
        "fear_index": calculate_fear_index(price_change_24h, volume / market_cap * 100 if market_cap else 0),
        "price_change_7d": price_change_7d,
        "last_updated": datetime.utcnow().isoformat()
    }


def transform_all(coins):
    """
    Run transform_coin on every coin in the list
    """
    transformed = []
    for coin in coins:
        transformed.append(transform_coin(coin))
    print(f" Transformed {len(transformed)} coins successfully")
    return transformed