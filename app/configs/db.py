from pymongo import AsyncMongoClient  # type: ignore
from .settings import settings

client: AsyncMongoClient | None = None


async def connect_to_mongo():
    global client
    client = AsyncMongoClient(settings.MONGODB_URI)


async def close_mongo_connection():
    global client
    if client:
        await client.close()


def get_db():
    if client is None:
        raise RuntimeError("MongoDB client is not initialized.")
    return client[settings.DB_NAME]
