from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.repositories.rooms import RoomsRepository


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all_filtered(hotel_id=hotel_id)


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
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Стандартный номер",
                "value": {
                    "title": "Стандарт двухместный",
                    "description": "Уютный номер с двумя односпальными кроватями, телевизором и кондиционером",
                    "price": 5000,
                    "quantity": 15,
                },
            },
            "2": {
                "summary": "Люкс с видом на море",
                "value": {
                    "title": "Люкс Премиум",
                    "description": "Просторный номер с королевской кроватью, мини-баром и панорамным видом на море",
                    "price": 12000,
                    "quantity": 8,
                },
            },
        }
    ),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(
            _room_data,
            id=room_id,
            hotel_id=hotel_id,
        )
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    _room_data = RoomPatch(
        hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)
    )
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(
            _room_data,
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
        await RoomsRepository(session).delete(
            id=room_id,
            hotel_id=hotel_id,
        )
        await session.commit()
    return {"status": "OK"}
