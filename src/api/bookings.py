from fastapi import APIRouter, Body

from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.api.dependencies import DBDep, UserIdDep


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    return await db.bookings.get_all_filtered(user_id=user_id)


@router.post("")
async def create_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest = Body(),
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if not room:
        return {"status": "OK", "data": "Room not found"}

    _booking_data = BookingAdd(
        user_id=user_id,
        price=room.price,
        **booking_data.model_dump(),
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "OK", "data": booking}
