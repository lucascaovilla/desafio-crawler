from pymongo import MongoClient
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
DB_NAME = os.getenv("MONGO_DB", "crawler_data")

def get_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]

def store_data(site, data):
    if not data:
        return
    collection = get_db()[site]
    for item in data:
        item["_inserted_at"] = datetime.now(timezone.utc)

    collection.insert_many(data)

def fetch_all(site):
    collection = get_db()[site]
    return list(collection.find({}, {"_id": 0}))
