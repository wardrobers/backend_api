from typing import Any, Optional

from sqlalchemy import and_, delete, func, insert, select, update
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta


class BulkActionsMixin(metaclass=DeclarativeMeta):
    """
    Mixin for performing bulk operations on database models, featuring:

    - Asynchronous operations for enhanced concurrency.
    - Optimized bulk inserts and updates.
    - Bulk soft and hard deletes.
    - Bulk upsert operation (insert or update).
    - Type hints for improved clarity.
    """

    @classmethod
    async def bulk_create(cls, db_session: AsyncSession, items: list[dict[str, Any]]):
        """
        Perform a bulk insert operation asynchronously.

        Args:
            db_session (AsyncSession): The asynchronous database session.
            items (List[Dict[str, Any]]): A list of dictionaries representing the data to insert.
        """
        async with db_session as session:
            await session.execute(insert(cls), items)
            await session.commit()

    @classmethod
    async def bulk_update(cls, db_session: AsyncSession, items: list[dict[str, Any]]):
        """
        Perform a bulk update operation asynchronously.

        Args:
            db_session (AsyncSession): The asynchronous database session.
            items (List[Dict[str, Any]]): A list of dictionaries representing the data to update.
                Each dictionary must contain the 'id' of the record to update.
        """
        async with db_session as session:
            for item in items:
                await session.execute(
                    update(cls)
                    .where(cls.id == item["id"])
                    .values(**{k: v for k, v in item.items() if k != "id"})
                )
            await session.commit()

    @classmethod
    async def bulk_delete(cls, db_session: AsyncSession, ids: list[UUID]):
        """
        Perform a bulk hard delete operation asynchronously.

        Args:
            db_session (AsyncSession): The asynchronous database session.
            ids (List[UUID]): A list of IDs to delete.
        """
        async with db_session as session:
            await session.execute(delete(cls).where(cls.id.in_(ids)))
            await session.commit()

    @classmethod
    async def bulk_soft_delete(cls, db_session: AsyncSession, ids: list[UUID]):
        """
        Perform a bulk soft delete operation asynchronously.

        Args:
            db_session (AsyncSession): The asynchronous database session.
            ids (List[UUID]): A list of IDs to soft delete.
        """
        async with db_session as session:
            await session.execute(
                update(cls).where(cls.id.in_(ids)).values(deleted_at=func.now())
            )
            await session.commit()

    @classmethod
    async def bulk_upsert(
        cls,
        db_session: AsyncSession,
        items: list[dict[str, Any]],
        unique_constraint: Optional[tuple[str, ...]] = None,
    ):
        """
        Perform a bulk upsert operation (insert or update) asynchronously.

        Args:
            db_session (AsyncSession): The asynchronous database session.
            items (List[Dict[str, Any]]): A list of dictionaries representing the data to upsert.
            unique_constraint (Optional[Tuple[str, ...]]): The unique constraint
                to use for determining whether to insert or update. If None, the primary key is used.
        """
        async with db_session as session:
            for item in items:
                if unique_constraint:
                    # Use unique constraint for checking existing records
                    filter_condition = and_(
                        *[getattr(cls, col) == item[col] for col in unique_constraint]
                    )
                else:
                    # Use primary key for checking existing records
                    filter_condition = cls.id == item.get("id")

                existing_record = await session.execute(
                    select(cls).where(filter_condition)
                )
                existing_record = existing_record.scalars().first()

                if existing_record:
                    # Update the existing record
                    if unique_constraint:
                        await session.execute(
                            update(cls)
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
                        await session.execute(
                            update(cls)
                            .where(cls.id == item["id"])
                            .values(**{k: v for k, v in item.items() if k != "id"})
                        )
                else:
                    # Insert a new record
                    await session.execute(insert(cls).values(**item))
            await session.commit()
