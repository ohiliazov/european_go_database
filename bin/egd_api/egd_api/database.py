from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from .config import app_settings

engine = create_engine(app_settings.database_uri, echo=app_settings.debug_mode)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Iterator[scoped_session[Session]]:
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()
