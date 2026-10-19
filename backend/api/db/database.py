from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api.core.config import get_settings


def get_db_engine():
    settings = get_settings()
    database_url = settings.sqlalchemy_url
    if not database_url:
        raise RuntimeError("DB_URL is not configured")

    engine_options = {"pool_pre_ping": True}
    if database_url.startswith("sqlite"):
        engine_options["connect_args"] = {"check_same_thread": False}
    else:
        engine_options.update({"pool_size": 32, "max_overflow": 64})

    return create_engine(database_url, **engine_options)


db_engine = get_db_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
Base = declarative_base()


def create_database():
    return Base.metadata.create_all(bind=db_engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
