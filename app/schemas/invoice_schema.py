from pydantic import BaseModel


class InvoiceListSchema(BaseModel):
    booking_id: str
    invoice_file: str | None = None
    customer_name: str
