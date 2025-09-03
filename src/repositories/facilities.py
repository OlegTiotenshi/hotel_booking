from sqlalchemy import select, delete, insert

from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def update_room_facilities(
        self,
        room_id: int,
        facilities_ids: list[int],
    ) -> None:
        get_current_facilities_query = select(self.model.facility_id).filter_by(
            room_id=room_id
        )
        res = await self.session.execute(get_current_facilities_query)
        current_facilities_ids: list[int] = res.scalars().all()

        current_facilities_ids_set = set(current_facilities_ids)
        new_facilities_ids_set = set(facilities_ids)

        facilities_to_add = new_facilities_ids_set - current_facilities_ids_set
        facilities_to_remove = current_facilities_ids_set - new_facilities_ids_set

        if facilities_to_remove:
            delete_m2m_facilities_stmt = delete(self.model).filter(
                self.model.room_id == room_id,
                self.model.facility_id.in_(facilities_to_remove),
            )
            await self.session.execute(delete_m2m_facilities_stmt)

        if facilities_to_add:
            insert_m2m_facilities_stmt = insert(self.model).values(
                [
                    {"room_id": room_id, "facility_id": f_id}
                    for f_id in facilities_to_add
                ],
            )
            await self.session.execute(insert_m2m_facilities_stmt)
