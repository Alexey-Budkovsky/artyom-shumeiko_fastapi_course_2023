# data access object --> DAO
# -----------------------------
from sqlalchemy.dialects.postgresql.pg_catalog import pg_enum

from app.database import async_session_maker
from sqlalchemy import select, insert


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

# =============================================== `execute`
"""
В данном коде для работы с базой данных используется SQLAlchemy. Метод `execute()` выполняет SQL-запросы асинхронно в рамках сессии базы данных. Рассмотрим его работу более подробно.

### Как работает `execute()`:

1. **Создание сессии**:
   В каждом методе используется асинхронный контекстный менеджер `async with async_session_maker() as session`, который создает и открывает сессию базы данных. Эта сессия управляет транзакциями, соединениями с базой данных и выполнением SQL-запросов.

2. **Выполнение запроса**:
   После создания сессии выполняется метод `execute(query)`, который отправляет SQL-запрос в базу данных и возвращает результат.
   
   - В методах `find_by_id`, `find_one_or_none`, и `find_all` передается объект запроса, созданный с помощью `select(cls.model)` и различных фильтров (например, `filter_by()`).
   - В методе `add` создается запрос вставки данных с помощью `insert(cls.model).values(**data)`.

3. **Асинхронность**:
   Важной частью является то, что `execute()` здесь — это асинхронный метод. Он работает в связке с асинхронной сессией (`AsyncSession`), позволяя выполнять запросы без блокировки основного потока приложения.

4. **Возвращаемые данные**:
   В зависимости от типа запроса `execute()` возвращает различные объекты:
   - В `find_by_id` и `find_one_or_none` результат `execute()` передается в метод `scalar_one_or_none()`, который возвращает либо единственную запись (если она найдена), либо `None`, если записи не найдено.
   - В `find_all` метод `scalars().all()` возвращает список всех результатов.
   - В `add` запрос на вставку данных завершится подтверждением транзакции с помощью `commit()`.

### Визуализация процесса:
- Когда вызывается метод, например, `find_by_id`, создается сессия с базой данных.
- Далее формируется SQL-запрос `SELECT ... FROM ... WHERE id = :model_id` (через метод `select()`).
- Запрос передается в метод `session.execute()`, который отправляет его в базу данных.
- Результат запроса извлекается и возвращается в методе с помощью вызова `scalar_one_or_none()`.

Пример использования:

```python
# Поиск записи с id=5
user = await BaseDAO.find_by_id(5)
if user:
    print(user)
```

В этом примере будет выполнен запрос к базе данных, который вернет объект с id=5 (или None, если запись не найдена).
"""