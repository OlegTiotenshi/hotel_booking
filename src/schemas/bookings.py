from datetime import date

from pydantic import BaseModel


class BookingAddRequest(BaseModel):
    date_from: date
    date_to: date
    quantity: int
    room_id: int


class BookingAdd(BaseModel):
    date_from: date
    date_to: date
    price: int
    quantity: int
    room_id: int
    user_id: int


class Booking(BookingAdd):
    id: int
