from jose import jwt
from datetime import datetime, timedelta, timezone


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    print(expire)
    print(type(expire))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        key='dsdasdDSAADS',
        algorithm='HS256'
    )
    return encoded_jwt


res = create_access_token({"user": "Bilbo"})
print(res)
