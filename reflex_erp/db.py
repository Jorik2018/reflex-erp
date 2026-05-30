from functools import lru_cache
from pymongo import MongoClient
import os

@lru_cache
def get_db():
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")

    if not uri or not db_name:
        return None

    client = MongoClient(uri)
    return client[db_name]

def get_employee_collection():
    db = get_db()
    if db is None:
        return None
    return db["employee"]