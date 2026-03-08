from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.configs.db import connect_to_mongo, close_mongo_connection
from app.configs.cloudinary_config import init_cloudinary


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    init_cloudinary()
    yield
    await close_mongo_connection()
