import os
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()

def get_database():
    mongo_url = os.getenv("MONGO_URL")

    if not mongo_url:
        raise ValueError("MONGO_URL not found in .env file")
    
    client = MongoClient(mongo_url)
    db = client["crypto_pipeline"]
    print("Connected to MongoDB successfully")
    return db