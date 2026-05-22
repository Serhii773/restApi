from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic_mongo import PydanticObjectId
from schemas.book_schema import BookCreate


class BookRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection("books")

    async def get_all(self, skip: int = 0, limit: int = 10):
        cursor = self.collection.find({}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def get_by_id(self, book_id):
        oid = book_id if isinstance(book_id, ObjectId) else PydanticObjectId(str(book_id))
        return await self.collection.find_one({"_id": oid})

    async def create(self, book_data: BookCreate):
        book_dict = book_data.model_dump()
        result = await self.collection.insert_one(book_dict)
        return await self.get_by_id(result.inserted_id)

    async def delete(self, book_id: str):
        result = await self.collection.delete_one({"_id": PydanticObjectId(book_id)})
        return result.deleted_count > 0