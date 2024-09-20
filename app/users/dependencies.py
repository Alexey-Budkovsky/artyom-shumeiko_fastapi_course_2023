from fastapi import Request, Depends
from jose import jwt, JWTError
from datetime import datetime, timezone

from app.config import settings
from app.exceptions import TokenExpiredException, TokenAbsentException, IncorrectTokenFormatException, \
    UserNotPresentException
from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token=token,
            key=settings.ENCRYPTION_KEY,
            algorithms=[settings.ENCRYPTION_ALGORITHM],
        )
    except JWTError:
        raise IncorrectTokenFormatException
    expire = payload.get('exp')
    if (not expire) or (int(expire) < int(datetime.now(timezone.utc).timestamp())):
        raise TokenExpiredException
    user_id = payload.get('sub')
    if not user_id:
        raise UserNotPresentException
    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserNotPresentException
    return user


async def get_current_admin_user(current_user: UsersDAO = Depends(get_current_user)):
    # if current_user.role != 'admin':
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return current_user
