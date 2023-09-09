from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
# from app.crud.donation import donation_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectCreate, CharityProjectDB
#                                     #  MeetingRoomUpdate)
# from app.schemas.reservation import ReservationDB
# from app.api.validators import check_meeting_room_exists, check_name_duplicate

router = APIRouter()


@router.post(
        '/',
        response_model=CharityProjectDB,
        response_model_exclude_none=True,)
       # dependencies=[Depends(current_superuser)],)
async def create_new_meeting_room(
        meeting_room: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
  #  await check_name_duplicate(meeting_room.name, session)
    new_room = await charity_project_crud.create(meeting_room, session)
    return new_room


@router.get('/',
            response_model=list[CharityProjectDB],
            response_model_exclude_none=True,)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.patch('/{project_id}',
              response_model=CharityProjectDB,
              response_model_exclude_none=True,
              dependencies=[Depends(current_superuser)],)
async def partially_update_meeting_room(
        project_id: int,
        obj_in: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    # """Только для суперюзеров."""
    # meeting_room = await check_meeting_room_exists(
    #     meeting_room_id, session
    # )

    # if obj_in.name is not None:
    #     await check_name_duplicate(obj_in.name, session)
    charity_project = await charity_project_crud.update(
        project_id, obj_in, session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_meeting_room(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    # """Только для суперюзеров."""
    # # Выносим повторяющийся код в отдельную корутину.
    # meeting_room = await check_meeting_room_exists(
    #     meeting_room_id, session
    # )
    charity_project = await charity_project_crud.remove(
        project_id, session
    )
    return charity_project
