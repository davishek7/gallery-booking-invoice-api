from fastapi import status
from app.utils.responses import success_response
from app.serializers.booking_serializer import serialize_booking
from app.utils.aggregate_pipelines import sort_bookings_by_event_date, group_payments_by_year


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

        total_revenue = 0
        total_received = 0
        total_due = 0
        total_expenses = 0

        async for doc in bookings_cursor:
            booking = serialize_booking(doc)

            total_revenue += booking.total_revenue
            total_received += booking.paid_amount
            total_due += booking.due_amount
            total_expenses += booking.total_expense

        data = {
            "total_images": total_images,
            "total_bookings": total_bookings,
            "total_revenue": total_revenue,
            "total_received": total_received,
            "total_due": total_due,
            "total_expenses": total_expenses,
        }

        return success_response(
            "Stats fetched successfully",
            status.HTTP_200_OK,
            data=data,
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
