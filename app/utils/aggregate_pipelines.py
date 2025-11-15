from datetime import datetime


def sort_bookings_by_event_date(skip: int, limit: int):
    return [
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
        {"$skip": skip},
        {"$limit": limit},
    ]
