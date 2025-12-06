from zoneinfo import ZoneInfo
from datetime import datetime
from ..configs.settings import settings


def format_display_datetime(created_at: datetime) -> str:
    tz_aware_datetime = created_at.astimezone(ZoneInfo(settings.TIMEZONE))
    return tz_aware_datetime.strftime("%d %B %Y")


def format_datetime(item_date: datetime):
    return item_date.strftime("%Y-%m-%d")
