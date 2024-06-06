# backend_API/app/routers/users/profile/user_addresses_router.py
from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_async_session
from app.models.users import Users
from app.repositories.users import UserAddressRepository
from app.schemas.users import UserAddressCreate, UserAddressRead, UserAddressUpdate
from app.services.users import AuthService
from app.services.users.profile.user_addresses_service import UserAddressesService

router = APIRouter()


# Dependency to get user addresses service
async def get_user_address_service(
    db_session: AsyncSession = Depends(get_async_session),
):
    user_address_repository = UserAddressRepository(db_session)
    return UserAddressesService(user_address_repository)


# --- Add User Address ---
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserAddressRead)
async def add_user_address(
    address_data: UserAddressCreate,
    current_user: Users = Depends(AuthService.get_current_user),
    user_address_service: UserAddressesService = Depends(get_user_address_service),
):
    """
    Adds a new address to the user's profile.

    **Requires Authentication (JWT).**

    **Request Body:**
        - `address_data` (UserAddressCreate): The address details.

    **Response (Success - 201 Created):**
        - `UserAddressRead` (schema): The newly created address object.

    **Error Codes:**
        - 400 Bad Request: If there is an error adding the address (e.g., address already exists).
        - 401 Unauthorized: If the user is not authenticated.
    """
    return await user_address_service.create_user_address(current_user.id, address_data)


# --- Get User Addresses ---
@router.get("/{address_id}", response_model=UserAddressRead)
async def get_address(
    address_id: UUID4,
    user_address_service: UserAddressesService = Depends(get_user_address_service),
):
    """
    Retrieves address by its UUID.

    **Requires Authentication (JWT).**

    **Response (Success - 200 OK):**
        - `UserAddressRead` (schema): User's address.
    """
    return await user_address_service.get_address(address_id)


@router.get("/", response_model=list[UserAddressRead])
async def get_all_user_addresses(
    current_user: Users = Depends(AuthService.get_current_user),
    user_address_service: UserAddressesService = Depends(get_user_address_service),
):
    """
    Retrieves all addresses associated with the authenticated user.

    **Requires Authentication (JWT).**

    **Response (Success - 200 OK):**
        - `List[UserAddressRead]` (schema): A list of the user's addresses.
    """
    return await user_address_service.get_all_user_addresses(current_user.id)


# --- Update User Address ---
@router.put(
    "/{address_id}", status_code=status.HTTP_200_OK, response_model=UserAddressRead
)
async def update_user_address(
    address_id: UUID4,
    address_update: UserAddressUpdate,
    current_user: Users = Depends(AuthService.get_current_user),
    user_address_service: UserAddressesService = Depends(get_user_address_service),
):
    """
    Updates a specific address belonging to the current user.

    **Requires Authentication (JWT).**

    **Request Body:**
        - `address_update` (UserAddressUpdate): The updated address details.

    **Response (Success - 200 OK):**
        - `UserAddressRead` (schema): The updated address object.

    **Error Codes:**
        - 400 Bad Request: If there's an error updating the address.
        - 401 Unauthorized: If the user is not authenticated.
        - 403 Forbidden: If the user is not authorized to update the address.
        - 404 Not Found: If the address with the given `address_id` is not found for the user.
    """
    return await user_address_service.update_user_address(
        current_user.id, address_id, address_update
    )


# --- Delete User Address ---
@router.delete(
    "/{address_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_user_address(
    address_id: UUID4,
    current_user: Users = Depends(AuthService.get_current_user),
    user_address_service: UserAddressesService = Depends(get_user_address_service),
):
    """
    Deletes a specific address from the current user's profile.

    **Requires Authentication (JWT).**

    **Response (Success - 204 No Content):**
        - Indicates successful address deletion.

    **Error Codes:**
        - 401 Unauthorized: If the user is not authenticated.
        - 403 Forbidden: If the user is not authorized to delete the address.
        - 404 Not Found: If the address with the given `address_id` is not found for the user.
    """
    await user_address_service.delete_user_address(current_user.id, address_id)
