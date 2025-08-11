from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "emotion_spending_db")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_database():
    return db
