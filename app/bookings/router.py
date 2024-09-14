from fastapi import APIRouter, Depends
from app.bookings.dao import BookingDAO
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)):
    # print('* user:', user)
    # print('* type(user):',type(user))
    # print('* user.id',user.id)
    # print('* user.email',user.email)
    # return user
    return await BookingDAO.find_all(id=1)
