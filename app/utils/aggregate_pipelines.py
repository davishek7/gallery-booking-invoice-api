from datetime import datetime


def sort_bookings_by_event_date(skip: int, limit: int):
    return [
        {
            "$addFields": {
                "sortDate": {"$min": "$items.date"}  # earliest event date
            }
        },
        {
            "$sort": {"sortDate": 1}  # nearest upcoming first
        },
        {"$skip": skip},
        {"$limit": limit},
    ]
