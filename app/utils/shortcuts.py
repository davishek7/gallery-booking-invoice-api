from fastapi import status
from pymongo.collection import Collection
from ..exceptions.custom_exception import AppException


async def get_object_or_404(collection: Collection, query: dict):
    obj = await collection.find_one(query)
    if not obj:
        raise AppException("Booking not found", status.HTTP_404_NOT_FOUND)
    return obj
