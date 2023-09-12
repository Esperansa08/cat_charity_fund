from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# from app.api.validators import (check_meeting_room_exists,
#                                 check_reservation_intersections,
#                                 check_reservation_before_edit)
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.schemas.donation import DonationCreate, DonationDB, DonationBase
from app.services.donation import get_donation_balance, set_donation_invested
from app.models import User

router = APIRouter()


@router.post('/', response_model=DonationCreate)
async def create_donation(
        donation: DonationBase,
        session: AsyncSession = Depends(get_async_session),
        #user: User = Depends(current_user),
):
    donation_invested = await get_donation_balance(donation.full_amount, session)
    new_donation = await donation_crud.create(donation, session)
    if donation.full_amount != donation_invested:
        await set_donation_invested(new_donation, donation_invested, session)
    return new_donation



@router.get('/',
            response_model=list[DonationDB],)
           # dependencies=[Depends(current_user)],)
async def get_all_new_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    donations = await donation_crud.get_multi(session)
    return donations


@router.get('/my',
            response_model=list[DonationCreate],
            dependencies=[Depends(current_user)],)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    donations = await donation_crud.get_multi(session)
    return donations