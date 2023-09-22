from datetime import datetime
from typing import List

from app.models.base import PreBaseCharityDonation


def investment(
        target: PreBaseCharityDonation,
        sources: List[PreBaseCharityDonation]) -> List[PreBaseCharityDonation]:
    updated_objects = []
    if target.invested_amount is None:
        target.invested_amount = 0
    for source in sources:
        available_amount = min_value(target, source)
        updated_objects.append(source)
        change_objects(target, source, available_amount)
        if target.fully_invested:
            break
    return updated_objects


def min_value(target, source):
    return min(source.full_amount - source.invested_amount,
               target.full_amount - target.invested_amount)


def change_objects(target, source, available_amount):
    for investment in [target, source]:
        investment.invested_amount += available_amount
        investment.fully_invested = (
            investment.invested_amount == investment.full_amount
        )
        if investment.fully_invested:
            investment.close_date = datetime.now()
