from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.schemas.donation import DonationCreate, DonationDB, DonationBase
from app.services.investment import investment
from app.models import User

router = APIRouter()


@router.post('/',
             response_model=DonationCreate,
             response_model_exclude_none=True)
async def create_donation(
        donation: DonationBase,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(donation, session, user)
    await investment(new_donation, session)
    await session.refresh(new_donation)
    return new_donation


@router.get('/',
            response_model=list[DonationDB],
            response_model_exclude_none=True,
            dependencies=[Depends(current_superuser)],)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров.
    Возвращает список всех пожертвований."""
    donations = await donation_crud.get_multi(session)
    return donations


@router.get('/my',
            response_model=list[DonationCreate],
            dependencies=[Depends(current_user)],)
async def get_my_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    donations = await donation_crud.get_donations_by_user(user, session)
    return donations