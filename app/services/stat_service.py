from fastapi import status
from ..utils.responses import success_response
from ..utils.serializers import serialize_booking
from ..utils.aggregate_pipelines import (
    group_payments_by_year,
    sort_bookings_by_event_date,
)


class StatService:
    def __init__(
        self,
        gallery_collection,
        booking_collection,
        contact_collection,
        expense_collection,
    ):
        self.gallery_collection = gallery_collection
        self.booking_collection = booking_collection
        self.contact_collection = contact_collection
        self.expense_collection = expense_collection

    async def stats(self):
        total_images = await self.gallery_collection.count_documents({})
        total_bookings = await self.booking_collection.count_documents({})

        bookings_cursor = await self.booking_collection.aggregate(
            sort_bookings_by_event_date()
        )
        bookings_total_revenue = 0
        booking_total_received = 0
        bookings_total_due = 0
        booking_total_expenses = 0

        async for doc in bookings_cursor:
            booking = serialize_booking(doc)
            bookings_total_revenue += booking.total_revenue - booking.total_expense
            booking_total_received += booking.paid_amount - booking.total_expense
            bookings_total_due += booking.due_amount
            booking_total_expenses += booking.total_expense

        data = {
            "total_images": total_images,
            "total_bookings": total_bookings,
            "total_revenue": bookings_total_revenue,
            "total_received": booking_total_received - booking_total_expenses,
            "total_due": bookings_total_due,
            "total_expenses": booking_total_expenses,
        }

        return success_response(
            "Stats fetched successfully", status.HTTP_200_OK, data=data
        )

    async def get_yearly_income(self):
        cursor = await self.booking_collection.aggregate(group_payments_by_year())
        data = [
            {
                "year": doc["_id"],
                "total_income": doc["total_income"],
                "payments_count": doc["payments_count"],
            }
            async for doc in cursor
        ]
        return success_response(
            "Year wise income fetched",
            status.HTTP_200_OK,
            data=data,
        )
