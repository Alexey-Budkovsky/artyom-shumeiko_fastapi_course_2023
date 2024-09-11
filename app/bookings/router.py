from fastapi import APIRouter, Request
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(request: Request):  # -> list[SBooking]:
    print('request.cookies: ', request.cookies)
    print('request.url: ', request.url)
    print('request.client: ', request.client)
    # return dir(request)
