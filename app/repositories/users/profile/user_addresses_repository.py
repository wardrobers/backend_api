from typing import Optional

from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import UserAddresses
from app.schemas.users import AddressType, UserAddressCreate, UserAddressUpdate


class UserAddressRepository:
    """Repository for managing user addresses."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_address_by_id(self, address_id: UUID) -> Optional[UserAddresses]:
        """Retrieves an address by its ID."""
        address = await self.db_session.execute(
            select(UserAddresses).where(UserAddresses.id == address_id)
        )
        return address.scalars().first()

    async def get_addresses_by_user_id(self, user_id: UUID) -> list[UserAddresses]:
        """Retrieves all addresses for a given user."""
        addresses = await self.db_session.execute(
            select(UserAddresses).where(UserAddresses.user_id == user_id)
        )
        return addresses.scalars().all()

    async def get_address_by_user_id_and_type(
        self, user_id: UUID, address_type: AddressType
    ) -> Optional[UserAddresses]:
        """Retrieves an address by user ID and type."""
        address = await self.db_session.execute(
            select(UserAddresses).where(
                and_(
                    UserAddresses.user_id == user_id,
                    UserAddresses.address_type == address_type,
                )
            )
        )
        return address.scalars().first()

    async def add_user_address(
        self, user_id: UUID, address_data: UserAddressCreate
    ) -> UserAddresses:
        """Adds a new address to the user."""
        # Check for duplicates
        existing_address = await self.get_address_by_user_id_and_type(
            user_id, address_data.address_type
        )
        if existing_address:
            raise HTTPException(
                status_code=400,
                detail="Address of this type already exists for the user",
            )

        new_address = UserAddresses(**address_data.model_dump(), user_id=user_id)
        await new_address.create(self.db_session)
        return new_address

    async def update_user_address(
        self, address_id: UUID, address_data: UserAddressUpdate
    ) -> UserAddresses:
        """Updates an existing user address."""
        address = await self.get_address_by_id(address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        await address.update(
            self.db_session, **address_data.model_dump(exclude_unset=True)
        )
        return address

    async def delete_user_address(self, address_id: UUID) -> None:
        """Deletes a user address."""
        address = await self.get_address_by_id(address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        await address.delete(self.db_session)
