from typing import Optional

from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.models.users import UserAddresses
from app.repositories.common import BulkActionsMixin, CachingMixin, SearchMixin
from app.schemas.users import (
    AddressType,
    UserAddressCreate,
    UserAddressRead,
    UserAddressUpdate,
)


class UserAddressRepository(CachingMixin, BulkActionsMixin, SearchMixin):
    """Repository for managing user addresses."""

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.model = UserAddresses  # Define the model for this repository

    def get_address_by_id(self, address_id: UUID) -> Optional[UserAddressRead]:
        """Retrieves an address by its ID."""

        address = self.db_session.execute(
            select(UserAddresses).where(UserAddresses.id == address_id)
        )
        address = address.scalars().first()
        return UserAddressRead.model_validate(address) if address else None

    def get_addresses_by_user_id(self, user_id: UUID) -> list[UserAddressRead]:
        """Retrieves all addresses for a given user."""

        addresses = self.db_session.execute(
            select(UserAddresses).where(UserAddresses.user_id == user_id)
        )
        addresses = addresses.scalars().all()
        return [UserAddressRead.model_validate(address) for address in addresses]

    def get_address_by_user_id_and_type(
        self, user_id: UUID, address_type: AddressType
    ) -> Optional[UserAddressRead]:
        """Retrieves an address by user ID and type."""

        address = self.db_session.execute(
            select(UserAddresses).where(
                and_(
                    UserAddresses.user_id == user_id,
                    UserAddresses.address_type == address_type,
                )
            )
        )
        address = address.scalars().first()
        return UserAddressRead.model_validate(address) if address else None

    def add_user_address(
        self, user_id: UUID, address_data: UserAddressCreate
    ) -> UserAddressRead:
        """Adds a new address to the user."""

        # Check for duplicates
        existing_address = self.get_address_by_user_id_and_type(
            user_id, address_data.address_type
        )
        if existing_address:
            raise HTTPException(
                status_code=400,
                detail="Address of this type already exists for the user",
            )

        new_address = UserAddresses(**address_data.model_dump(), user_id=user_id)
        self.db_session.add(new_address)
        self.db_session.commit()
        self.db_session.refresh(new_address)
        return UserAddressRead.model_validate(new_address)

    def update_user_address(
        self, address_id: UUID, address_data: UserAddressUpdate
    ) -> UserAddressRead:
        """Updates an existing user address."""

        address = self.get_address_by_id(address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")

        address.update(session, **address_data.model_dump(exclude_unset=True))

        self.db_session.commit()
        self.db_session.refresh(address)
        return UserAddressRead.model_validate(address)

    def delete_user_address(self, address_id: UUID) -> None:
        """Deletes a user address."""

        address = self.get_address_by_id(address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")

        self.db_session.delete(address)
        self.db_session.commit()
