from motor.motor_asyncio import AsyncIOMotorDatabase

from schemas.user_schema import UserCreate
from services.auth_service import hash_password


class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection("users")

    async def get_by_username(self, username: str):
        return await self.collection.find_one({"username": username})

    async def create(self, user_data: UserCreate):
        doc = {
            "username": user_data.username,
            "hashed_password": hash_password(user_data.password),
        }
        result = await self.collection.insert_one(doc)
        return await self.collection.find_one({"_id": result.inserted_id})