# Change the parent class for the sqlachemy models, so repetative fields like 'created_at' and methods would be properly handled

from typing import TypeVar, Type, Optional, Any
from sqlalchemy.orm import Session, declared_attr, object_session
from sqlalchemy import Column, DateTime, func, Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr, declarative_base

# Create a generic type for the base class
T = TypeVar("T", bound="BaseMixin")


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseMixin:
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)
    is_active = Column(Boolean, default=True, nullable=False)

    @classmethod
    def find_by_id(cls: Type[T], db_session: Session, _id: UUID) -> Optional[T]:
        return (
            db_session.query(cls).filter(cls.id == _id, cls.is_active == True).first()
        )

    @classmethod
    def find_all(cls: Type[T], db_session: Session) -> list[T]:
        return db_session.query(cls).filter(cls.is_active == True).all()

    @classmethod
    def create(cls: Type[T], db_session: Session, **kwargs) -> T:
        instance = cls(**kwargs)
        db_session.add(instance)
        db_session.commit()
        db_session.refresh(instance)
        return instance

    def update(self, db_session: Session, **kwargs) -> T:
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        db_session.commit()
        db_session.refresh(self)
        return self

    def soft_delete(self, db_session: Optional[Session] = None) -> None:
        self.is_active = False
        db_session = db_session or object_session(self)
        db_session.commit()

    def delete(self, db_session: Optional[Session] = None) -> None:
        db_session = db_session or object_session(self)
        db_session.delete(self)
        db_session.commit()

    @classmethod
    def deactivate_all(cls: Type[T], db_session: Session, ids: list[UUID]) -> None:
        db_session.query(cls).filter(cls.id.in_(ids)).update(
            {cls.is_active: False}, synchronize_session="fetch"
        )
        db_session.commit()

    @classmethod
    def bulk_create(cls: Type[T], db_session: Session, items: list[dict]) -> list[T]:
        instances = [cls(**item) for item in items]
        db_session.bulk_save_objects(instances)
        db_session.commit()
        return instances

    @classmethod
    def search(
        cls: Type[T],
        db_session: Session,
        filters: dict[str, str | list[str] | dict[str, Any]],
    ) -> list[T]:
        """
        Perform an advanced search with various filters. Filters can be a simple string match, a list of possible values, or a range.
        """
        query = db_session.query(cls)
        for attribute, value in filters.items():
            if isinstance(value, dict):
                # Assuming the dictionary has keys 'min' and/or 'max' for range values
                if "min" in value:
                    query = query.filter(getattr(cls, attribute) >= value["min"])
                if "max" in value:
                    query = query.filter(getattr(cls, attribute) <= value["max"])
            elif isinstance(value, list):
                query = query.filter(getattr(cls, attribute).in_(value))
            else:
                query = query.filter(getattr(cls, attribute) == value)
        return query.all()

    @classmethod
    def sort_and_paginate(
        cls: Type[T],
        db_session: Session,
        sort_field: str,
        sort_order: str,
        page: int,
        page_size: int,
    ) -> list[T]:
        """
        Sort the results based on a given field and order, then paginate.
        """
        order_function = (
            func.lower(getattr(cls, sort_field))
            if isinstance(getattr(cls, sort_field).type, String)
            else getattr(cls, sort_field)
        )
        order_function = (
            order_function.asc() if sort_order == "asc" else order_function.desc()
        )

        return (
            db_session.query(cls)
            .order_by(order_function)
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

    @classmethod
    def get_by_multiple_ids(
        cls: Type[T], db_session: Session, ids: list[UUID]
    ) -> list[T]:
        """
        Get multiple records by a list of IDs.
        """
        return (
            db_session.query(cls).filter(cls.id.in_(ids), cls.is_active == True).all()
        )

    @classmethod
    def filter_by_attributes(
        cls: Type[T], db_session: Session, **attributes
    ) -> list[T]:
        """Filter items based on attribute values."""
        return db_session.query(cls).filter_by(**attributes, is_active=True).all()

    @classmethod
    def get_sorted_and_filtered(
        cls: Type[T],
        db_session: Session,
        sort_fields: list[tuple[str, str]],
        filter_criteria: dict[str, Any],
    ) -> list[T]:
        """
        Retrieve items sorted and filtered by given fields and criteria.
        """
        query = db_session.query(cls).filter_by(is_active=True)
        for attr, value in filter_criteria.items():
            if hasattr(cls, attr):
                query = query.filter(getattr(cls, attr) == value)
        for field, direction in sort_fields:
            if hasattr(cls, field):
                sort_attr = getattr(cls, field)
                query = query.order_by(
                    sort_attr.desc() if direction == "desc" else sort_attr
                )
        return query.all()

    @classmethod
    def bulk_update(
        cls: Type[T], db_session: Session, updates: dict[UUID, dict]
    ) -> None:
        """Bulk update items based on a dictionary of item IDs and their update values."""
        for item_id, update_values in updates.items():
            item = cls.find_by_id(db_session, item_id)
            if item:
                for key, value in update_values.items():
                    setattr(item, key, value)
        db_session.commit()

    @classmethod
    def find_with_filters(cls: Type[T], db_session: Session, **filters) -> list[T]:
        """
        Generic method to find records with given filters.
        """
        query = db_session.query(cls).filter_by(**filters)
        return query.all()

    @classmethod
    def get_sorted_by_field(
        cls: Type[T], db_session: Session, sort_field: str, descending: bool = False
    ) -> list[T]:
        """
        Get all records sorted by a specific field.
        """
        sort_by = (
            getattr(cls, sort_field).desc() if descending else getattr(cls, sort_field)
        )
        return db_session.query(cls).order_by(sort_by).all()
