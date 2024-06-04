from typing import Any, Optional

from sqlalchemy import Column, DateTime, func, select, update
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import RelationshipProperty, aliased, declared_attr, mapped_column


class ModelBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=ModelBase)


class BaseMixin:
    """
    Base mixin providing common attributes and methods for all models.

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

    @classmethod
    async def get_by_id(cls, db_session: AsyncSession, _id: UUID):
        """
        Retrieve a model instance by its ID. Handles async session execution.
        """
        async with db_session as session:
            result = await session.execute(
                select(cls).where(cls.id == _id, cls.deleted_at.is_(None))
            )
            return result.scalars().first()

    @classmethod
    async def get_all(cls, db_session: AsyncSession):
        """
        Retrieve all non-deleted instances of the model.
        """
        async with db_session as session:
            result = await session.execute(select(cls).where(cls.deleted_at.is_(None)))
            return result.scalars().all()

    @classmethod
    async def get_by_ids(cls, db_session: AsyncSession, ids: list[UUID]):
        """
        Retrieve multiple model instances by their IDs.
        """
        async with db_session as session:
            result = await session.execute(select(cls).where(cls.id.in_(ids)))
            return result.scalars().all()

    async def create(self, db_session: AsyncSession, **kwargs):
        """
        Create and save a new instance of the model.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        db_session.add(self)
        await db_session.commit()
        await db_session.refresh(self)
        return self

    async def update(self, db_session: AsyncSession, **kwargs):
        """
        Update an existing model instance.
        """
        async with db_session as session:
            await session.execute(
                update(self.__class__)
                .where(self.__class__.id == self.id)
                .values(**kwargs)
            )
            await session.commit()
            await session.refresh(self)
        return self

    async def soft_delete(self, db_session: AsyncSession):
        """
        Mark the model instance as deleted (soft delete).
        """
        async with db_session as session:
            setattr(self, "is_active", False)
            self.deleted_at = func.now()
            await session.commit()
            await session.refresh(self)
        return self

    async def delete(self, db_session: AsyncSession):
        """
        Permanently delete the model instance (hard delete).
        """
        async with db_session as session:
            self.soft_delete(session)
            await session.delete(self)
            await session.commit()

    @classmethod
    async def _apply_filters(
        cls, query: select, filters: Optional[dict[str, Any]]
    ) -> select:
        """
        Applies filter conditions to the query.
        """
        if filters:
            for attribute, value in filters.items():
                column = cls.__table__.c.get(attribute)
                if isinstance(value, dict) and "min" in value and "max" in value:
                    query = query.where(column.between(value["min"], value["max"]))
                elif isinstance(value, list):
                    query = query.where(column.in_(value))
                else:
                    query = query.where(column == value)
        return query

    @classmethod
    async def _apply_relationship_filters(
        cls, query: select, relationships: Optional[dict[str, tuple[str, Any]]]
    ) -> select:
        """
        Applies filters based on related model attributes.
        """
        if relationships:
            for rel_attr, (rel_field, rel_filter) in relationships.items():
                relationship: RelationshipProperty = getattr(cls, rel_attr)
                related_cls = relationship.mapper.class_
                rel_alias = aliased(related_cls)
                query = query.join(rel_alias, relationship).filter(
                    getattr(rel_alias, rel_field) == rel_filter
                )
        return query

    @classmethod
    async def _apply_ordering(
        cls, query: select, order_by: Optional[list[tuple[str, str]]]
    ) -> select:
        """
        Applies ordering to the query.
        """
        if order_by:
            for field, direction in order_by:
                column = cls.__table__.c.get(field)
                if direction.lower() == "desc":
                    query = query.order_by(column.desc())
                else:
                    query = query.order_by(column)
        return query

    @classmethod
    async def filter(
        cls,
        db_session: AsyncSession,
        filters: Optional[dict[str, Any]] = None,
        relationships: Optional[dict[str, tuple[str, Any]]] = None,
        order_by: Optional[list[tuple[str, str]]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list:
        """
        Perform advanced filtering, ordering, and pagination asynchronously.

        Args:
            db_session (AsyncSession): The async database session.
            filters (Optional[Dict[str, Any]]): Filtering criteria for the main model.
            relationships (Optional[Dict[str, Tuple[str, Any]]]): Filtering based on related models.
            order_by (Optional[List[Tuple[str, str]]]): Ordering criteria.
            limit (Optional[int]): Maximum number of results.
            offset (Optional[int]): Result offset for pagination.

        Returns:
            List: A list of filtered and ordered model instances.
        """
        query = select(cls)
        query = await cls._apply_filters(query, filters)
        query = await cls._apply_relationship_filters(query, relationships)
        query = await cls._apply_ordering(query, order_by)

        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        async with db_session as session:
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def paginate(
        cls,
        db_session: AsyncSession,
        page: int,
        page_size: int,
        filters: Optional[dict[str, any]] = None,
        relationships: Optional[dict[str, tuple[str, Any]]] = None,
        order_by: Optional[list[tuple[str, str]]] = None,
    ) -> list:
        """
        Retrieve paginated model instances asynchronously.

        Args:
            db_session (AsyncSession): The async database session.
            page (int): The page number to retrieve (1-based indexing).
            page_size (int): Number of items per page.
            filters (Optional[Dict[str, Any]]): Filtering criteria.
            relationships (Optional[Dict[str, Tuple[str, Any]]]): Filtering based on related models.
            order_by (Optional[List[Tuple[str, str]]]): Ordering criteria.

        Returns:
            List: A list of model instances for the specified page.
        """
        offset = (page - 1) * page_size
        return await cls.filter(
            db_session,
            filters=filters,
            relationships=relationships,
            order_by=order_by,
            limit=page_size,
            offset=offset,
        )
