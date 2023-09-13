from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import (set_full_invested,
                                     investment)
from app.api.validators import (check_charity_project_exists,
                                check_name_duplicate,
                                check_charity_project_closed,
                                check_charity_project_invested,
                                check_full_amount_to_update)


router = APIRouter()


@router.post('/',
             response_model=CharityProjectDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)],)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Создаёт благотворительный проект."""
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(charity_project, session)
    await investment(new_charity_project, session)
    await set_full_invested(new_charity_project)
    await session.refresh(new_charity_project)
    return new_charity_project


@router.get('/',
            response_model=list[CharityProjectDB],
            response_model_exclude_none=True,)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.patch('/{charity_project_id}',
              response_model=CharityProjectDB,
              dependencies=[Depends(current_superuser)],)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Закрытый проект нельзя редактировать,
    нельзя установить требуемую сумму меньше уже вложенной."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session)
    await check_charity_project_closed(
        charity_project_id, session)
    if obj_in.full_amount is not None:
        await check_full_amount_to_update(
            charity_project_id, obj_in.full_amount, session)
    if obj_in.name is not None and obj_in.name != charity_project.name:
        await check_name_duplicate(obj_in.name, session)
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session)
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров. Удаляет проект.
    Нельзя удалить проект, в который уже были
    инвестированы средства, его можно только закрыть."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session)
    await check_charity_project_invested(
        charity_project_id, session)
    charity_project = await charity_project_crud.remove(
        charity_project, session)
    return charity_project
