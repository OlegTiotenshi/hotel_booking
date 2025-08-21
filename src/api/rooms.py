from fastapi import APIRouter, Body

from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.api.dependencies import DBDep


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
):
    return await db.rooms.get_all_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    return await db.rooms.get_one_or_none(
        hotel_id=hotel_id,
        id=room_id,
    )


@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep,
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
    room = await db.rooms.add(_room_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
    db: DBDep,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(
        _room_data,
        id=room_id,
        hotel_id=hotel_id,
    )
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
    db: DBDep,
):
    _room_data = RoomPatch(
        hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)
    )
    await db.rooms.edit(
        _room_data,
        partially_update=True,
        id=room_id,
        hotel_id=hotel_id,
    )
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    await db.rooms.delete(
        id=room_id,
        hotel_id=hotel_id,
    )
    await db.commit()
    return {"status": "OK"}
