from fastapi.encoders import jsonable_encoder
from ..schemas.booking_schema import BookingIn, Booking, Payment
from ..utils.random_id import generate_booking_id


class BookingService:
    def __init__(self, collection):
        self.collection = collection

    async def create(self, booking_schema: BookingIn):
        booking = booking_schema.model_dump()
        booking["booking_id"] = generate_booking_id()
        # if booking["advance"] > 0:

        result = await self.collection.insert_one(booking)
        return str(result.inserted_id)
    

    async def get_list(self):
        cursor = self.collection.find()
        bookings = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            bookings.append(Booking(**doc))
        return bookings
    

    async def get(self, booking_id: str):
        doc = await self.collection.find_one({"booking_id": booking_id})
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        booking = Booking(**doc)

        response = {
            **booking.model_dump(),
            "total": booking.total_rate,
            "final": booking.final_amount,
            "paid": booking.paid_amount,
            "due_amount": booking.due_amount,
            "payment_status": booking.payment_status
        }
        return response
    

    async def add_payment(self, booking_id: str, payment_schema: Payment):
        payment_data = payment_schema.model_dump()
        booking = await self.collection.find_one({"booking_id": booking_id})
        if booking:
            await self.collection.update_one({"booking_id": booking_id}, {"$push": {"payments": payment_data}})
        return {"message": "New payment added successfully."}