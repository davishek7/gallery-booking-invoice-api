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
from ..utils.serializers import (
    serialize_booking_list,
    serialize_booking,
    serialize_expense,
)
from ..utils.responses import success_response
from ..exceptions.custom_exception import AppException
from ..utils.aggregate_pipelines import sort_bookings_by_event_date


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

    async def get_list(self, limit: int, offset: int):
        total = await self.collection.count_documents({})
        pipeline = sort_bookings_by_event_date(skip=offset, limit=limit)
        cursor = await self.collection.aggregate(pipeline)
        bookings = [
            serialize_booking_list(booking, self.invoice_service.get_presigned_url)
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

        total_expenses_count = await self.expense_collection.count_documents(
            {"booking_id": booking["booking_id"]}
        )

        expense_cursor = self.expense_collection.find(
            {"booking_id": booking["booking_id"]}
        )

        expenses = [serialize_expense(doc) async for doc in expense_cursor]

        total_expense = sum(_.amount for _ in expenses)

        return success_response(
            "Booking fetched successfully",
            status.HTTP_200_OK,
            data={
                "booking": serialize_booking(
                    booking, total_expense, self.invoice_service.get_presigned_url
                ),
                "expenses": expenses,
            },
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
