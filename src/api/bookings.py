from fastapi import APIRouter, Body

from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.api.dependencies import DBDep


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def create_booking(
    db: DBDep,
    booking_data: BookingAddRequest = Body(),
):
    room = await db.rooms.get_one_or_none(booking_data.room_id)
    if not room:
        return {"status": "OK", "data": "Room not found"}

    _booking_data = BookingAdd(price=room.price, **booking_data.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "OK", "data": booking}
