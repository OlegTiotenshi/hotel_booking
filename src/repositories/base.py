from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_all_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self):
        return await self.get_all_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by) -> BaseModel:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        try:
            stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError as ex:
            print(f"{type(ex.orig.__cause__)=}")
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            else:
                raise ex

    async def add_bulk(self, data: list[BaseModel]):
        stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(stmt)

    async def edit(self, data: BaseModel, partially_update: bool = False, **filter_by):
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=partially_update))
        )
        await self.session.execute(stmt)

    async def delete(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
