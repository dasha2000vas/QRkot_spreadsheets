from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objects = await session.execute(select(self.model))
        return db_objects.scalars().all()

    async def get_first_open_object(
            self,
            session: AsyncSession
    ):
        db_object = await session.execute(
            select(self.model).where(
                self.model.fully_invested == False # noqa
            )
        )
        return db_object.scalars().first()

    async def create(
            self,
            fields,
            session: AsyncSession,
            user: Optional[User] = None,
    ):
        fields_data = fields.dict()
        if user is not None:
            fields_data['user_id'] = user.id
        db_object = self.model(**fields_data)
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object
