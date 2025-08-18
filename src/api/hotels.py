from fastapi import Query, APIRouter, Body

from src.database import async_session_maker
from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH
from src.repositories.hotels import HotelsRepository


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    location: str | None = Query(None),
    title: str | None = Query(None),
):
    per_page = pagination.per_page or 5

    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=(pagination.page - 1) * per_page,
        )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(
    hotel_data: Hotel = Body(
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
    )
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(
            hotel_data,
            id=hotel_id,
        )
        await session.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
async def partially_edit_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(
            hotel_data,
            partially_update=True,
            id=hotel_id,
        )
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}
