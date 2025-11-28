from fastapi import status, Depends
from fastapi.responses import StreamingResponse
from ..schemas.booking_schema import (
    BookingIn,
    Payment,
    BookingItem,
    PaymentMethod,
    PaymentType,
)
from ..utils.random_id import generate_booking_id
from ..utils.serializers import serialize_booking
from ..utils.responses import success_response
from ..exceptions.custom_exception import AppException
from ..utils.aggregate_pipelines import sort_bookings_by_event_date


class BookingService:
    def __init__(self, collection, invoice_service):
        self.collection = collection
        self.invoice_service = invoice_service

    async def create(self, booking_schema: BookingIn):
        booking = booking_schema.model_dump()
        booking["booking_id"] = generate_booking_id()
        if booking["advance"] > 0:
            payment = Payment(
                amount=booking["advance"],
                method=PaymentMethod.upi,
                payment_type=PaymentType.advance,
                date=booking["advance_date"],
            )
            booking["payments"].append(payment.model_dump())
        await self.collection.insert_one(booking)
        return success_response(
            "New Booking added successfully",
            status.HTTP_201_CREATED,
            data={"booking_id": booking["booking_id"]},
        )

    async def get_list(self, limit: int, offset: int):
        total = await self.collection.count_documents({})
        pipeline = sort_bookings_by_event_date(skip=offset, limit=limit)
        cursor = await self.collection.aggregate(pipeline)
        bookings = [
            serialize_booking(booking, self.invoice_service.get_presigned_url)
            async for booking in cursor
        ]
        if not bookings:
            return success_response(
                "No bookings found",
                status.HTTP_200_OK,
                data={"bookings": [], "limit": limit, "total": total},
            )
        return success_response(
            "Bookings fetched successfully",
            status.HTTP_200_OK,
            data={"bookings": bookings, "limit": limit, "total": total},
        )

    async def get(self, booking_id: str):
        booking = await self.collection.find_one({"booking_id": booking_id})
        if not booking:
            raise AppException("Booking not found", status.HTTP_404_NOT_FOUND)
        return success_response(
            "Booking fetched successfully",
            status.HTTP_200_OK,
            data=serialize_booking(booking, self.invoice_service.get_presigned_url),
        )

    async def add_payment(self, booking_id: str, payment_schema: Payment):
        payment_data = payment_schema.model_dump()
        booking = await self.collection.find_one({"booking_id": booking_id})
        if not booking:
            raise AppException("Booking not found", status.HTTP_404_NOT_FOUND)
        await self.collection.update_one(
            {"booking_id": booking_id}, {"$push": {"payments": payment_data}}
        )
        return success_response("New payment added successfully", status.HTTP_200_OK)

    async def add_item(self, booking_id: str, item_schema: BookingItem):
        item_data = item_schema.model_dump()
        booking = await self.collection.find_one({"booking_id": booking_id})
        if not booking:
            raise AppException("Booking not found", status.HTTP_404_NOT_FOUND)
        await self.collection.update_one(
            {"booking_id": booking_id}, {"$push": {"items": item_data}}
        )
        return success_response("New item added successfully", status.HTTP_200_OK)

    async def delete(self, booking_id: str):
        booking = await self.collection.find_one({"booking_id": booking_id})
        if not booking:
            raise AppException("Booking not found", status.HTTP_404_NOT_FOUND)
        await self.collection.delete_one({"booking_id": booking_id})
        return success_response("Booking deleted successfully", status.HTTP_200_OK)

    async def upload_invoice(self, booking_id, file):
        data = await self.invoice_service.upload_invoice(booking_id, file)
        return success_response(
            message="Invoice uploaded successfully",
            status_code=status.HTTP_201_CREATED,
            data=data,
        )

    async def download_invoice(self, booking_id):
        result = await self.invoice_service.download_invoice(booking_id)
        return StreamingResponse(
            result["r2_file"].iter_content(chunk_size=1024),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{result["filename"]}"'
            },
        )
