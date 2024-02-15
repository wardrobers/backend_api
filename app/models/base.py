from typing import TypeVar, Type, List, Optional, Any, Dict, Tuple
from sqlalchemy.orm import Session, declared_attr, object_session
from sqlalchemy import Column, DateTime, func, Boolean, String, Integer, or_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from fastapi import HTTPExceptio

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
    def find_all(cls: Type[T], db_session: Session) -> List[T]:
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
    def deactivate_all(cls: Type[T], db_session: Session, ids: List[UUID]) -> None:
        db_session.query(cls).filter(cls.id.in_(ids)).update(
            {cls.is_active: False}, synchronize_session="fetch"
        )
        db_session.commit()

    @classmethod
    def bulk_create(cls: Type[T], db_session: Session, items: List[Dict]) -> List[T]:
        instances = [cls(**item) for item in items]
        db_session.bulk_save_objects(instances)
        db_session.commit()
        return instances

    @classmethod
    def find_available_items(cls: Type[T], db_session: Session) -> List[T]:
        """Find items that are available for rental."""
        return db_session.query(cls).filter_by(quantity > 0, is_active=True).all()

    @classmethod
    def find_by_size_and_color(
        cls: Type[T], db_session: Session, size: str, color: str
    ) -> List[T]:
        """Find items by size and color."""
        return (
            db_session.query(cls)
            .filter_by(size=size, color=color, is_active=True)
            .all()
        )

    def rent_out(self, db_session: Session, quantity: int = 1) -> None:
        """Rent out a specified quantity of this clothing item."""
        if self.quantity < quantity:
            raise HTTPException(status_code=400, detail="Not enough items in stock")
        self.quantity -= quantity
        db_session.commit()

    def return_item(self, db_session: Session, quantity: int = 1) -> None:
        """Return a specified quantity of this clothing item."""
        self.quantity += quantity
        db_session.commit()

    @classmethod
    def restock(
        cls: Type[T], db_session: Session, restock_data: Dict[UUID, int]
    ) -> None:
        """Bulk restock items based on a dictionary of item IDs and quantities."""
        for item_id, additional_quantity in restock_data.items():
            item = cls.find_by_id(db_session, item_id)
            if item:
                item.quantity += additional_quantity
        db_session.commit()

    @classmethod
    def search(
        cls: Type[T],
        db_session: Session,
        filters: Dict[str, Union[str, List[str], Dict[str, Any]]],
    ) -> List[T]:
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
    ) -> List[T]:
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
        cls: Type[T], db_session: Session, ids: List[UUID]
    ) -> List[T]:
        """
        Get multiple records by a list of IDs.
        """
        return (
            db_session.query(cls).filter(cls.id.in_(ids), cls.is_active == True).all()
        )

    @classmethod
    def filter_by_attributes(
        cls: Type[T], db_session: Session, **attributes
    ) -> List[T]:
        """Filter items based on attribute values."""
        return db_session.query(cls).filter_by(**attributes, is_active=True).all()

    @classmethod
    def get_sorted_and_filtered(
        cls: Type[T],
        db_session: Session,
        sort_fields: List[Tuple[str, str]],
        filter_criteria: Dict[str, Any],
    ) -> List[T]:
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
        cls: Type[T], db_session: Session, updates: Dict[UUID, Dict]
    ) -> None:
        """Bulk update items based on a dictionary of item IDs and their update values."""
        for item_id, update_values in updates.items():
            item = cls.find_by_id(db_session, item_id)
            if item:
                for key, value in update_values.items():
                    setattr(item, key, value)
        db_session.commit()

    @classmethod
    def get_active_count(cls: Type[T], db_session: Session) -> int:
        """Get the count of active items."""
        return db_session.query(cls).filter_by(is_active=True).count()

    @classmethod
    def find_with_filters(cls: Type[T], db_session: Session, **filters) -> List[T]:
        """
        Generic method to find records with given filters.
        """
        query = db_session.query(cls).filter_by(**filters)
        return query.all()

    @classmethod
    def get_sorted_by_field(
        cls: Type[T], db_session: Session, sort_field: str, descending: bool = False
    ) -> List[T]:
        """
        Get all records sorted by a specific field.
        """
        sort_by = (
            getattr(cls, sort_field).desc() if descending else getattr(cls, sort_field)
        )
        return db_session.query(cls).order_by(sort_by).all()

    @classmethod
    def find_subscriptions_by_user(
        cls: Type[T], db_session: Session, user_id: UUID
    ) -> List[T]:
        """
        Find all active subscriptions for a given user.
        """
        return db_session.query(cls).filter_by(user_id=user_id, is_active=True).all()

    @classmethod
    def find_photos_for_item(
        cls: Type[T], db_session: Session, item_id: UUID
    ) -> List[T]:
        """
        Find all photos related to a specific item.
        """
        return db_session.query(cls).filter_by(item_id=item_id, is_active=True).all()

    @classmethod
    def get_active_users(cls: Type[T], db_session: Session) -> int:
        """
        Get the count of active users on the platform.
        """
        return db_session.query(cls).filter_by(is_active=True, type="user").count()

    @classmethod
    def get_user_activity(
        cls: Type[T], db_session: Session, user_id: UUID
    ) -> Optional[T]:
        """
        Retrieve the activity log of a specific user.
        """
        return db_session.query(cls).filter_by(user_id=user_id, is_active=True).first()

    @classmethod
    def update_user_activity(
        cls: Type[T], db_session: Session, user_id: UUID, **activity_updates
    ) -> Optional[T]:
        """
        Update the activity log of a specific user.
        """
        user_activity = cls.get_user_activity(db_session, user_id)
        if user_activity:
            for key, value in activity_updates.items():
                setattr(user_activity, key, value)
            db_session.commit()
            db_session.refresh(user_activity)
            return user_activity
        return None

    @classmethod
    def get_inventory_status(
        cls: Type[T], db_session: Session
    ) -> List[Tuple[UUID, int]]:
        """
        Get the current inventory status, including item quantities.
        """
        return db_session.query(cls.id, cls.quantity).filter_by(is_active=True).all()

    @classmethod
    def update_inventory(
        cls: Type[T], db_session: Session, item_id: UUID, quantity_change: int
    ) -> Optional[T]:
        """
        Update the inventory by adding or subtracting quantities of items.
        """
        item = cls.find_by_id(db_session, item_id)
        if item:
            item.quantity = max(
                0, item.quantity + quantity_change
            )  # Avoid negative quantities
            db_session.commit()
            db_session.refresh(item)
            return item
        return None

    @classmethod
    def get_all_active_subscriptions(cls: Type[T], db_session: Session) -> List[T]:
        """
        Get all active subscriptions on the platform.
        """
        return (
            db_session.query(cls).filter_by(is_active=True, type="subscription").all()
        )

    @classmethod
    def get_subscription_details(
        cls: Type[T], db_session: Session, subscription_id: UUID
    ) -> Optional[T]:
        """
        Get the details of a specific subscription.
        """
        return (
            db_session.query(cls).filter_by(id=subscription_id, is_active=True).first()
        )

    @classmethod
    def get_user_photos(cls: Type[T], db_session: Session, user_id: UUID) -> List[T]:
        """
        Get all photos associated with a user's profile.
        """
        return db_session.query(cls).filter_by(user_id=user_id, is_active=True).all()

    @classmethod
    def add_user_subscription(
        cls: Type[T], db_session: Session, user_id: UUID, subscription_data: Dict
    ) -> T:
        """
        Add a new subscription for a user.
        """
        subscription = cls.create(db_session, user_id=user_id, **subscription_data)
        return subscription

    @classmethod
    def cancel_user_subscription(
        cls: Type[T], db_session: Session, subscription_id: UUID
    ) -> Optional[T]:
        """
        Cancel a user's subscription.
        """
        subscription = cls.get_subscription_details(db_session, subscription_id)
        if subscription:
            subscription.is_active = False
            subscription.deleted_at = func.now()
            db_session.commit()
            return subscription
        return None
