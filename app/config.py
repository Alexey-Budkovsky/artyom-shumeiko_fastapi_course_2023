from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    class Config:
        env_file = ".env"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()

print(settings.DATABASE_URL)

# -->
"""
Этот код на Python использует библиотеку Pydantic для работы с переменными окружения и создания настроек для FastAPI. Вот как он работает:

### 1. Импорт необходимых модулей

```python
from pydantic_settings import BaseSettings
```
Этот импорт включает класс `BaseSettings` из библиотеки `pydantic_settings`. `BaseSettings` позволяет автоматически загружать переменные окружения из файлов `.env` и других источников.

### 2. Определение класса настроек `Settings`

```python
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
```
Класс `Settings` наследуется от `BaseSettings`. В нём определены атрибуты для хранения информации о подключении к базе данных:

- `DB_HOST`: Адрес сервера базы данных.
- `DB_PORT`: Порт, на котором работает база данных.
- `DB_USER`: Имя пользователя базы данных.
- `DB_PASS`: Пароль для доступа к базе данных.
- `DB_NAME`: Название базы данных.

### 3. Конфигурация для загрузки переменных окружения

```python
    class Config:
        env_file = ".env"
```
Вложенный класс `Config` определяет конфигурацию для класса `Settings`. Он указывает, что переменные окружения должны загружаться из файла `.env`. Это файл, в котором можно хранить конфиденциальные данные, такие как пароли и ключи API, отдельно от кода.

### 4. Вычисляемое свойство `DATABASE_URL`

```python
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
```
Метод `DATABASE_URL` использует декоратор `@property`, чтобы сделать его свойством объекта `Settings`. Это означает, что `DATABASE_URL` будет вычисляться при каждом обращении к нему, и его значение будет строкой подключения к базе данных.

Формат строки подключения:
- `postgresql+asyncpg://` — Указывает на использование PostgreSQL с асинхронным драйвером `asyncpg`.
- `{self.DB_USER}:{self.DB_PASS}` — Имя пользователя и пароль для подключения.
- `{self.DB_HOST}:{self.DB_PORT}` — Хост и порт базы данных.
- `/{self.DB_NAME}` — Имя базы данных.

### 5. Создание экземпляра класса `Settings` и использование `DATABASE_URL`

```python
settings = Settings()

print(settings.DATABASE_URL)
```
Здесь создаётся экземпляр класса `Settings`. При этом автоматически загружаются все переменные окружения из файла `.env`. Затем выводится на экран строка подключения `DATABASE_URL`, которая формируется на основе загруженных значений.

### Итог

Этот код предоставляет удобный способ управления конфигурацией приложения, автоматически загружая переменные окружения и предоставляя вычисляемое свойство для строки подключения к базе данных. Это делает код более чистым, организованным и легко настраиваемым.
"""