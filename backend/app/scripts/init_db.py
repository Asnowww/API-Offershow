from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

from app.core.config import get_settings
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import entities  # noqa: F401
from app.scripts.seed_data import seed


def ensure_database_exists() -> None:
    settings = get_settings()
    target_url = settings.database_url
    admin_url = target_url.rsplit("/", 1)[0] + "/" + settings.postgres_admin_database
    db_name = target_url.rsplit("/", 1)[-1].split("?", 1)[0]
    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT", pool_pre_ping=True)
    with admin_engine.connect() as conn:
        exists = conn.execute(text("select 1 from pg_database where datname = :name"), {"name": db_name}).scalar()
        if not exists:
            try:
                conn.execute(text(f'create database "{db_name}" encoding \'UTF8\''))
            except ProgrammingError:
                print(f'warning: current PostgreSQL user cannot create database "{db_name}".')
    admin_engine.dispose()


def ensure_schema_exists() -> None:
    settings = get_settings()
    with engine.connect() as conn:
        conn.execute(text(f'create schema if not exists "{settings.postgres_schema}"'))
        conn.commit()


def main() -> None:
    ensure_database_exists()
    ensure_schema_exists()
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed(db)
    print("database initialized")


if __name__ == "__main__":
    main()
