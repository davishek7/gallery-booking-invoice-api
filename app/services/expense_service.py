from fastapi import status
from bson import ObjectId
from datetime import datetime
from ..schemas.expense_schema import ExpenseIn, ExpenseUpdate
from ..utils.responses import success_response
from ..utils.shortcuts import get_object_or_404
from ..utils.serializers import serialize_expense
from ..exceptions.custom_exception import AppException


class ExpenseService:
    def __init__(self, collection, booking_collection):
        self.collection = collection
        self.booking_collection = booking_collection

    async def create(self, expense_schema: ExpenseIn):
        expense = expense_schema.model_dump()
        expense["created_at"] = datetime.now()
        await get_object_or_404(
            self.booking_collection, {"booking_id": expense["booking_id"]}
        )
        await self.collection.insert_one(expense)
        return success_response("Expense added successfully.", status.HTTP_201_CREATED)

    async def get_list(self):
        cursor = self.collection.find({}).sort("date", -1)
        docs = await cursor.to_list(length=None)
        expenses = [serialize_expense(doc) for doc in docs]
        if not expenses:
            return success_response(
                "No expenses found", status.HTTP_200_OK, data={"expenses": []}
            )
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

    async def update(self, expense_schema: ExpenseUpdate):
        updated_expense = expense_schema.model_dump()
        expense = await self.collection.find_one(
            {"_id": ObjectId(updated_expense["id"])}
        )

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
