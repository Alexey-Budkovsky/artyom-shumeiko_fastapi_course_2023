import bcrypt
from jose import jwt
from datetime import datetime, timedelta, timezone
from pydantic import EmailStr

from app.users.dao import UsersDAO
from app.config import settings


# Hash a password using bcrypt
def get_password_hash(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode('utf-8')


# Check if the provided password matches the stored password (hashed)
def verify_password(plain_password, hashed_password):
    password_byte_enc = plain_password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(
        password=password_byte_enc,
        hashed_password=hashed_password
    )


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        key=settings.ENCRYPTION_KEY,
        algorithm=settings.ENCRYPTION_ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user and not verify_password(password, user.hashed_password):
        return None
    return user


# =============================================== bcrypt
"""
`bcrypt` — это библиотека для безопасного хэширования паролей. Она использует криптографический алгоритм `bcrypt`, который разработан специально для защиты паролей. Основная особенность этого алгоритма заключается в том, что он добавляет "соль" к паролю перед хэшированием и делает процесс хэширования ресурсоёмким, что усложняет атаки методом перебора.

### Важные особенности `bcrypt`:
1. **Добавление соли (salt)**: перед хэшированием к паролю добавляется случайная строка (соль). Это защищает от атак с использованием радужных таблиц (precomputed hashes).
2. **Медлительность**: `bcrypt` специально разработан так, чтобы быть медленным, что усложняет взлом паролей путём перебора всех возможных вариантов (brute-force).
3. **Регулируемая сложность**: сложность хэширования можно регулировать, увеличивая или уменьшая затраты времени и ресурсов.

### Разбор кода:
```python
import bcrypt

# Функция для хэширования пароля с использованием bcrypt
def get_password_hash(password):
    # Преобразуем строковый пароль в байты (т.к. bcrypt работает с байтами)
    pwd_bytes = password.encode('utf-8')
    
    # Генерируем соль, которая будет добавлена к паролю перед хэшированием
    salt = bcrypt.gensalt()
    
    # Хэшируем пароль с добавленной солью
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    
    # Возвращаем хэшированный пароль в строковом формате
    return hashed_password.decode('utf-8')
```

### Описание шагов:
1. **`password.encode('utf-8')`** — преобразует строку пароля в байты, так как `bcrypt` РАБОТАЕТ С БАЙТАМИ.
   
2. **`bcrypt.gensalt()`** — генерирует соль (случайные данные), которая будет добавлена к паролю. Соль уникальна для каждого пароля.

3. **`bcrypt.hashpw(password=pwd_bytes, salt=salt)`** — хэширует байтовую строку пароля, используя алгоритм `bcrypt` и сгенерированную соль.

4. **`hashed_password.decode('utf-8')`** — преобразует хэшированный пароль из байтов обратно в строку для удобного хранения в базе данных.

### Пример:
Если пароль `"mypassword"`, то он будет преобразован в байты, затем к нему будет добавлена соль, и результатом работы функции будет строка, представляющая хэшированный пароль с солью, например: 
`"$2b$12$WQ6DvsQ0xMv4y6IOhGZPbOFVpZW8upnTfyM4G5xuCGmK2zGwMOnbO"`.
"""
