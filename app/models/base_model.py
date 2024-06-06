from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    declarative_base,
    declared_attr,
    mapped_column,
)


class ModelBase:
    """
    Attributes:
        id (UUID): Unique identifier for the model instance.
        created_at (DateTime): Timestamp of creation.
        updated_at (DateTime): Timestamp of the last update.
        deleted_at (DateTime): Timestamp of soft deletion (if applicable).
    """

    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=ModelBase)