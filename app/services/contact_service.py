from fastapi import status
from bson import ObjectId  # type: ignore
from ..schemas.contact_schema import ContactIn
from ..utils.responses import success_response
from ..utils.serializers import serialize_contact
from ..signals.send_email_signal import send_email_signal
from ..configs.settings import settings
from ..exceptions.custom_exception import AppException


class ContactService:
    def __init__(self, collection):
        self.collection = collection

    async def create(self, contact_schema: ContactIn):
        contact_data = contact_schema.model_dump()
        result = await self.collection.insert_one(contact_data)
        send_email_signal.send(
            "services.contact_service",
            subject="New Contact Message Received",
            recipients=[settings.MAIL_RECEIVER],
            template_name="email/contact_created.html",
            context={
                "subject": "New Contact Message Received",
                "title": "New Contact Message Received",
                "full_name": contact_data["name"],
                "message_text": contact_data["message"],
            },
        )
        return success_response(
            "Message sent successfully",
            status.HTTP_201_CREATED,
            data={"contact_id": str(result.inserted_id)},
        )

    async def get_list(self):
        cursor = self.collection.find().sort({"created_at": -1})
        contacts = [serialize_contact(doc) async for doc in cursor]
        if not contacts:
            return success_response("No contacts found", status.HTTP_200_OK, data=[])
        return success_response(
            "Contacts fetched successfully", status.HTTP_200_OK, data=contacts
        )

    async def get(self, contact_id: str):
        contact = await self.collection.find_one({"_id": ObjectId(contact_id)})
        if not contact:
            raise AppException("Contact not found", status.HTTP_404_NOT_FOUND)
        return success_response(
            "Contact fetched successfully",
            status.HTTP_200_OK,
            data=serialize_contact(contact),
        )

    async def update(self, contact_id: str):
        contact = await self.collection.find_one({"_id": ObjectId(contact_id)})
        if not contact:
            raise AppException("Contact not found", status.HTTP_404_NOT_FOUND)
        await self.collection.update_one(
            {"_id": ObjectId(contact_id)}, {"$set": {"read_status": True}}
        )
        return success_response("Contact updated successfully", status.HTTP_200_OK)

    async def delete(self, contact_id: str):
        contact = await self.collection.find_one({"_id": ObjectId(contact_id)})
        if not contact:
            raise AppException("Contact not found", status.HTTP_404_NOT_FOUND)
        await self.collection.delete_one({"_id": ObjectId(contact_id)})
        return success_response("Contact deleted successfully", status.HTTP_200_OK)
