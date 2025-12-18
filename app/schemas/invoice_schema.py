from pydantic import BaseModel


class InvoiceListSchema(BaseModel):
    booking_id: str
    invoice_file: str
    customer_name: str
