"""
Database session management.
Supports both PostgreSQL and SQLite (auto-detected from DATABASE_URL).
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings

# ------------------------------------------------------------
# Engine — adapt settings based on dialect
# ------------------------------------------------------------
_is_sqlite = settings.DATABASE_URL.startswith("sqlite")

_engine_kwargs: dict = {}

if _is_sqlite:
    _engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    _engine_kwargs["pool_pre_ping"] = True  # verify connections (handles Railway sleep/wake)

engine = create_engine(settings.DATABASE_URL, **_engine_kwargs)

# Enable WAL mode and foreign keys for SQLite (improves concurrency & integrity)
if _is_sqlite:
    @event.listens_for(engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# ------------------------------------------------------------
# Session Factory
# ------------------------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ------------------------------------------------------------
# Declarative Base
# ------------------------------------------------------------
class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


# ------------------------------------------------------------
# Dependency for FastAPI routes
# ------------------------------------------------------------
def get_db():
    """
    FastAPI dependency that provides a database session
    and ensures it's closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
