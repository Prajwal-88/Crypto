import requests
from datetime import datetime

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"

def fetch_coins(vs_currency="usd", per_page=20):

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
            data = response.json()
            fetched_at = datetime.utcnow().isoformat()
            print(f"Successfully fetched {len(data)} coins at {fetched_at}")
            return data
        
        elif response.status_code == 429:
            print("Rate limited by CoinGecko try again in 60 seconds")
            return[]
        
        else:
            print(f"Error fetching data: {response.status_code}")
            return []
        
    except requests.exceptions.Timeout:
        print("Request timed out — CoinGecko took too long to respond")
        return []
    
    except requests.exceptions.ConnectionError:
        print("No internet connection — please check your network")
        return []


