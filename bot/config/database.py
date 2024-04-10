import datetime
from typing import Annotated
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import func, MetaData, TIMESTAMP
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config.config import settings
from contextlib import asynccontextmanager

engine = create_async_engine(url=settings.sqlalchemy_database_uri, echo=True)

async_session = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)


naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


created_at = Annotated[
    datetime.datetime, mapped_column(server_default=func.current_timestamp())
]
updated_at = Annotated[
    datetime.datetime, mapped_column(server_default=func.current_timestamp(), onupdate=func.current_timestamp())
]


class Base(DeclarativeBase):

    metadata = MetaData(
        naming_convention=naming_convention
    )
    type_annotation_map = {
        datetime.datetime: TIMESTAMP(timezone=False),
    }

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


@asynccontextmanager
async def db_session() -> AsyncSession:
    session = async_session()
    try:
        yield session
    finally:
        await session.close()

