from pydantic import BaseModel, Field, computed_field
from enum import Enum
from datetime import datetime
from typing import List


class PaymentType(str, Enum):
    advance = "Advance"
    final = "Final"
    installment = "Installment"


class PaymentMethod(str, Enum):
    upi = "UPI"
    cash = "Cash"
    bank = "Bank"


class Payment(BaseModel):
    amount: int
    method: PaymentMethod
    payment_type: PaymentType
    date: datetime


class PaymentResponse(BaseModel):
    amount: int
    method: PaymentMethod
    payment_type: PaymentType
    date: str


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


class BookingItemResponse(BaseModel):
    item_type: BookingItemType
    item_category: BookingItemCategory
    rate: int
    date: str


class CustomerDetails(BaseModel):
    name: str
    address: str
    phone_number: str


class BookingIn(BaseModel):
    items: List[BookingItem]
    customer: CustomerDetails
    advance: int = 0
    advance_date: datetime
    discount: int = 0
    payments: List[Payment] = []
    created_at: datetime = Field(default_factory=datetime.now)


class Booking(BaseModel):
    id: str
    booking_id: str
    items: List[BookingItemResponse]
    customer_name: str
    customer_address: str
    customer_phone_number: int
    advance: int
    discount: int
    payments: List[PaymentResponse] = []
    invoice_url: str | None = None
    download_url: str | None = None
    created_at: str

    @computed_field(return_type=int)
    @property
    def total_rate(self) -> int:
        return sum(item.rate for item in self.items)

    @computed_field(return_type=int)
    @property
    def final_amount(self) -> int:
        return self.total_rate - self.discount

    @computed_field(return_type=int)
    @property
    def paid_amount(self) -> int:
        return sum(p.amount for p in self.payments)

    @computed_field(return_type=int)
    @property
    def due_amount(self) -> int:
        return self.final_amount - self.paid_amount

    @computed_field(return_type=str)
    @property
    def payment_status(self) -> str:
        if self.paid_amount >= self.final_amount:
            return "Fully Paid"
        elif self.paid_amount > 0:
            return "Partially Paid"
        else:
            return "Unpaid"

    @computed_field(return_type=str)
    @property
    def earliest_booking_item(self) -> str:
        return self.items[0].date  # as the items are already sorted in the serializer
