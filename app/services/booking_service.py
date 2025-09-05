from fastapi import status
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


class BookingService:
    def __init__(self, collection):
        self.collection = collection

    async def create(self, booking_schema: BookingIn):
        booking = booking_schema.model_dump()
        booking["booking_id"] = generate_booking_id()
        if booking["advance"] > 0:
            payment = Payment(
                amount=booking["advance"],
                method=PaymentMethod.upi,
                payment_type=PaymentType.advance,
            )
            booking["payments"].append(payment.model_dump())
        await self.collection.insert_one(booking)
        return success_response(
            "New Booking added successfully",
            status.HTTP_201_CREATED,
            data={"booking_id": booking["booking_id"]},
        )

    async def get_list(self):
        cursor = self.collection.find().sort({"created_at": -1})
        bookings = [serialize_booking(booking) async for booking in cursor]
        if not bookings:
            return success_response("No bookings found", status.HTTP_200_OK, data=[])
        return success_response(
            "Bookings fetched successfully", status.HTTP_200_OK, data=bookings
        )

    async def get(self, booking_id: str):
        booking = await self.collection.find_one({"booking_id": booking_id})
        if not booking:
            raise AppException("Booking not found", status.HTTP_404_NOT_FOUND)
        return success_response(
            "Booking fetched successfully",
            status.HTTP_200_OK,
            data=serialize_booking(booking),
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
