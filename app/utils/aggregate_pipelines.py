from datetime import datetime


def sort_bookings_by_event_date(
    skip: int = None, limit: int = None, booking_id: str = None
):
    pipeline = [
        {
            "$lookup": {
                "from": "expense",
                "localField": "booking_id",
                "foreignField": "booking_id",
                "as": "expenses",
            }
        },
        {"$addFields": {"total_expense": {"$sum": "$expenses.amount"}}},
        {
            "$addFields": {
                "sortDate": {"$min": "$items.date"}  # earliest event date
            }
        },
        {
            "$addFields": {
                "isCompleted": {"$cond": [{"$lt": ["$sortDate", datetime.now()]}, 1, 0]}
            }
        },
        {"$sort": {"isCompleted": 1, "sortDate": 1}},
    ]
    if skip:
        pipeline.append({"$skip": skip})
    if limit:
        pipeline.append({"$limit": limit})
    if booking_id:
        pipeline.append({"$match": {"booking_id": booking_id}})
    return pipeline


def group_payments_by_year():
    return [
        {"$unwind": "$payments"},
        {
            "$group": {
                "_id": {"$year": "$payments.date"},
                "total_income": {"$sum": "$payments.amount"},
                "payments_count": {"$sum": 1},
            }
        },
        {"$sort": {"_id": -1}},
    ]
