from datetime import date

from fastapi import APIRouter, Body, Query

from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.schemas.facilities import RoomFacilityAdd
from src.api.dependencies import DBDep


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2025-08-01"),
    date_to: date = Query(example="2025-08-10"),
):
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to,
    )


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
    room_data: RoomAddRequest = Body(),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)

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
    await update_room_facilities(db, room_id, room_data.facilities_ids)

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
    if room_data.facilities_ids is not None:
        await update_room_facilities(db, room_id, room_data.facilities_ids)
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


async def update_room_facilities(
    db: DBDep,
    room_id: int,
    new_facility_ids: list[int],
):
    current_facilities = await db.rooms_facilities.get_all_filtered(room_id=room_id)
    current_facility_ids = {fac.facility_id for fac in current_facilities}
    new_facility_ids_set = set(new_facility_ids)

    facilities_to_add = new_facility_ids_set - current_facility_ids
    facilities_to_remove = current_facility_ids - new_facility_ids_set

    if facilities_to_remove:
        facilities_to_remove_ids = [
            fac.id
            for fac in current_facilities
            if fac.facility_id in facilities_to_remove
        ]
        await db.rooms_facilities.delete_bulk(facilities_to_remove_ids)

    if facilities_to_add:
        rooms_facilities_data = [
            RoomFacilityAdd(room_id=room_id, facility_id=f_id)
            for f_id in facilities_to_add
        ]
        await db.rooms_facilities.add_bulk(rooms_facilities_data)
