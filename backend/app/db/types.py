"""
Portable SQLAlchemy column types that work across SQLite and PostgreSQL.

- GUID: stores UUIDs as CHAR(32) on SQLite, native UUID on Postgres.
- JSONB_COMPAT: uses JSON on SQLite, JSONB on Postgres.
"""

import uuid

from sqlalchemy import types, String, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB


class GUID(types.TypeDecorator):
    """Platform-independent UUID type.

    Uses PostgreSQL's UUID type when available,
    otherwise stores as CHAR(32) (hex-encoded, no dashes).
    """

    impl = types.CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(types.CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return value if isinstance(value, uuid.UUID) else uuid.UUID(value)
        else:
            if isinstance(value, uuid.UUID):
                return value.hex
            else:
                return uuid.UUID(value).hex

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(value)


class JSONB_COMPAT(types.TypeDecorator):
    """Platform-independent JSON/JSONB type.

    Uses PostgreSQL's JSONB when available, otherwise plain JSON.
    """

    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB())
        else:
            return dialect.type_descriptor(JSON())
