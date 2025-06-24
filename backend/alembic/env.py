# backend/alembic/env.py
from logging.config import fileConfig
import asyncio
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Добавляем путь к пакету backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.db import Base  # SQLAlchemy Base
# Импорт всех моделей для регистрации метаданных
from models import student, teacher, subject, teacher_subject, parent, grade, schedule, attendance, administrator, class_  # noqa

from core.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Подставляем строку подключения к БД из settings
config.set_main_option('sqlalchemy.url', str(settings.DATABASE_URL))

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()