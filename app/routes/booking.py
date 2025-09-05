from fastapi import APIRouter, status, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials  # type: ignore
from ..configs.dependency import get_booking_service
from ..schemas.booking_schema import BookingIn, Payment, BookingItem
from ..utils.auth import access_security, refresh_security


router = APIRouter()


@router.post("/")
async def create_booking(
    booking_schema: BookingIn,
    booking_service=Depends(get_booking_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await booking_service.create(booking_schema)


@router.get("/")
async def get_bookings(
    booking_service=Depends(get_booking_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await booking_service.get_list()


@router.get("/{booking_id}")
async def get_booking(
    booking_id: str,
    booking_service=Depends(get_booking_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await booking_service.get(booking_id)


@router.patch("/{booking_id}/payment")
async def add_payment(
    booking_id: str,
    payment_schema: Payment,
    booking_service=Depends(get_booking_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await booking_service.add_payment(booking_id, payment_schema)


@router.patch("/{booking_id}/item")
async def add_item(
    booking_id: str,
    item_schema: BookingItem,
    booking_service=Depends(get_booking_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await booking_service.add_item(booking_id, item_schema)


@router.delete("/{booking_id}")
async def delete(
    booking_id: str,
    booking_service=Depends(get_booking_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await booking_service.delete(booking_id)
