from fastapi import status
from ..utils.responses import success_response
from ..utils.serializers import serialize_booking


class AdminStatService:
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
        # total_contacts = await self.contact_collection.count_documents({})

        bookings_cursor = self.booking_collection.find()
        bookings_total_revenue = 0
        booking_total_received = 0
        bookings_total_due = 0
        booking_total_expenses = 0
        expenses_cursor = self.expense_collection.find({})
        async for _doc in expenses_cursor:
            booking_total_expenses += _doc["amount"]

        async for doc in bookings_cursor:
            booking = serialize_booking(doc)
            bookings_total_revenue += booking.total_revenue
            booking_total_received += booking.paid_amount
            bookings_total_due += booking.due_amount
            booking_total_expenses += booking.total_expense

        data = {
            "total_images": total_images,
            "total_bookings": total_bookings,
            # "total_contacts": total_contacts,
            "total_revenue": bookings_total_revenue,
            "total_received": booking_total_received - booking_total_expenses,
            "total_due": bookings_total_due,
            "total_expenses": booking_total_expenses,
        }

        return success_response(
            "Stats fetched successfully", status.HTTP_200_OK, data=data
        )
