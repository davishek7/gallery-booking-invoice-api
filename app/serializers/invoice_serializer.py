from app.schemas.invoice_schema import InvoiceListSchema
from app.utils.mongo import mongo_to_dict


def serialize_invoice_list(booking: dict):
    booking = mongo_to_dict(booking)

    booking["customer_name"] = booking["customer"]["name"]

    return InvoiceListSchema(**booking)
