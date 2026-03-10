from pydantic import BaseModel, Field, computed_field, constr
from datetime import datetime
from typing import List, Optional

from app.schemas.expense_schema import ExpenseResponse
from app.enums.booking_enums import (
    BookingItemCategory,
    BookingItemType,
    PaymentMethod,
    PaymentType,
)


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
    phone_number: constr(min_length=10, max_length=15)


class BookingIn(BaseModel):
    items: List[BookingItem]
    customer: CustomerDetails

    advance: int = 0
    advance_date: Optional[datetime] = None

    discount: int = 0
    payments: List[Payment] = Field(default_factory=list)

    invoice_file: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)


class BookingComputed(BaseModel):
    items: List[BookingItemResponse]
    payments: List[PaymentResponse] = Field(default_factory=list)
    discount: int

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

    @computed_field(return_type=str)
    @property
    def payment_status(self) -> str:
        if self.paid_amount >= self.final_amount:
            return "Fully Paid"
        elif self.paid_amount > 0:
            return "Partially Paid"
        return "Unpaid"

    @computed_field(return_type=str)
    @property
    def earliest_booking_item(self) -> str:
        return self.items[0].date


class BookingList(BookingComputed):
    id: str
    booking_id: str

    customer_name: str

    invoice_file: Optional[str] = None
    created_at: str


class BookingResponse(BookingComputed):
    id: str
    booking_id: str

    customer_name: str
    customer_address: str
    customer_phone_number: int  # kept as int (existing prod data)

    advance: int

    expenses: List[ExpenseResponse] = Field(default_factory=list)
    total_expense: int

    invoice_file: Optional[str] = None
    created_at: str

    @computed_field(return_type=int)
    @property
    def due_amount(self) -> int:
        return self.final_amount - self.paid_amount

    @computed_field(return_type=int)
    @property
    def total_revenue(self) -> int:
        return self.final_amount - self.total_expense


class BookingSearchResult(BaseModel):
    booking_id: str
    customer_name: str
