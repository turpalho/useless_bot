from sqlalchemy import(
    BigInteger, DateTime, Integer, Text, String, func,
    Boolean, MetaData, ForeignKey, Text, Table, Column, Index
)
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship


# Default naming convention for all indexes and constraints
# See why this is important and how it would save your time:
# https://alembic.sqlalchemy.org/en/latest/naming.html
convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': (
        'fk__%(table_name)s__%(all_column_names)s__'
        '%(referred_table_name)s'
    ),
    'pk': 'pk__%(table_name)s'
}
metadata = MetaData(naming_convention=convention)


# Registry for all tables
class Base(DeclarativeBase):
    metadata = metadata


class User(Base):
    __tablename__ = 'users'
    Base.metadata

    user_id = mapped_column(BigInteger, primary_key=True, index=True)
    first_name = mapped_column(Text, default=None)
    username = mapped_column(Text)
    # contact = mapped_column(Text)
    is_blocked = mapped_column(Boolean, default=False)
    create_at = mapped_column(DateTime, server_default=func.now()) # index=True

    __mapper_args__ = {"eager_defaults": True}


class Config(Base):
    __tablename__ = "config"

    id = mapped_column(Integer, primary_key=True)
    admins_ids = mapped_column(String(255))

    __mapper_args__ = {"eager_defaults": True}


async def create_db(db_user, db_password, db_host, db_name, echo) -> AsyncEngine:
    engine = create_async_engine(
        f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}/{db_name}",
        echo=echo,
    )
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return engine


async def dispose_db(engine: AsyncEngine) -> None:
    await engine.dispose()