from typing import Optional

from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import UserAddresses
from app.repositories.common import (
    BaseMixin,
    BulkActionsMixin,
    CachingMixin,
    SearchMixin,
)
from app.schemas.users import (
    AddressType,
    UserAddressCreate,
    UserAddressRead,
    UserAddressUpdate,
)


class UserAddressRepository(BaseMixin, CachingMixin, BulkActionsMixin, SearchMixin):
    """Repository for managing user addresses."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.model = UserAddresses  # Define the model for this repository

    async def get_address_by_id(
        self, address_id: UUID
    ) -> Optional[UserAddressRead]:
        """Retrieves an address by its ID."""
        async with self.db_session as session:
            address = await session.execute(
                select(UserAddresses).where(UserAddresses.id == address_id)
            )
            address = address.scalars().first()
            return UserAddressRead.model_validate(address) if address else None

    async def get_addresses_by_user_id(
        self, user_id: UUID
    ) -> list[UserAddressRead]:
        """Retrieves all addresses for a given user."""
        async with self.db_session as session:
            addresses = await session.execute(
                select(UserAddresses).where(UserAddresses.user_id == user_id)
            )
            addresses = addresses.scalars().all()
            return [
                UserAddressRead.model_validate(address) for address in addresses
            ]

    async def get_address_by_user_id_and_type(
        self, user_id: UUID, address_type: AddressType
    ) -> Optional[UserAddressRead]:
        """Retrieves an address by user ID and type."""
        async with self.db_session as session:
            address = await session.execute(
                select(UserAddresses).where(
                    and_(
                        UserAddresses.user_id == user_id,
                        UserAddresses.address_type == address_type,
                    )
                )
            )
            address = address.scalars().first()
            return UserAddressRead.model_validate(address) if address else None

    async def add_user_address(
        self, user_id: UUID, address_data: UserAddressCreate
    ) -> UserAddressRead:
        """Adds a new address to the user."""
        async with self.db_session as session:
            # Check for duplicates
            existing_address = await self.get_address_by_user_id_and_type(
                user_id, address_data.address_type
            )
            if existing_address:
                raise HTTPException(
                    status_code=400,
                    detail="Address of this type already exists for the user",
                )

            new_address = UserAddresses(
                **address_data.model_dump(), user_id=user_id
            )
            session.add(new_address)
            await session.commit()
            await session.refresh(new_address)
            return UserAddressRead.model_validate(new_address)

    async def update_user_address(
        self, address_id: UUID, address_data: UserAddressUpdate
    ) -> UserAddressRead:
        """Updates an existing user address."""
        async with self.db_session as session:
            address = await self.get_address_by_id(address_id)
            if not address:
                raise HTTPException(status_code=404, detail="Address not found")

            await address.update(
                session, **address_data.model_dump(exclude_unset=True)
            )

            await session.commit()
            await session.refresh(address)
            return UserAddressRead.model_validate(address)

    async def delete_user_address(self, address_id: UUID) -> None:
        """Deletes a user address."""
        async with self.db_session as session:
            address = await self.get_address_by_id(address_id)
            if not address:
                raise HTTPException(status_code=404, detail="Address not found")

            await session.delete(address)
            await session.commit()