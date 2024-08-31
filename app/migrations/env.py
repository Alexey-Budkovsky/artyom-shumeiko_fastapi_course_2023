from logging.config import fileConfig
import sys
from os.path import abspath, dirname

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context


sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
# -->
"""
Команда `sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))` используется для динамической настройки пути поиска модулей в Python. Давайте разберем, как она работает и зачем она нужна.

### Объяснение команды

1. **`__file__`**: 
   - В Python `__file__` — это специальная переменная, которая содержит путь к файлу, из которого выполняется текущий скрипт. В данном случае это путь к файлу `env.py`, который является частью Alembic миграций.

2. **`abspath(__file__)`**:
   - Функция `abspath()` из модуля `os.path` преобразует путь к файлу в абсолютный путь. Абсолютный путь — это полный путь от корневой директории до файла, например, `/home/user/project/app/migrations/env.py`.

3. **`dirname(...)`**:
   - Функция `dirname()` также из модуля `os.path` возвращает имя директории, в которой находится указанный файл. Если последовательно вызвать `dirname()` несколько раз, можно подниматься по структуре директорий вверх.
   - В данном коде используется три вызова `dirname()`, что позволяет подняться на три уровня вверх от текущего файла:
     - Первый `dirname()` возвращает директорию `migrations`.
     - Второй `dirname()` возвращает директорию `app`.
     - Третий `dirname()` возвращает корневую директорию проекта, где находятся другие модули и файлы проекта.

   Пример:
   - Если путь до файла `env.py` равен `/home/user/project/app/migrations/env.py`, то после выполнения команды `dirname(dirname(dirname(abspath(__file__))))` результатом будет `/home/user/project`.

4. **`sys.path.insert(0, ...)`**:
   - `sys.path` — это список путей, в которых Python ищет модули для импорта. В начале выполнения скрипта этот список содержит стандартные пути, такие как директория, где находится скрипт, и пути до установленных пакетов.
   - Команда `sys.path.insert(0, ...)` добавляет новый путь в начало этого списка. Добавление в начало списка (`index 0`) означает, что этот путь будет приоритетным при поиске модулей. Python будет сначала искать модули в этом пути, а затем в остальных.

### Зачем это нужно?
В данном коде это делается для того, чтобы гарантировать, что при импорте модулей `app.database` и `app.hotels.models` Python сможет найти их в корневой директории проекта (`/home/user/project` в нашем примере). Без этого добавления пути, Python мог бы не найти эти модули, так как скрипт `env.py` выполняется в контексте директории `migrations`, которая находится глубже в структуре проекта.

Таким образом, эта команда позволяет импортировать модули из корневой директории проекта независимо от того, где находится выполняемый файл (`env.py` в данном случае).
"""

# --> позволяет передать метаданные из `Base` в `target_metadata` (ниже)
from app.database import Base, DATABASE_URL
# --> связывает классы `Base` и `Hotels`
# --> передавая метаданные `Hotels` в `Base` ==>
from app.hotels.models import Hotels


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

config.set_main_option("sqlalchemy.url", f"{DATABASE_URL}?async_fallback=True")
# -->
"""
Этот фрагмент кода настраивает объект конфигурации Alembic для работы с асинхронным двигателем SQLAlchemy. Давайте подробно рассмотрим, что происходит в этих двух строках.

### 1. `config = context.config`
- **`context.config`**: `context` — это объект, предоставляемый Alembic, который содержит глобальную конфигурацию для выполнения миграций. `context.config` возвращает объект конфигурации Alembic, который предоставляет доступ к параметрам, определенным в конфигурационном файле Alembic (например, `alembic.ini`).
- **`config`**: Эта переменная теперь содержит ссылку на объект конфигурации Alembic, который можно использовать для доступа и модификации настроек миграций.

### 2. `config.set_main_option("sqlalchemy.url",f"{DATABASE_URL}?async_fallback=True")`
- **`config.set_main_option("sqlalchemy.url", ...)`**: Эта строка устанавливает или переопределяет значение параметра конфигурации `sqlalchemy.url`. Параметр `sqlalchemy.url` в Alembic используется для указания URL-адреса подключения к базе данных. Это ключевой параметр, который указывает Alembic, как подключиться к базе данных для выполнения миграций.
  
- **`f"{DATABASE_URL}?async_fallback=True"`**: 
  - **`DATABASE_URL`**: Это строка подключения к базе данных, сформированная ранее в коде. Например, она может выглядеть так: `postgresql+asyncpg://user:password@localhost:5432/dbname`.
  - **`?async_fallback=True`**: Это дополнительный параметр, который добавляется к строке подключения. Он указывает SQLAlchemy использовать синхронное выполнение запросов, если асинхронный движок не поддерживается в текущем контексте. Этот параметр полезен, когда вам нужно обеспечить совместимость с инструментами, которые не поддерживают асинхронные операции (например, Alembic).

### Зачем это нужно?
- **Управление конфигурацией**: Этот код позволяет динамически изменять настройки конфигурации Alembic перед выполнением миграций. Вместо того чтобы жестко задавать URL базы данных в файле `alembic.ini`, он задается программно, что позволяет гибко менять его в зависимости от условий выполнения.
- **Асинхронность**: Добавление параметра `?async_fallback=True` позволяет Alembic корректно работать с асинхронными движками, такими как `asyncpg`. Это важно для проектов, использующих асинхронные технологии, но требующих синхронных операций для выполнения миграций.

### Итог
Этот фрагмент кода конфигурирует Alembic для работы с базой данных, задавая URL подключения и обеспечивая совместимость с асинхронными и синхронными режимами работы SQLAlchemy.
"""

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
