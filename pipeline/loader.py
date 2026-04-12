
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

def get_database():
    """
    Connect to MongoDB Atlas and return database
    """
    mongo_url = os.getenv("MONGO_URL")
    
    if not mongo_url:
        print("MONGO_URL not found in .env file")
        return None
    
    try:
        client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        #client = MongoClient(mongo_url)
        client.server_info()
        db = client["crypto_pipeline"]
        print("Connected to MongoDB successfully")
        return db

    except Exception as e:
        print(f"Could not connect to MongoDB: {str(e)}")
        return None


def save_raw_coins(coins):
    """
    Save raw CoinGecko data into raw_prices collection
    """
    db = get_database()
    if db is None:
        print("Skipping save no database connection")
        return
    
    try:
        collection = db["raw_prices"]

        # Add timestamp to each coin
        timestamp = datetime.utcnow().isoformat()
        for coin in coins:
            coin["fetched_at"] = timestamp

        # Clear old data and insert fresh
        
        #collection.delete_many({})
        collection.insert_many(coins)
        print(f" Saved {len(coins)} raw coins to MongoDB")

    except Exception as e:
        print(f"Error saving raw coins: {str(e)}")

def save_processed_coins(coins):
    """
    Save transformed/enriched coin data into processed_coins collection
    """
    db = get_database()
    collection = db["processed_coins"]

    timestamp = datetime.utcnow().isoformat()
    for coin in coins:
        coin["saved_at"] = timestamp
    # Clear old data and insert fresh
    #collection.delete_many({})
    collection.insert_many(coins)
    print(f"Saved {len(coins)} processed coins to MongoDB")


def get_processed_coins():
    """
    Retrieve all processed coins from MongoDB
    Returns list of coin dictionaries
    """
    db = get_database()
    collection = db["processed_coins"]

    # Get the latest timestamp
    latest = collection.find_one(
        {},
        sort=[("saved_at", -1)]
    )

    if not latest:
        return []
    
    # Get all coins from that latest timestamp
    latest_time = latest["saved_at"]
    coins = list(collection.find(
        {"saved_at": latest_time},
        {"_id": 0}
    ))

    # Exclude MongoDB _id field
    #coins = list(collection.find({}, {"_id": 0}))
    print(f"Retrieved {len(coins)} latest coins from MongoDB")
    return coins


def get_coin_by_id(coin_id):
    """
    Retrieve a single coin by its id
    """
    db = get_database()
    collection = db["processed_coins"]

    # Get most recent record for this coin
    coin = collection.find_one(
        {"id": coin_id},
        sort=[("saved_at", -1)],
        projection={"_id": 0}
    )
    return coin

