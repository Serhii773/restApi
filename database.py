import os
import motor.motor_asyncio

MONGO_URL = os.getenv(
    "DATABASE_URL",
    "mongodb://mongo_admin:password@localhost:27017"
)

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.library

def get_db():
    return db