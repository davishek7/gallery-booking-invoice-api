import os
import boto3
import requests
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

    def get_presigned_url(self, filename: str):
        return self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket, "Key": filename},
            ExpiresIn=43200,
        )

    async def upload_invoice(self, booking_id, file):
        await get_object_or_404(self.booking_collection, {"booking_id": booking_id})

        content = await file.read()

        self.client.put_object(
            Bucket=self.bucket,
            Key=file.filename,
            Body=content,
            ContentType=file.content_type,
            ContentDisposition=f'attachment; filename="{file.filename}"',
        )

        await self.booking_collection.update_one(
            {"booking_id": booking_id}, {"$set": {"invoice_file": file.filename}}
        )

        updated_booking = await self.booking_collection.find_one(
            {"booking_id": booking_id}
        )

        return serialize_booking(updated_booking, 0, self.get_presigned_url)

    async def download_invoice(self, booking_id):
        booking = await get_object_or_404(
            self.booking_collection, {"booking_id": booking_id}
        )
        signed_url = self.get_presigned_url(booking["invoice_file"])
        r2_file = requests.get(signed_url, stream=True)
        return {"r2_file": r2_file, "filename": booking["invoice_file"]}
