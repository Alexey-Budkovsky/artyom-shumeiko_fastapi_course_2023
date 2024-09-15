from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user, get_current_admin_user
from app.users.models import Users
from app.users.schemas import SUserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"],
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500)
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {
        'access_token': access_token
    }


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    return {
        "message": "User has logged out of the booking system"
    }


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.get("/all")
async def read_users_all(current_user: Users = Depends(get_current_admin_user)):
    return await UsersDAO.find_all()


# =============================================== {"sub": user.id}
"""
В коде FastAPI, фрагмент `{"sub": user.id}` используется для создания **JSON Web Token (JWT)** при аутентификации пользователя. Давайте разберёмся с тем, как это работает и зачем это нужно:

### JWT (JSON Web Token)
JWT — это компактный, URL-безопасный способ представления утверждений между двумя сторонами. Обычно он состоит из трёх частей: заголовка (header), полезной нагрузки (payload) и подписи (signature).

- **Заголовок** содержит тип токена и алгоритм подписи (например, `HS256`).
- **Полезная нагрузка (payload)** содержит утверждения (claims). Это информация, которую сервер хочет передать в токене.
- **Подпись** используется для проверки целостности токена.

### Что означает `{"sub": user.id}`?
Полезная нагрузка токена содержит утверждения, которые могут быть стандартизированными или пользовательскими.

- **`sub`** — это стандартное поле (зарезервированное), обозначающее **subject** (субъект) — то есть, идентификатор субъекта, которому предназначен токен. В контексте аутентификации, это обычно идентификатор пользователя.
- **`user.id`** — это уникальный идентификатор пользователя (например, из базы данных), который аутентифицируется.

Таким образом, `{"sub": user.id}` в JWT полезной нагрузке сообщает, что токен создан для пользователя с данным идентификатором. Этот идентификатор будет передаваться в токене и может быть использован для проверки того, какой пользователь аутентифицирован при запросах к защищённым маршрутам.

### Пример JWT payload:
Пример содержимого полезной нагрузки JWT, созданного с этим фрагментом:
```json
{
  "sub": 123,  // user.id
  "exp": 1628389493  // Время истечения токена
}
```
Здесь `"sub": 123` — это идентификатор пользователя с ID 123, который был аутентифицирован, и токен содержит эту информацию.

### Использование `sub`
Когда пользователь отправляет JWT в запросах к защищённым ресурсам, сервер может извлечь `sub` из токена и использовать его для идентификации аутентифицированного пользователя, например, для получения данных пользователя или выполнения проверок доступа.

### Заключение
`{"sub": user.id}` в коде FastAPI используется для того, чтобы связать JWT с конкретным пользователем, и передать его ID в токене, который будет использоваться для последующей авторизации.
"""

# =============================================== set_cookie
"""
Метод `set_cookie` в FastAPI (через `Starlette` и `Response`) используется для установки cookies в HTTP-ответе. Этот метод имеет несколько параметров, которые контролируют поведение и свойства cookies. Давайте рассмотрим каждый из них подробно:

### Аргументы метода `set_cookie`

1. **`key: str`** (обязательный)
   - Название cookie.
   - Это ключ, под которым cookie будет храниться в браузере.
   - Пример: `"session_id"`.

2. **`value: str = ""`** (по умолчанию: пустая строка)
   - Значение cookie.
   - Это данные, которые будут храниться в cookie.
   - Пример: `"1234567890abcdef"`.

3. **`max_age: int | None = None`** (по умолчанию: `None`)
   - Время жизни cookie в секундах.
   - Если указано, то cookie будет удалено через указанное количество секунд после установки.
   - Пример: `3600` — cookie будет действовать один час.

4. **`expires: datetime | str | int | None = None`** (по умолчанию: `None`)
   - Дата истечения срока действия cookie.
   - Можно указать как `datetime` объект, строку в формате времени, или количество секунд.
   - Пример: `expires=datetime(2024, 12, 31)` — cookie истечет 31 декабря 2024 года.

5. **`path: str | None = "/"`** (по умолчанию: `/`)
   - Путь, для которого cookie будет доступен.
   - Определяет, для каких URL на сайте cookie будет отправляться.
   - Пример: `path="/user"` — cookie будет отправляться только для запросов, начинающихся с `/user`.

6. **`domain: str | None = None`** (по умолчанию: `None`)
   - Домен, для которого cookie будет доступен.
   - Если указано, cookie будет доступен только для запросов на этот домен.
   - Пример: `domain="example.com"` — cookie будет доступен только для запросов на `example.com`.

7. **`secure: bool = False`** (по умолчанию: `False`)
   - Указывает, что cookie должно передаваться только через защищённые соединения (по HTTPS).
   - Если установлено в `True`, cookie не будет отправлено при HTTP-запросах.
   - Пример: `secure=True` — cookie будет отправляться только по HTTPS.

8. **`httponly: bool = False`** (по умолчанию: `False`)
   - Указывает, что cookie должно быть доступно только серверу и не должно быть доступно через JavaScript (свойство `HttpOnly`).
   - Если установлено в `True`, JavaScript на странице не сможет прочитать cookie.
   - Пример: `httponly=True` — cookie доступно только серверу, для защиты от XSS-атак.

9. **`samesite: Literal["lax", "strict", "none"] | None = "lax"`** (по умолчанию: `lax`)
   - Политика SameSite для защиты от CSRF-атак.
     - `"lax"`: cookie будет отправляться для большинства запросов, но не для всех (например, для POST-запросов, идущих с других сайтов).
     - `"strict"`: cookie будет отправляться только для запросов с того же сайта.
     - `"none"`: cookie будет отправляться для всех запросов, включая межсайтовые.
   - Пример: `samesite="strict"` — cookie отправляется только для запросов, идущих с того же домена.

### Пример использования

```python
from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI()

@app.get("/setcookie")
async def set_cookie_example(response: Response):
    response.set_cookie(
        key="session_id",
        value="abcdef123456",
        max_age=3600,  # 1 час
        expires=3600,  # 1 час
        path="/",
        domain="example.com",
        secure=True,
        httponly=True,
        samesite="lax"
    )
    return {"message": "Cookie set!"}
```

### Краткий итог:
Метод `set_cookie` позволяет вам управлять тем, как cookie будет храниться в браузере: срок действия, доступность по протоколу (HTTP/HTTPS), защита от XSS и CSRF, и другие свойства.
"""
