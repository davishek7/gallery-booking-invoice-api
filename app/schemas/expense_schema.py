from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class ExpenseType(str, Enum):
    helper_expense = "Helper Expense"
    others = "Others"


class ExpenseIn(BaseModel):
    booking_id: str
    expense_type: ExpenseType
    amount: int
    remarks: str
    date: datetime
    created_at: datetime = Field(default_factory=datetime.now)


class ExpenseResponse(BaseModel):
    id: str
    booking_id: str
    expense_type: str
    remarks: str = None
    amount: int
    display_date: str
    date: str
    created_at: str


class ExpenseUpdate(BaseModel):
    id: str
    booking_id: str
    expense_type: str
    remarks: str
    amount: int
    date: datetime


class ExpenseSearchResult(BaseModel):
    id: str
    booking_id: str
