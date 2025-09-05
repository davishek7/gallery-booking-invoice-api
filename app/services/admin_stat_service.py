from fastapi import status
from ..utils.responses import success_response
from ..utils.serializers import serialize_booking


class AdminStatService:
    def __init__(self, gallery_collection, booking_collection, contact_collection):
        self.gallery_collection = gallery_collection
        self.booking_collection = booking_collection
        self.contact_collection = contact_collection

    async def stats(self):
        total_images = await self.gallery_collection.count_documents({})
        total_bookings = await self.booking_collection.count_documents({})
        total_contacts = await self.contact_collection.count_documents({})

        bookings_cursor = self.booking_collection.find()
        bookings_total_revenue = 0
        bookings_total_due = 0

        async for doc in bookings_cursor:
            booking = serialize_booking(doc)
            bookings_total_revenue += booking.paid_amount
            bookings_total_due += booking.due_amount

        data = {
            "total_images": total_images,
            "total_bookings": total_bookings,
            "total_contacts": total_contacts,
            "total_revenue": bookings_total_revenue,
            "total_due": bookings_total_due,
        }

        return success_response(
            "Stats fetched successfully", status.HTTP_200_OK, data=data
        )
