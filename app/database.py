from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


engine = create_async_engine(settings.DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


# ================================================= database.py
"""
Этот код настраивает подключение к базе данных PostgreSQL с использованием SQLAlchemy в асинхронном режиме и задает базовый класс для ORM (Object-Relational Mapping). Давайте разберем каждую часть кода подробнее.

### 1. Импортирование нужных модулей
```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
```
- **`AsyncSession`**: Асинхронная версия сессии SQLAlchemy. Она используется для выполнения асинхронных запросов к базе данных.
- **`create_async_engine`**: Функция для создания асинхронного двигателя (engine) SQLAlchemy, который управляет пулом соединений и выполняет SQL-запросы.
- **`DeclarativeBase`**: Базовый класс для декларативной ORM модели в SQLAlchemy.
- **`sessionmaker`**: Фабрика для создания сессий. Она настраивается для работы с определенным двигателем (engine).

### 2. Настройки подключения к базе данных
```python
DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASS = "postgres"
DB_NAME = "postgres"

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
```
- **Параметры подключения**: Здесь указываются данные для подключения к базе данных:
  - `DB_HOST`: Адрес хоста базы данных (в данном случае локальный компьютер).
  - `DB_PORT`: Порт, на котором работает PostgreSQL (стандартный порт — 5432).
  - `DB_USER`: Имя пользователя базы данных.
  - `DB_PASS`: Пароль для этого пользователя.
  - `DB_NAME`: Имя базы данных.
- **`DATABASE_URL`**: Формируется строка подключения (URL) к базе данных в формате, который понимает SQLAlchemy. `postgresql+asyncpg` указывает на использование PostgreSQL с асинхронным драйвером `asyncpg`.

### 3. Создание асинхронного двигателя
```python
engine = create_async_engine(DATABASE_URL)
```
- **`engine`**: Это объект, который управляет пулом соединений к базе данных и выполняет SQL-запросы. Он настроен на использование асинхронного режима работы с базой данных через `asyncpg`.

### 4. Создание фабрики сессий
```python
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```
- **`async_session_maker`**: Это фабрика, которая создает экземпляры `AsyncSession`, используя `engine`. Важно:
  - `class_ = AsyncSession` указывает, что сессии будут асинхронными.
  - `expire_on_commit=False`: Указывает, что данные в сессии не будут автоматически сбрасываться после фиксации (commit). Это полезно, если вы хотите продолжить работу с объектами после фиксации транзакции.

### 5. Определение базового класса для ORM моделей
```python
class Base(DeclarativeBase):
    pass
```
- **`Base`**: Это базовый класс, от которого будут наследоваться все ORM-модели. Этот класс позволяет SQLAlchemy знать, что все классы, которые наследуются от `Base`, являются моделями базы данных. Обычно в этом классе не определяются дополнительные методы, так как это просто основа для всех моделей.

### Итог

В этом коде выполнена настройка подключения к PostgreSQL в асинхронном режиме, создано асинхронное соединение с базой данных, а также настроена ORM-структура, которую можно использовать для определения моделей базы данных. Этот код является основой для работы с базой данных в асинхронных веб-приложениях на FastAPI.
"""
# Объект класса Base создаётся через механизм dependency injection ? ==>
"""
Нет, объект класса `Base` в SQLAlchemy не создаётся через механизм Dependency Injection (внедрение зависимостей) FastAPI.

### Что такое `Base` в SQLAlchemy?
`Base` — это класс, который используется в SQLAlchemy как основа для создания моделей базы данных. В контексте SQLAlchemy и Pydantic, `Base` служит для декларативного определения моделей, которые затем используются для взаимодействия с базой данных.

Пример создания модели на основе `Base`:
```python
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
```

### Как создаётся объект класса `Base`?
Класс `Base` не является объектом, который должен быть "создан" или "инициализирован" как обычный объект. Он выступает как метакласс для ORM моделей, и экземпляры `Base` создаются неявно, когда вы создаёте таблицы на его основе.

### Dependency Injection в FastAPI
Dependency Injection в FastAPI — это механизм передачи объектов или функций в маршруты или другие зависимости через специальный декоратор `Depends`. Например:

```python
from fastapi import Depends

def get_db():
    db = async_session_maker()
    try:
        yield db
    finally:
        await db.close()

@app.get("/users/")
async def read_users(db: AsyncSession = Depends(get_db)):
    users = await db.execute(select(User))
    return users.scalars().all()
```

В этом примере `Depends` используется для внедрения зависимости `get_db`, которая возвращает асинхронную сессию базы данных.

### Заключение
Класс `Base` не используется через механизм Dependency Injection. Он используется как декларативная основа для создания ORM моделей в SQLAlchemy, и экземпляры `Base` (таблицы и объекты базы данных) создаются не напрямую, а через определение классов-моделей и последующую работу с базой данных через сессии SQLAlchemy.
"""
