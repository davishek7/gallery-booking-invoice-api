from pydantic import BaseModel, Field
from datetime import datetime
from app.enums.expense_enums import ExpenseType


class ExpenseIn(BaseModel):
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
    expense_type: str | None = None
    remarks: str | None = None
    amount: int | None = None
    date: datetime | None = None


class ExpenseSearchResult(BaseModel):
    id: str
    booking_id: str
