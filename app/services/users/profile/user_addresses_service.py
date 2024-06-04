# app/services/users/user_service.py
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID

from app.models.users import UserAddresses
from app.repositories.users import UserAddressRepository
from app.schemas.users import UserAddressCreate, UserAddressUpdate


class UserAddressesService:
    """
    Service layer for core user management operations.
    """

    def __init__(
        self,
        user_address_repository: UserAddressRepository,
    ):
        self.user_address_repository = user_address_repository

    # --- User Address Operations ---
    async def get_user_addresses(self, user_id: UUID) -> list[UserAddresses]:
        """Retrieves all addresses for a given user."""
        return await self.user_address_repository.get_addresses_by_user_id(user_id)

    async def add_user_address(
        self, user_id: UUID, address_data: UserAddressCreate
    ) -> UserAddresses:
        """Adds a new address to the user."""
        return await self.user_address_repository.add_user_address(
            user_id, address_data
        )

    async def update_user_address(
        self, user_id: UUID, address_id: UUID, address_data: UserAddressUpdate
    ) -> UserAddresses:
        """Updates an existing user address."""
        address = await self.user_address_repository.get_address_by_id(address_id)
        if not address or address.user_id != user_id:
            raise HTTPException(
                status_code=404, detail="Address not found for this user"
            )
        return await self.user_address_repository.update_user_address(
            address_id, address_data
        )

    async def delete_user_address(self, user_id: UUID, address_id: UUID) -> None:
        """Deletes a user address."""
        address = await self.user_address_repository.get_address_by_id(address_id)
        if not address or address.user_id != user_id:
            raise HTTPException(
                status_code=404, detail="Address not found for this user"
            )
        await self.user_address_repository.delete_user_address(address_id)
