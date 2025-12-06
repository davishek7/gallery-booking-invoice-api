from fastapi import APIRouter, Depends
from ..schemas.expense_schema import ExpenseIn, ExpenseUpdate
from ..configs.dependency import get_expense_service


router = APIRouter()


@router.post("/")
async def create_expenses(
    expense_schema: ExpenseIn, expense_service=Depends(get_expense_service)
):
    return await expense_service.create(expense_schema)


@router.get("/")
async def get_expenses(expense_service=Depends(get_expense_service)):
    return await expense_service.get_list()


@router.get("/{expense_id}")
async def get_expense(expense_id: str, expense_service=Depends(get_expense_service)):
    return await expense_service.get(expense_id)


@router.put("/")
async def update_expense(
    expense_schema: ExpenseUpdate, expense_service=Depends(get_expense_service)
):
    return await expense_service.update(expense_schema)


@router.delete("/{expense_id}")
async def delete_expense(expense_id: str, expense_service=Depends(get_expense_service)):
    return expense_service.delete(expense_id)
