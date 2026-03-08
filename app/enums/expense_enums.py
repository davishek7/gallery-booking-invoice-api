from enum import Enum


class ExpenseType(str, Enum):
    helper_expense = "Helper Expense"
    others = "Others"
