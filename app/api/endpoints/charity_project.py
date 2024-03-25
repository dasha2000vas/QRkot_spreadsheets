from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_fully_invested,
    check_charity_project_exists,
    check_charity_project_has_invested_amount,
    check_name_duplicate,
    check_new_full_amount_is_grater_then_invested,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.donation import add_to_project

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    return await add_to_project(new_project, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_charity_project_fully_invested(charity_project)
    await check_charity_project_has_invested_amount(charity_project)
    return await charity_project_crud.remove(charity_project, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    fields: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_charity_project_fully_invested(charity_project)
    if fields.name is not None:
        await check_name_duplicate(fields.name, session)
    if fields.full_amount is not None:
        await check_new_full_amount_is_grater_then_invested(
            fields.full_amount, charity_project.invested_amount
        )
    return await charity_project_crud.update(
        charity_project, fields, session
    )
