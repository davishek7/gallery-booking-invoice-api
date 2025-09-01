import datetime
import random
import string

def generate_booking_id() -> str:
    # Example: BK-2025-08-29-XYZ12
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"KANKANA-{date_str}-{rand_str}"