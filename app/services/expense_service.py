from fastapi import status
from bson import ObjectId
from datetime import datetime
from app.schemas.expense_schema import ExpenseIn, ExpenseUpdate
from app.utils.responses import success_response
from app.utils.shortcuts import get_object_or_404
from app.serializers.expense_serializer import serialize_expense
from app.exceptions.custom_exception import AppException


class ExpenseService:
    def __init__(self, collection, booking_collection):
        self.collection = collection
        self.booking_collection = booking_collection

    async def create(self, booking_id: str, expense_schema: ExpenseIn):
        expense = expense_schema.model_dump()
        expense.update({"booking_id": booking_id})
        expense["created_at"] = datetime.now()
        await get_object_or_404(self.booking_collection, {"booking_id": booking_id})
        await self.collection.insert_one(expense)
        return success_response("Expense added successfully.", status.HTTP_201_CREATED)

    async def get_list(self):
        cursor = self.collection.find({}).sort("date", -1)
        docs = await cursor.to_list(length=None)
        expenses = [serialize_expense(doc) for doc in docs]
        return success_response(
            "Expenses fetched successfully",
            status.HTTP_200_OK,
            data={"expenses": expenses},
        )

    async def get(self, expense_id: str):
        expense = await self.collection.find_one({"_id": ObjectId(expense_id)})
        if not expense:
            raise AppException("Expense not found.", status.HTTP_404_NOT_FOUND)
        return success_response(
            "Expense fetched successfully.",
            status.HTTP_200_OK,
            data=serialize_expense(expense),
        )

    async def update(self, expense_id: str, expense_schema: ExpenseUpdate):
        updated_expense = expense_schema.model_dump()
        expense = await self.collection.find_one({"_id": ObjectId(expense_id)})

        if not expense:
            raise AppException("Expense not found.", status.HTTP_404_NOT_FOUND)

        await get_object_or_404(
            self.booking_collection, {"booking_id": expense["booking_id"]}
        )

        await self.collection.update_one(
            {"_id": expense["_id"]}, {"$set": updated_expense}
        )
        return success_response("Expense updated successfully", status.HTTP_200_OK)

    async def delete(self, expense_id: str):
        expense = await self.collection.find_one({"_id": ObjectId(expense_id)})
        if not expense:
            raise AppException("Expense not found.", status.HTTP_404_NOT_FOUND)
        return await self.collection.delete_one({"_id": ObjectId(expense_id)})
