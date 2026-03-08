from app.schemas.expense_schema import ExpenseResponse
from app.utils.datetime_formatter import format_display_datetime, format_datetime
from app.utils.mongo import mongo_to_dict


def serialize_expense(expense: dict) -> ExpenseResponse:
    expense = mongo_to_dict(expense)

    expense["display_date"] = format_display_datetime(expense["date"])
    expense["date"] = format_datetime(expense["date"])
    expense["created_at"] = format_display_datetime(expense["created_at"])

    return ExpenseResponse(**expense)
