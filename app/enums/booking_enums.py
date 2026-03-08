from enum import Enum


class BookingView(str, Enum):
    default = "default"
    invoice = "invoice"


class PaymentType(str, Enum):
    advance = "Advance"
    final = "Final"
    installment = "Installment"


class PaymentMethod(str, Enum):
    upi = "UPI"
    cash = "Cash"
    bank = "Bank"


class BookingItemType(str, Enum):
    hd = "HD"
    non_hd = "NON-HD"


class BookingItemCategory(str, Enum):
    bridal = "Bridal"
    reception = "Reception"
    haldi = "Haldi"
    party = "Party"
