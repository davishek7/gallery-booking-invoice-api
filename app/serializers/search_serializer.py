from app.schemas.booking_schema import BookingSearchResult
from app.schemas.gallery_schema import ImageSearchResult
from app.schemas.contact_schema import ContactSearchResult
from app.schemas.expense_schema import ExpenseSearchResult
from app.utils.mongo import mongo_to_dict


def serialize_search_results(
    data: dict, search_result_type: str
) -> (
    ImageSearchResult | BookingSearchResult | ContactSearchResult | ExpenseSearchResult
):
    data = mongo_to_dict(data)

    if search_result_type == "gallery":
        return ImageSearchResult(**data)

    if search_result_type == "booking":
        data["customer_name"] = data["customer"]["name"]
        return BookingSearchResult(**data)

    if search_result_type == "contact":
        return ContactSearchResult(**data)

    if search_result_type == "expense":
        return ExpenseSearchResult(**data)
