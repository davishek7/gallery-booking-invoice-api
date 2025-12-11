import re
from fastapi import status
from ..utils.responses import success_response
from ..utils.serializers import serialize_search_results


class SearchService:
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

    async def search(self, search_param):
        safe_search_term = re.escape(search_param)

        gallery_fields = ["category", "public_id", "folder"]
        booking_fields = [
            "customer.name",
            "customer.address",
            "customer.phone_number",
            "booking_id",
            "invoice_file",
        ]
        contact_fields = ["name", "phone_number", "message"]
        expense_fields = ["booking_id", "expense_type", "remarks", "amount"]

        gallery_query = {
            "$or": [
                {gallery_field: {"$regex": safe_search_term, "$options": "i"}}
                for gallery_field in gallery_fields
            ]
        }

        booking_query = {
            "$or": [
                {booking_field: {"$regex": safe_search_term, "$options": "i"}}
                for booking_field in booking_fields
            ]
        }

        contact_query = {
            "$or": [
                *[
                    {contact_field: {"$regex": safe_search_term, "$options": "i"}}
                    for contact_field in contact_fields
                ],
                {
                    "$expr": {
                        "$regexMatch": {
                            "input": {"$toString": "$phone_number"},
                            "regex": safe_search_term,
                            "options": "i",
                        }
                    }
                },
            ]
        }

        expense_query = {
            "$or": [
                {expense_field: {"$regex": safe_search_term, "$options": "i"}}
                for expense_field in expense_fields
            ]
        }

        images_cursor = self.gallery_collection.find(gallery_query, {"_id": 1})
        images = [
            serialize_search_results(doc, "gallery") async for doc in images_cursor
        ]

        bookings_cursor = self.booking_collection.find(booking_query, {"booking_id": 1})
        bookings = [
            serialize_search_results(doc, "booking") async for doc in bookings_cursor
        ]

        contacts_cursor = self.contact_collection.find(
            contact_query, {"name": 1, "_id": 1}
        )
        contacts = [
            serialize_search_results(doc, "contact") async for doc in contacts_cursor
        ]

        expenses_cursor = self.expense_collection.find(
            expense_query, {"booking_id": 1, "_id": 1}
        )
        expenses = [
            serialize_search_results(doc, "expense") async for doc in expenses_cursor
        ]

        data = {
            "images": images,
            "bookings": bookings,
            "contacts": contacts,
            "expenses": expenses,
        }

        return success_response(
            f"Search results for: {search_param}", status.HTTP_200_OK, data=data
        )
