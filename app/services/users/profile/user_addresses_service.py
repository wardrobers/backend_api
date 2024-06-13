from typing import Optional

from fastapi import HTTPException, status
from pydantic import UUID4

from app.repositories.users import UserAddressRepository
from app.schemas.users import (
    AddressType,
    UserAddressCreate,
    UserAddressRead,
    UserAddressUpdate,
)


class UserAddressesService:
    """
    Service layer for managing user addresses, providing advanced logic,
    authorization checks, and business-specific functionalities.
    """

    def __init__(self, user_address_repository: UserAddressRepository):
        self.user_address_repository = user_address_repository

    def get_address_by_id(
        self, address_id: UUID4, current_user_id: Optional[UUID4] = None
    ) -> UserAddressRead:
        """
        Retrieves an address by ID, optionally checking authorization.
        """
        address = self.user_address_repository.get_address_by_id(address_id)

        if not address:
            raise HTTPException(status_code=404, detail="Address not found")

        # Authorization check (example):
        if current_user_id and address.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this address",
            )

        return UserAddressRead.model_validate(address)

    def get_addresses_by_user_id(self, user_id: UUID4) -> list[UserAddressRead]:
        """
        Retrieves all addresses for a given user.
        """
        return self.user_address_repository.get_addresses_by_user_id(user_id)

    def create_user_address(
        self, user_id: UUID4, address_data: UserAddressCreate
    ) -> UserAddressRead:
        """
        Creates a new address for a user.
        """
        # You can add more validation or business logic here, e.g.,
        # checking address validity using an external service.

        address = self.user_address_repository.add_user_address(user_id, address_data)
        return UserAddressRead.model_validate(address)

    def update_user_address(
        self,
        address_id: UUID4,
        address_data: UserAddressUpdate,
        current_user_id: UUID4,
    ) -> UserAddressRead:
        """
        Updates an existing user address, with authorization check.
        """
        address = self.user_address_repository.get_address_by_id(address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")

        # Authorization check:
        if address.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this address",
            )

        address = self.user_address_repository.update_user_address(
            address_id, address_data
        )
        return UserAddressRead.model_validate(address)

    def delete_user_address(self, address_id: UUID4, current_user_id: UUID4) -> None:
        """
        Deletes a user address, with authorization check.
        """
        address = self.user_address_repository.get_address_by_id(address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")

        # Authorization check:
        if address.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this address",
            )

        self.user_address_repository.delete_user_address(address_id)

    # --- Advanced Business Logic Methods ---

    def set_default_address(
        self, user_id: UUID4, address_id: UUID4, address_type: AddressType
    ) -> UserAddressRead:
        """
        Sets the specified address as the user's default for the given type
        (shipping or billing).
        """
        # 1. Get the address to be set as default.
        address_to_set_default = self.get_address_by_id(address_id)
        if address_to_set_default.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The address does not belong to this user",
            )

        # 2. Find any existing default address of the same type for the user.
        existing_default_address = (
            self.user_address_repository.get_address_by_user_id_and_type(
                user_id, address_type
            )
        )

        with self.user_address_repository.db_session as session:
            # 3. If there's an existing default, update it to no longer be default.
            if existing_default_address:
                existing_default_address.address_type = AddressType.SHIPPING
                existing_default_address.update(session)

            # 4. Update the selected address to be the default.
            address_to_set_default.address_type = address_type
            address_to_set_default.update(session)

        return UserAddressRead.model_validate(address_to_set_default)

    def validate_address(self, address_data: UserAddressCreate) -> bool:
        """
        Validates the address using an external service (placeholder).
        """
        # TODO: Integrate with an address validation API
        # (e.g., Google Maps API, SmartyStreets)
        return True  # Placeholder - replace with actual validation logic

    def get_preferred_address(self, user_id: UUID4) -> Optional[UserAddressRead]:
        """
        Retrieves the user's preferred address (if defined). You might
        implement logic to determine the preferred address based on usage,
        a user setting, or other factors.
        """
        # TODO: Implement logic to determine and retrieve the preferred address.
        return None  # Placeholder
