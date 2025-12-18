from fastapi import APIRouter, Depends, Security, Query, UploadFile, Form, File
from ..schemas.booking_schema import BookingView
from ..configs.dependency import get_booking_service
from fastapi_jwt import JwtAuthorizationCredentials
from ..utils.auth import access_security


router = APIRouter()


@router.get("/")
async def get_invoices(
    view: BookingView = Query(BookingView.invoice),
    limit: int = Query(15, gt=0),
    offset: int = Query(0, ge=0),
    booking_service=Depends(get_booking_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await booking_service.get_list(view, limit, offset)


@router.get("/{booking_id}")
async def get_invoice(
    booking_id: str,
    booking_service=Depends(get_booking_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await booking_service.get(booking_id)


@router.post("/upload-invoice")
async def upload_invoice(
    file: UploadFile = File(...),
    booking_id: str = Form(...),
    booking_service=Depends(get_booking_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await booking_service.upload_invoice(booking_id, file)


@router.get("/download-invoice/{booking_id}")
async def download_invoice(
    booking_id: str,
    booking_service=Depends(get_booking_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await booking_service.download_invoice(booking_id)
