from fastapi import APIRouter
from sqlalchemy import select

from app.database import async_session_maker
from app.bookings.models import Bookings


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings():
    async with async_session_maker() as session:
        query = select(Bookings)  # SELECT * FROM bookings
        result = await session.execute(query)
        # print(result)
        # print(result.all())
        # print(result.scalars().all())
        # --> Booking.id
        # --> Booking.total_cost
        return result.scalars().all()