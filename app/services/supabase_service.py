import os
from fastapi import UploadFile, status
from supabase import create_client, Client
from ..configs.settings import settings
from ..utils.shortcuts import get_object_or_404
from ..utils.responses import success_response
from ..utils.serializers import serialize_booking


class SupabaseService:
    def __init__(self, booking_collection):
        self.client: Client = create_client(
            settings.SUPABASE_URL, settings.SUPABASE_KEY
        )
        self.bucket: str = settings.INVOICE_FOLDER_NAME
        self.booking_collection = booking_collection

    async def upload_invoice(self, booking_id, file):
        await get_object_or_404(self.booking_collection, {"booking_id": booking_id})
        file_ext = os.path.splitext(file.filename)[1]
        filename = f"{booking_id}{file_ext}"
        file_path = filename

        content = await file.read()

        self.client.storage.from_(self.bucket).upload(
            file=content,
            path=file_path,
            file_options={"content-type": "application/pdf", "upsert": "true"},
        )

        await self.booking_collection.update_one(
            {"booking_id": booking_id}, {"$set": {"invoice_file": file_path}}
        )

        updated_booking = await self.booking_collection.find_one(
            {"booking_id": booking_id}
        )

        return success_response(
            message="Invoice uploaded successfully",
            status_code=status.HTTP_201_CREATED,
            data=serialize_booking(
                updated_booking, client=self.client, bucket=self.bucket
            ),
        )
