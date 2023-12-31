from typing import List

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (spreadsheets_create, set_user_permissions,
                                     spreadsheets_update_value)
from app.models import CharityProject

router = APIRouter()


@router.post(
    '/',
    response_model=str,
    dependencies=[Depends(current_superuser)],)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
) -> List[CharityProject]:
    """Только для суперюзеров."""
    charity_projects = await charity_project_crud.get_projects_by_completion_rate(
        session)
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    return await spreadsheets_update_value(
        spreadsheetid,
        charity_projects,
        wrapper_services)
