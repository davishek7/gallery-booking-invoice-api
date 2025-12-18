from fastapi import APIRouter, Depends, Security, Query
from fastapi_jwt import JwtAuthorizationCredentials
from ..configs.dependency import get_booking_service
from ..schemas.booking_schema import BookingIn, Payment, BookingItem, BookingView
from ..utils.auth import access_security


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
    view: BookingView = Query(BookingView.default),
    limit: int = Query(15, gt=0),
    offset: int = Query(0, ge=0),
    booking_service=Depends(get_booking_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await booking_service.get_list(view, limit, offset)


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


@router.get("/booking-id/list")
async def get_booking_id_list(
    booking_service=Depends(get_booking_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await booking_service.booking_id_list()
