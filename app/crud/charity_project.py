
from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get(
            self,
            project_id: int,
            session: AsyncSession,
    ):
        db_project = await session.execute(
            select(self.model).where(
                self.model.id == project_id
            )
        )
        return db_project.scalars().first()

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,

    ) -> Optional[int]:
        project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> Optional[list[dict[str, str]]]:
        projects = await session.execute(
            select(
                CharityProject
            ).where(
                CharityProject.fully_invested == True # noqa
            ).order_by(
                CharityProject.close_date - CharityProject.create_date
            )
        )
        return projects.scalars().all()

    async def update(
            self,
            project: CharityProject,
            fields,
            session: AsyncSession,
    ):
        object_data = jsonable_encoder(project)
        update_data = fields.dict(exclude_unset=True)
        for field in object_data:
            if field in update_data:
                setattr(project, field, update_data[field])
        if project.full_amount == project.invested_amount:
            setattr(project, 'fully_invested', True)
            setattr(project, 'close_date', datetime.now())
        session.add(project)
        await session.commit()
        await session.refresh(project)
        return project

    async def remove(
            self,
            project: CharityProject,
            session: AsyncSession
    ):
        await session.delete(project)
        await session.commit()
        return project


charity_project_crud = CRUDCharityProject(CharityProject)
