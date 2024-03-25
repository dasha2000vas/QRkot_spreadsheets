from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud


async def close_object(
        object: Union[CharityProject, Donation],
):
    setattr(object, 'fully_invested', True)
    setattr(object, 'close_date', datetime.now())


async def calculate(
        project: CharityProject,
        donation: Donation,
        session: AsyncSession,
):
    if donation.invested_amount == 0:
        donation_amount = donation.full_amount
    else:
        donation_amount = donation.full_amount - donation.invested_amount
    current = project.invested_amount + donation_amount
    difference = current - project.full_amount
    if difference <= 0:
        setattr(donation, 'invested_amount', donation.full_amount)
        setattr(project, 'invested_amount', current)
        await close_object(donation)
    else:
        setattr(
            project, 'invested_amount', project.full_amount
        )
        await close_object(project)
        setattr(
            donation,
            'invested_amount',
            donation.full_amount - difference
        )
    if difference == 0:
        await close_object(project)
    session.add(project)
    session.add(donation)
    await session.commit()
    await session.refresh(project)
    await session.refresh(donation)


async def add_donation(
        donation: Donation,
        session: AsyncSession
):
    project = await charity_project_crud.get_first_open_object(session)
    if not project:
        return donation
    await calculate(project, donation, session)
    if donation.fully_invested:
        return donation
    return await add_donation(donation, session)


async def add_to_project(
        project: CharityProject,
        session: AsyncSession
):
    donation = await donation_crud.get_first_open_object(session)
    if not donation:
        return project
    await calculate(project, donation, session)
    if project.fully_invested:
        return project
    return await add_to_project(project, session)
