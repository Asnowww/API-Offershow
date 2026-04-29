from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings


db_metadata = MetaData(schema=get_settings().postgres_schema)


class Base(DeclarativeBase):
    metadata = db_metadata
