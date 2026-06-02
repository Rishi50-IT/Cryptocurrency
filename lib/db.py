import os
from functools import lru_cache
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

@lru_cache(maxsize=1)
def get_client() -> MongoClient:
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    return MongoClient(uri, serverSelectionTimeoutMS=3000)

def get_db():
    name = os.getenv("MONGO_DB", "crypto_predictor")
    return get_client()[name]

def users():
    db = get_db()
    db.users.create_index("username", unique=True)
    return db.users

def watchlists():
    db = get_db()
    db.watchlists.create_index("username", unique=True)
    return db.watchlists

def portfolios():
    db = get_db()
    db.portfolios.create_index("username")
    return db.portfolios

def ping() -> tuple[bool, str]:
    try:
        get_client().admin.command("ping")
        return True, "Connected"
    except Exception as e:
        return False, str(e)
