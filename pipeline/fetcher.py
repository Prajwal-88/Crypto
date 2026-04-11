import requests

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"

def fetch_coins(vs_currency="usd", per_page=20):
    """
    Fetch top coins from CoinGecko API
    Returns a list of coin dictionaries
    """
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "7d"
    }
    try:
        response = requests.get(COINGECKO_URL, params=params)

        if response.status_code == 200:
            print(f" Successfully fetched {len(response.json())} coins")
            return response.json()
        
        elif response.status_code == 429:
            print("Rate limited by CoinGecko")
            return []
        else:
            print(f"Error fetching data: {response.status_code}")
            return []
        
    except requests.exceptions.Timeout:
        print("Request timed out Coingeko took long to respond")
        return []
    
    except requests.exceptions.ConnectionError:
        print("No internet connection")
        return []