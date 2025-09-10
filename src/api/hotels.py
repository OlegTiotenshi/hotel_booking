from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import HotelAdd, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
# @cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None),
        title: str | None = Query(None),
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),
):
    per_page = pagination.per_page or 5

    return await db.hotels.get_filtered_by_time(
        location=location,
        title=title,
        date_from=date_from,
        date_to=date_to,
        limit=per_page,
        offset=(pagination.page - 1) * per_page,
    )


@router.get("/{hotel_id}")
async def get_hotel(
        hotel_id: int,
        db: DBDep,
):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(
            openapi_examples={
                "1": {
                    "summary": "Сочи",
                    "value": {
                        "title": "Отель RICH 5 звезд у моря",
                        "location": "Сочи, ул. Моря, 1",
                    },
                },
                "2": {
                    "summary": "Дубай",
                    "value": {
                        "title": "Отель SHARM все включено",
                        "location": "Дубай, ул. Шейха, 2",
                    },
                },
            }
        ),
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(
        hotel_id: int,
        hotel_data: HotelAdd,
        db: DBDep,
):
    await db.hotels.edit(
        hotel_data,
        id=hotel_id,
    )
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPatch,
        db: DBDep,
):
    await db.hotels.edit(
        hotel_data,
        partially_update=True,
        id=hotel_id,
    )
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(
        hotel_id: int,
        db: DBDep,
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
