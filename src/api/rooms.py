from fastapi import Query, APIRouter, Body

from src.database import async_session_maker
from src.schemas.rooms import RoomAdd, RoomPATCH
from src.repositories.rooms import RoomsRepository


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    title: str | None = Query(None),
):
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).get_all(hotel_id=hotel_id)
        if title:
            rooms = [room for room in rooms if title.lower() in room.title.lower()]

        return rooms


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
    hotel_id: int,
    room_id: int,
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(
            hotel_id=hotel_id,
            id=room_id,
        )


@router.post("/{hotel_id}/rooms")
async def create_room(
    hotel_id: int,
    room_data: RoomAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Стандартный номер",
                "value": {
                    "title": "Стандарт двухместный",
                    "description": "Уютный номер с двумя односпальными кроватями, телевизором и кондиционером",
                    "price": 5000,
                    "quantity": 15,
                    "hotel_id": 2,
                },
            },
            "2": {
                "summary": "Люкс с видом на море",
                "value": {
                    "title": "Люкс Премиум",
                    "description": "Просторный номер с королевской кроватью, мини-баром и панорамным видом на море",
                    "price": 12000,
                    "quantity": 8,
                    "hotel_id": 3,
                },
            },
        }
    ),
):
    if room_data.hotel_id != hotel_id:
        return {"status": "ERROR", "message": "hotel_id in path and body must match"}

    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomAdd,
):
    async with async_session_maker() as session:
        existing_room = await RoomsRepository(session).get_one_or_none(
            id=room_id,
            hotel_id=hotel_id,
        )
        if not existing_room:
            return {
                "status": "ERROR",
                "message": "Room not found in this hotel",
            }

        await RoomsRepository(session).edit(
            room_data,
            id=room_id,
            hotel_id=hotel_id,
        )
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPATCH,
):
    async with async_session_maker() as session:
        existing_room = await RoomsRepository(session).get_one_or_none(
            id=room_id,
            hotel_id=hotel_id,
        )
        if not existing_room:
            return {
                "status": "ERROR",
                "message": "Room not found in this hotel",
            }

        await RoomsRepository(session).edit(
            room_data,
            partially_update=True,
            id=room_id,
            hotel_id=hotel_id,
        )
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    hotel_id: int,
    room_id: int,
):

    async with async_session_maker() as session:
        existing_room = await RoomsRepository(session).get_one_or_none(
            id=room_id,
            hotel_id=hotel_id,
        )
        if not existing_room:
            return {
                "status": "ERROR",
                "message": "Room not found in this hotel",
            }

        await RoomsRepository(session).delete(
            id=room_id,
            hotel_id=hotel_id,
        )
        await session.commit()
    return {"status": "OK"}
