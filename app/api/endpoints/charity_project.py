from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectCreate, CharityProjectDB
from app.services.charity_project import (charity_project_invested,
                                          charity_project_balance)
from app.api.validators import (check_charity_project_exists,
                                check_name_duplicate,
                                check_charity_project_closed,
                                check_charity_project_invested)


router = APIRouter()


@router.post(
        '/',
        response_model=CharityProjectDB,
        response_model_exclude_none=True,)
       # dependencies=[Depends(current_superuser)],)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    invested_amount = await charity_project_balance(
        charity_project.full_amount, session)
    new_charity_project = await charity_project_crud.create(charity_project, session)
    await charity_project_invested(new_charity_project, invested_amount,
                                   session)
    return new_charity_project


@router.get('/',
            response_model=list[CharityProjectDB],
            response_model_exclude_none=True,)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.patch('/{charity_project_id}',
              response_model=CharityProjectDB,
              response_model_exclude_none=True,)
             # dependencies=[Depends(current_superuser)],)
async def partially_update_meeting_room(
        charity_project_id: int,
        obj_in: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session)

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session)
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,)
    #dependencies=[Depends(current_superuser)],)
async def remove_charity_project(
        charity_project_id: int,
       # obj_in: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session)
    # charity_project = await check_charity_project_invested(
    #     charity_project_id, session)
    # charity_project = await check_charity_project_closed(
    #     charity_project_id, session)
    charity_project = await charity_project_crud.remove(
        charity_project, session)
    return charity_project
