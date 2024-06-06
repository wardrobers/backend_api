from typing import Any, Optional
import logging

from sqlalchemy import func, select, update
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import RelationshipProperty, aliased


class BaseMixin:
    """
    Base mixin providing common attributes and methods for all models.
    """

    logger = logging.getLogger(__name__)
    model = None

    async def get_by_id(self, db_session: AsyncSession, _id: UUID):
        """
        Retrieve a model instance by its ID. Handles async session execution.
        """
        self.logger.debug("Fetching by ID: %s", _id)
        async with db_session as session:
            result = await session.execute(
                select(self.model).where(self.model.id == _id, self.model.deleted_at.is_(None))
            )
            return result.scalars().first()

    async def get_all(self, db_session: AsyncSession):
        """
        Retrieve all non-deleted instances of the model.
        """
        async with db_session as session:
            result = await session.execute(
                select(self.model).where(self.model.deleted_at.is_(None))
            )
            return result.scalars().all()

    async def get_by_ids(self, db_session: AsyncSession, ids: list[UUID]):
        """
        Retrieve multiple model instances by their IDs.
        """
        async with db_session as session:
            result = await session.execute(select(self.model).where(self.model.id.in_(ids)))
            return result.scalars().all()

    async def _apply_filters(
        self, db_session: AsyncSession, query: select, filters: Optional[dict[str, Any]]
    ) -> select:
        """
        Applies filter conditions to the query.
        """
        async with db_session.begin():
            if filters:
                for attribute, value in filters.items():
                    column = self.model.__table__.c.get(attribute)
                    if isinstance(value, dict) and "min" in value and "max" in value:
                        query = query.where(column.between(value["min"], value["max"]))
                    elif isinstance(value, list):
                        query = query.where(column.in_(value))
                    else:
                        query = query.where(column == value)
            return query

    async def _apply_relationship_filters(
        self, db_session: AsyncSession, query: select, relationships: Optional[dict[str, tuple[str, Any]]]
    ) -> select:
        """
        Applies filters based on related model attributes.
        """
        async with db_session.begin():
            if relationships:
                for rel_attr, (rel_field, rel_filter) in relationships.items():
                    relationship: RelationshipProperty = getattr(self.model, rel_attr)
                    related_self = relationship.mapper.class_
                    rel_alias = aliased(related_self)
                    query = query.join(rel_alias, relationship).filter(
                        getattr(rel_alias, rel_field) == rel_filter
                    )
            return query

    async def _apply_ordering(
        self, db_session: AsyncSession, query: select, order_by: Optional[list[tuple[str, str]]]
    ) -> select:
        """
        Applies ordering to the query.
        """
        async with db_session.begin():
            if order_by:
                for field, direction in order_by:
                    column = self.model.__table__.c.get(field)
                    if direction.lower() == "desc":
                        query = query.order_by(column.desc())
                    else:
                        query = query.order_by(column)
            return query

    async def filter(
        self,
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
        async with db_session.begin():
            query = select(self.model)
            query = await self._apply_filters(query, filters)
            query = await self._apply_relationship_filters(query, relationships)
            query = await self._apply_ordering(query, order_by)

            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)

            async with db_session as session:
                result = await session.execute(query)
                return result.scalars().all()

    async def paginate(
        self,
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
        async with db_session.begin():
            return await self.filter(
                db_session,
                filters=filters,
                relationships=relationships,
                order_by=order_by,
                limit=page_size,
                offset=offset,
            )

    async def create(self, db_session: AsyncSession, **kwargs):
        """
        Create and save a new instance of the model.
        """
        async with db_session.begin():
            new_instance = self.model(**kwargs)
            db_session.add(new_instance)
            await db_session.commit()
            await db_session.refresh(new_instance)
            return self.model

    async def update(self, db_session: AsyncSession, **kwargs):
        """
        Update an existing model instance.
        """
        for key, value in kwargs.items():
            setattr(self.model, key, value)
        await db_session.commit()
        await db_session.refresh(self.model)
        return self.model

    async def soft_delete(self, db_session: AsyncSession):
        """
        Mark the model instance as deleted (soft delete).
        """
        async with db_session.begin():
            self.model.is_active = False
            self.model.deleted_at = func.now()
            await db_session.commit()
            await db_session.refresh(self.model)
            return self.model

    async def delete(self, db_session: AsyncSession):
        """
        Permanently delete the model instance (hard delete).
        """
        async with db_session.begin():
            await db_session.delete(self.model)
            await db_session.commit()