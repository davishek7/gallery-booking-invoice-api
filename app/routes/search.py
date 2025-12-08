from fastapi import APIRouter, Query, Depends
from ..configs.dependency import get_search_service


router = APIRouter()


@router.get("/")
async def search(q: str, search_service=Depends(get_search_service)):
    return await search_service.search(q)
