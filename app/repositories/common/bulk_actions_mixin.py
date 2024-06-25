from typing import Any, Optional

from sqlalchemy import and_, delete, func, insert, select, update
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session


class BulkActionsMixin:
    """
    Mixin for performing bulk operations on database models, featuring:

    - Optimized bulk inserts and updates.
    - Bulk soft and hard deletes.
    - Bulk upsert operation (insert or update).
    - Type hints for improved clarity.
    """

    model = None

    def bulk_create(self, db_session: Session, items: list[dict[str, Any]]):
        """
        Perform a bulk insert operation asynchronously.

        Args:
            db_session (Session): The  database session.
            items (List[Dict[str, Any]]): A list of dictionaries representing the data to insert.
        """
        db_session.execute(insert(self.model), items)
        db_session.commit()

    def bulk_update(self, db_session: Session, items: list[dict[str, Any]]):
        """
        Perform a bulk update operation asynchronously.

        Args:
            db_session (Session): The  database session.
            items (List[Dict[str, Any]]): A list of dictionaries representing the data to update.
                Each dictionary must contain the 'id' of the record to update.
        """
        for item in items:
            db_session.execute(
                update(self.model)
                .where(self.model.id == item["id"])
                .values(**{k: v for k, v in item.items() if k != "id"})
            )
        db_session.commit()

    def bulk_delete(self, db_session: Session, ids: list[UUID]):
        """
        Perform a bulk hard delete operation asynchronously.

        Args:
            db_session (Session): The  database session.
            ids (List[UUID]): A list of IDs to delete.
        """
        db_session.execute(delete(self.model).where(self.model.id.in_(ids)))
        db_session.commit()

    def bulk_soft_delete(self, db_session: Session, ids: list[UUID]):
        """
        Perform a bulk soft delete operation asynchronously.

        Args:
            db_session (Session): The  database session.
            ids (List[UUID]): A list of IDs to soft delete.
        """
        db_session.execute(
            update(self.model)
            .where(self.model.id.in_(ids))
            .values(deleted_at=func.now())
        )
        db_session.commit()

    def bulk_upsert(
        self,
        db_session: Session,
        items: list[dict[str, Any]],
        unique_constraint: Optional[tuple[str, ...]] = None,
    ):
        """
        Perform a bulk upsert operation (insert or update) asynchronously.

        Args:
            db_session (Session): The  database session.
            items (List[Dict[str, Any]]): A list of dictionaries representing the data to upsert.
            unique_constraint (Optional[Tuple[str, ...]]): The unique constraint
                to use for determining whether to insert or update. If None, the primary key is used.
        """
        for item in items:
            if unique_constraint:
                # Use unique constraint for checking existing records
                filter_condition = and_(
                    *[
                        getattr(self.model, col) == item[col]
                        for col in unique_constraint
                    ]
                )
            else:
                # Use primary key for checking existing records
                filter_condition = self.model.id == item.get("id")

            existing_record = db_session.execute(
                select(self.model).where(filter_condition)
            )
            existing_record = existing_record.scalars().first()

            if existing_record:
                # Update the existing record
                if unique_constraint:
                    db_session.execute(
                        update(self.model)
                        .where(filter_condition)
                        .values(
                            **{
                                k: v
                                for k, v in item.items()
                                if k not in unique_constraint
                            }
                        )
                    )
                else:
                    db_session.execute(
                        update(self.model)
                        .where(self.model.id == item["id"])
                        .values(**{k: v for k, v in item.items() if k != "id"})
                    )
            else:
                # Insert a new record
                db_session.execute(insert(self.model).values(**item))
        db_session.commit()
