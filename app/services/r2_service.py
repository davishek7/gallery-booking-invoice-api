import os
import boto3
from botocore.config import Config
from ..configs.settings import settings
from ..utils.shortcuts import get_object_or_404
from ..utils.serializers import serialize_booking


class R2Service:
    def __init__(self, booking_collection):
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.R2_ENDPOINT_URL,
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            config=Config(signature_version="s3v4"),
            region_name="auto",
        )

        self.bucket = settings.INVOICE_FOLDER_NAME
        self.booking_collection = booking_collection

    async def upload_invoice(self, booking_id, file):
        await get_object_or_404(self.booking_collection, {"booking_id": booking_id})
        file_ext = os.path.splitext(file.filename)[1]
        filename = f"{booking_id}{file_ext}"
        file_path = filename

        content = await file.read()

        result = self.client.put_object(
            Bucket=self.bucket,
            Key=filename,
            Body=content,
            ContentType=file.content_type,
        )

        print(result)

        await self.booking_collection.update_one(
            {"booking_id": booking_id}, {"$set": {"invoice_file": file_path}}
        )

        updated_booking = await self.booking_collection.find_one(
            {"booking_id": booking_id}
        )

        return serialize_booking(
            updated_booking, client=self.client, bucket=self.bucket
        )
