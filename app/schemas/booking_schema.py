from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime, timezone
from typing import List, Optional


# --- Payment Enums ---
class PaymentType(str, Enum):
    advance = "Advance"
    final = "Final"
    installment = "Installment"


class PaymentMethod(str, Enum):
    upi = "UPI"
    cash = "Cash"
    bank = "Bank"


# --- Payment Model ---
class Payment(BaseModel):
    amount: int
    method: PaymentMethod
    payment_type: PaymentType
    date: datetime = Field(default_factory=datetime.now)


# --- Booking Items ---
class BookingItemType(str, Enum):
    hd = "HD"
    non_hd = "NON-HD"


class BookingItemCategory(str, Enum):
    bridal = "Bridal"
    reception = "Reception"
    haldi = "Haldi"
    party = "Party"


class BookingItem(BaseModel):
    item_type: BookingItemType
    item_category: BookingItemCategory
    rate: int
    date: datetime


# --- Customer Details ---
class CustomerDetails(BaseModel):
    name: str
    address: str
    phone_number: str


class BookingIn(BaseModel):
    item: List[BookingItem]
    customer: CustomerDetails
    advance: int = 0
    discount: int = 0
    payments: List[Payment] = []
    created_at: datetime = Field(default_factory=datetime.now)

# --- Booking ---
class Booking(BaseModel):
    id: str
    booking_id: str
    item: List[BookingItem]
    customer: CustomerDetails
    advance: int
    discount: int
    payments: List[Payment] = []
    created_at: datetime

    # def __init__(self, **data):
    #     super().__init__(**data)

    #     # if advance > 0, auto-create an advance payment
    #     if self.advance > 0:
    #         advance_payment = Payment(
    #             amount=self.advance,
    #             method=PaymentMethod.cash,   # default, or pass separately
    #             payment_type=PaymentType.advance
    #         )
    #         self.payments.append(advance_payment)

    @property
    def total_rate(self) -> int:
        return sum(item.rate for item in self.item)

    @property
    def final_amount(self) -> int:
        return self.total_rate - self.discount

    @property
    def paid_amount(self) -> int:
        return sum(p.amount for p in self.payments)

    @property
    def due_amount(self) -> int:
        return self.final_amount - self.paid_amount
    
    @property
    def payment_status(self) -> str:
        if self.paid_amount >= self.final_amount:
            return "Fully Paid"
        elif self.paid_amount > 0:
            return "Partially Paid"
        else:
            return "Unpaid"
