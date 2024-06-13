from typing import Any, Optional

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import RelationshipProperty, Session, aliased


class BaseMixin:
    """
    Base mixin providing common attributes and methods for all models.
    """

    model = None

    def get_by_id(self, db_session: Session, _id: UUID):
        """
        Retrieve a model instance by its ID. Handles session execution.
        """
        self.logger.debug("Fetching by ID: %s", _id)
        with db_session as session:
            result = session.execute(
                select(self.model).where(
                    self.model.id == _id, self.model.deleted_at.is_(None)
                )
            )
            return result.scalars().first()

    def get_all(self, db_session: Session):
        """
        Retrieve all non-deleted instances of the model.
        """
        with db_session as session:
            result = session.execute(
                select(self.model).where(self.model.deleted_at.is_(None))
            )
            return result.scalars().all()

    def get_by_ids(self, db_session: Session, ids: list[UUID]):
        """
        Retrieve multiple model instances by their IDs.
        """
        with db_session as session:
            result = session.execute(select(self.model).where(self.model.id.in_(ids)))
            return result.scalars().all()

    def _apply_filters(
        self, db_session: Session, query: select, filters: Optional[dict[str, Any]]
    ) -> select:
        """
        Applies filter conditions to the query.
        """
        with db_session.begin():
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

    def _apply_relationship_filters(
        self,
        db_session: Session,
        query: select,
        relationships: Optional[dict[str, tuple[str, Any]]],
    ) -> select:
        """
        Applies filters based on related model attributes.
        """
        with db_session.begin():
            if relationships:
                for rel_attr, (rel_field, rel_filter) in relationships.items():
                    relationship: RelationshipProperty = getattr(self.model, rel_attr)
                    related_self = relationship.mapper.class_
                    rel_alias = aliased(related_self)
                    query = query.join(rel_alias, relationship).filter(
                        getattr(rel_alias, rel_field) == rel_filter
                    )
            return query

    def _apply_ordering(
        self,
        db_session: Session,
        query: select,
        order_by: Optional[list[tuple[str, str]]],
    ) -> select:
        """
        Applies ordering to the query.
        """
        with db_session.begin():
            if order_by:
                for field, direction in order_by:
                    column = self.model.__table__.c.get(field)
                    if direction.lower() == "desc":
                        query = query.order_by(column.desc())
                    else:
                        query = query.order_by(column)
            return query

    def filter(
        self,
        db_session: Session,
        filters: Optional[dict[str, Any]] = None,
        relationships: Optional[dict[str, tuple[str, Any]]] = None,
        order_by: Optional[list[tuple[str, str]]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list:
        """
        Perform advanced filtering, ordering, and pagination asynchronously.

        Args:
            db_session (Session): The database session.
            filters (Optional[Dict[str, Any]]): Filtering criteria for the main model.
            relationships (Optional[Dict[str, Tuple[str, Any]]]): Filtering based on related models.
            order_by (Optional[List[Tuple[str, str]]]): Ordering criteria.
            limit (Optional[int]): Maximum number of results.
            offset (Optional[int]): Result offset for pagination.

        Returns:
            List: A list of filtered and ordered model instances.
        """
        with db_session.begin():
            query = select(self.model)
            query = self._apply_filters(query, filters)
            query = self._apply_relationship_filters(query, relationships)
            query = self._apply_ordering(query, order_by)

            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)

            with db_session as session:
                result = session.execute(query)
                return result.scalars().all()

    def paginate(
        self,
        db_session: Session,
        page: int,
        page_size: int,
        filters: Optional[dict[str, any]] = None,
        relationships: Optional[dict[str, tuple[str, Any]]] = None,
        order_by: Optional[list[tuple[str, str]]] = None,
    ) -> list:
        """
        Retrieve paginated model instances asynchronously.

        Args:
            db_session (Session): The database session.
            page (int): The page number to retrieve (1-based indexing).
            page_size (int): Number of items per page.
            filters (Optional[Dict[str, Any]]): Filtering criteria.
            relationships (Optional[Dict[str, Tuple[str, Any]]]): Filtering based on related models.
            order_by (Optional[List[Tuple[str, str]]]): Ordering criteria.

        Returns:
            List: A list of model instances for the specified page.
        """
        offset = (page - 1) * page_size
        with db_session.begin():
            return self.filter(
                db_session,
                filters=filters,
                relationships=relationships,
                order_by=order_by,
                limit=page_size,
                offset=offset,
            )

    def create(self, db_session: Session, **kwargs):
        """
        Create and save a new instance of the model.
        """
        with db_session.begin():
            new_instance = self.model(**kwargs)
            db_session.add(new_instance)
            db_session.commit()
            db_session.refresh(new_instance)
            return self.model

    def update(self, db_session: Session, **kwargs):
        """
        Update an existing model instance.
        """
        with db_session.begin():
            for key, value in kwargs.items():
                setattr(self.model, key, value)
            db_session.commit()
            db_session.refresh(self.model)
            return self.model

    def soft_delete(self, db_session: Session):
        """
        Mark the model instance as deleted (soft delete).
        """
        with db_session.begin():
            self.model.is_active = False
            self.model.deleted_at = func.now()
            db_session.commit()
            db_session.refresh(self.model)
            return self.model

    def delete(self, db_session: Session):
        """
        Permanently delete the model instance (hard delete).
        """
        with db_session.begin():
            db_session.delete(self.model)
            db_session.commit()
