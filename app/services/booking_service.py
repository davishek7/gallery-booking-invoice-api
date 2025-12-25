from fastapi import status
from fastapi.responses import StreamingResponse
from ..schemas.booking_schema import (
    BookingIn,
    Payment,
    BookingItem,
    PaymentMethod,
    PaymentType,
    BookingView,
)
from ..utils.random_id import generate_booking_id
from ..utils.serializers import (
    serialize_booking_list,
    serialize_booking,
    serialize_invoice_list,
)
from ..utils.responses import success_response
from ..exceptions.custom_exception import AppException
from ..utils.aggregate_pipelines import sort_bookings_by_event_date
from ..utils.shortcuts import get_object_or_404


class BookingService:
    def __init__(self, collection, expense_collection, invoice_service):
        self.collection = collection
        self.expense_collection = expense_collection
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

    async def get_list(self, view: BookingView, limit: int, offset: int):
        total = await self.collection.count_documents({})
        pipeline = sort_bookings_by_event_date(skip=offset, limit=limit)
        cursor = await self.collection.aggregate(pipeline)

        if view == BookingView.invoice:
            bookings = [serialize_invoice_list(booking) async for booking in cursor]
        else:
            bookings = [serialize_booking_list(booking) async for booking in cursor]
        return success_response(
            "Bookings fetched successfully",
            status.HTTP_200_OK,
            data={"bookings": bookings, "limit": limit, "total": total},
        )

    async def get(self, booking_id: str):
        pipeline = sort_bookings_by_event_date(booking_id=booking_id)
        cursor = await self.collection.aggregate(pipeline)
        booking = await cursor.to_list(length=1)
        if not booking:
            raise AppException("Booking not found", status.HTTP_404_NOT_FOUND)

        return success_response(
            "Booking fetched successfully",
            status.HTTP_200_OK,
            data=serialize_booking(booking[0]),
        )

    async def add_payment(self, booking_id: str, payment_schema: Payment):
        await get_object_or_404(self.collection, {"booking_id": booking_id})
        payment_data = payment_schema.model_dump()
        result = await self.collection.update_one(
            {
                "booking_id": booking_id,
                "$expr": {
                    "$lte": [
                        {
                            "$add": [
                                {"$sum": "$payments.amount"},
                                payment_data["amount"],
                            ]
                        },
                        {"$subtract": [{"$sum": "$items.rate"}, "$discount"]},
                    ]
                },
            },
            {"$push": {"payments": payment_data}},
        )
        if result.modified_count == 0:
            raise AppException("Payment exceeds final booking amount", status.HTTP_400_BAD_REQUEST)
        return success_response("New payment added successfully", status.HTTP_200_OK)

    async def add_item(self, booking_id: str, item_schema: BookingItem):
        item_data = item_schema.model_dump()
        result = await self.collection.update_one(
            {"booking_id": booking_id}, {"$push": {"items": item_data}}
        )
        if result.matched_count == 0:
            raise AppException("Booking not found", status.HTTP_404_NOT_FOUND)
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

    async def booking_id_list(self):
        cursor = self.collection.find(
            {}, {"booking_id": 1, "customer.name": 1, "_id": 0}
        ).sort("created_at", -1)
        bookings = [
            {"booking_id": doc["booking_id"], "customer_name": doc["customer"]["name"]}
            async for doc in cursor
        ]
        return success_response(
            "Booking IDs fetched successfully", status.HTTP_200_OK, data=bookings
        )
