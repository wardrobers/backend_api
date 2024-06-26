from typing import Any, Optional

from fastapi import HTTPException
from pydantic import BaseModel
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
        result = db_session.execute(
            select(self.model).where(
                self.model.id == _id, self.model.deleted_at.is_(None)
            )
        )
        return result.scalars().first()

    def get_all(self, db_session: Session):
        """
        Retrieve all non-deleted instances of the model.
        """
        result = db_session.execute(
            select(self.model).where(self.model.deleted_at.is_(None))
        )
        return result.scalars().all()

    def get_by_ids(self, db_session: Session, ids: list[UUID]):
        """
        Retrieve multiple model instances by their IDs.
        """
        result = db_session.execute(select(self.model).where(self.model.id.in_(ids)))
        return result.scalars().all()

    def get_by_field(
        self, db_session: Session, field_name: str, field_value: Any
    ) -> Optional[Any]:
        """
        Retrieve a model instance by a specific field.

        Args:
            db_session (Session): The database session.
            field_name (str): The name of the field to filter by.
            field_value (Any): The value of the field to filter by.

        Returns:
            Optional[Any]: The model instance if found, otherwise None.
        """
        return (
            db_session.query(self.model)
            .filter(getattr(self.model, field_name) == field_value)
            .first()
        )

    def _apply_filters(
        self, query: select, filters: Optional[dict[str, Any]]
    ) -> select:
        """
        Applies filter conditions to the query.
        """
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
        query: select,
        relationships: Optional[dict[str, tuple[str, Any]]],
    ) -> select:
        """
        Applies filters based on related model attributes.
        """
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
        query: select,
        order_by: Optional[list[tuple[str, str]]],
    ) -> select:
        """
        Applies ordering to the query.
        """
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
        query = select(self.model)
        query = self._apply_filters(query, filters)
        query = self._apply_relationship_filters(query, relationships)
        query = self._apply_ordering(query, order_by)

        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        result = db_session.execute(query).unique()
        return result.scalars().all()

    def paginate(
        self,
        db_session: Session,
        page: int,
        page_size: int,
        filters: Optional[dict[str, any]] = None,
        relationships: Optional[dict[str, tuple[str, Any]]] = None,
        order_by: Optional[list[tuple[str, str]]] = None,
    ) -> tuple[list, int]:
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
        items = self.filter(
            db_session,
            filters=filters,
            relationships=relationships,
            order_by=order_by,
            limit=page_size,
            offset=offset,
        )
        total_count = db_session.query(func.count(self.model.id)).scalar()
        return items, total_count

    def create(self, db_session: Session, create_data: BaseModel):
        """
        Create and save a new instance of the model from a Pydantic model.
        """
        new_instance = self.model(**create_data.model_dump()) 
        db_session.add(new_instance)
        db_session.commit()
        db_session.refresh(new_instance)
        return new_instance

    def update(self, db_session: Session, id: UUID, update_data: BaseModel) -> Any:
        """
        Update an existing model instance using a Pydantic model.

        Args:
            db_session (Session): The database session.
            id (UUID): The ID of the instance to update.
            update_data (BaseModel): The Pydantic model containing the update data.

        Returns:
            Any: The updated model instance.
        """
        instance = self.get_by_id(db_session, id)
        if not instance:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found"
            )

        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(instance, key, value)

        db_session.commit()
        db_session.refresh(instance)
        return instance

    def soft_delete(self, db_session: Session, _id: UUID) -> Any:
        """
        Mark the model instance as deleted (soft delete).
        """
        instance = self.get_by_id(db_session, _id)
        if not instance:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found"
            )

        instance.is_active = False
        instance.deleted_at = func.now()
        db_session.commit()
        db_session.refresh(instance)
        return instance

    def delete(self, db_session: Session, _id: UUID) -> None:
        """
        Permanently delete a model instance.

        Args:
            db_session (Session): The database session.
            id (UUID): The ID of the instance to delete.
        """
        instance = self.get_by_id(db_session, _id)
        if not instance:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found"
            )

        db_session.delete(instance)
        db_session.commit()
