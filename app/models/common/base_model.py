from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import (
    declared_attr,
    DeclarativeBase,
    mapped_column,
    Session,
    object_session,
    aliased,
)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class BaseMixin(ABC):
    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def find_by_id(cls, db_session: Session, _id: UUID) -> None:
        return (
            db_session.query(cls)
            .filter(cls.id == _id, cls.deleted_at.is_(None))
            .first()
        )

    @classmethod
    def find_all(cls, db_session: Session) -> None:
        return db_session.query(cls).filter(cls.deleted_at.is_(None)).all()

    @classmethod
    def find_by_multiple_ids(cls, db_session: Session, ids: list[UUID]) -> None:
        return db_session.query(cls).filter(cls.id.in_(ids)).all()

    @classmethod
    def create(cls, db_session: Session, **kwargs) -> None:
        instance = cls(**kwargs)
        db_session.add(instance)
        db_session.commit()
        return instance

    @classmethod
    def update(cls, db_session: Session, _id: UUID, **kwargs) -> None:
        instance = cls.find_by_id(db_session, _id)
        for attr, value in kwargs.items():
            setattr(instance, attr, value)
        db_session.commit()

    @classmethod
    def soft_delete(cls, db_session: Optional[Session], _id: UUID) -> None:
        instance = cls.find_by_id(db_session, _id)
        setattr(instance, "is_active", False)
        instance.deleted_at = func.now()
        db_session.commit()

    @classmethod
    def delete(cls, db_session: Optional[Session], _id: UUID) -> None:
        instance = cls.find_by_id(db_session, _id)
        db_session.delete(instance)
        db_session.commit()

    @classmethod
    def apply_filter_conditions(cls, query, attribute, value):
        """
        Apply filter conditions dynamically based on the type of value.
        """
        column = cls.__table__.c.get(attribute)
        if isinstance(value, dict) and "min" in value and "max" in value:
            return query.filter(column.between(value["min"], value["max"]))
        elif isinstance(value, list):
            return query.filter(column.in_(value))
        else:
            return query.filter(column == value)

    @classmethod
    def apply_relationship_filters(cls, query, relationships):
        """
        Apply relationship filters to the query.
        """
        for rel_key, rel_filter in relationships.items():
            relationship_class = cls.__mapper__.relationships[rel_key].mapper.class_
            alias = aliased(relationship_class)
            for key, value in rel_filter.items():
                query = query.join(alias).filter(getattr(alias, key) == value)
        return query

    @classmethod
    def apply_ordering(cls, query, order_by):
        """
        Apply ordering to the query.
        """
        if isinstance(order_by, list):
            for order_condition in order_by:
                query = query.order_by(order_condition)
        else:
            query = query.order_by(order_by)
        return query

    @classmethod
    def filter(
        cls,
        db_session: Session,
        filters: dict,
        relationships: dict = None,
        order_by=None,
        limit=None,
        offset=None,
    ) -> list:
        """
        Perform advanced filtering with support for relationships, complex conditions,
        and SQL functions. This method is optimized for complex queries and efficient
        database access.
        """
        query = db_session.query(cls)
        # Apply filters
        conditions = [
            cls.apply_filter_conditions(query, attribute, value)
            for attribute, value in filters.items()
        ]
        query = query.filter(*conditions)
        # Handle relationships
        query = cls.apply_relationship_filters(query, relationships or {})
        # Apply ordering
        query = cls.apply_ordering(query, order_by or [])
        # Apply pagination
        if offset is not None and limit is not None:
            query = query.offset(offset).limit(limit)
        return query

    @classmethod
    def dynamic_sort(
        cls,
        db_session: Session,
        sort_criteria: list[tuple[str, str]],
        filters: dict = None,
    ) -> list:
        query = db_session.query(cls)
        if filters:
            query = query.filter_by(**filters)
        for sort_field, direction in sort_criteria:
            query = query.order_by(
                cls.__table__.c.get(sort_field).desc()
                if direction.lower() == "desc"
                else cls.__table__.c.get(sort_field)
            )
        return query

    @classmethod
    def paginate(
        cls,
        db_session: Session,
        page_number: int,
        page_size: int,
        sort_criteria: list[tuple[str, str]] = None,
        filters: dict = None,
    ) -> list:
        query = db_session.query(cls)
        if filters:
            query = query.filter_by(**filters)
        if sort_criteria:
            for sort_field, direction in sort_criteria:
                query = query.order_by(
                    cls.__table__.c.get(sort_field).desc()
                    if direction.lower() == "desc"
                    else cls.__table__.c.get(sort_field)
                )
        offset = (page_number - 1) * page_size
        query = query.offset(offset).limit(page_size)
        return query

    @abstractmethod
    def validate(self):  # Method should be created later and updated
        # Child classes must implement their specific validation logic
        pass
