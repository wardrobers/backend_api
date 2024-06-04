from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import UUID

from app.database import get_async_session
from app.models.users import UserAddresses, Users
from app.repositories import UsersRepository
from app.schemas.users import UserAddressCreate, UserAddressRead, UserAddressUpdate
from app.services.users import AuthService, UserAddressService

router = APIRouter()


# --- Add User Address ---
@router.post(
    "/addresses", status_code=status.HTTP_201_CREATED, response_model=UserAddressRead
)
async def add_user_address(
    address_data: UserAddressCreate,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(AuthService.get_current_user),
):
    """
    Adds a new address to the user's profile.

    Requires Authentication (JWT).

    Request Body:
        - address_data (UserAddressCreate): The address details.

    Response (Success - 201 Created):
        - UserAddressRead: The newly created address object.

    Error Codes:
        - 400 Bad Request: If there is an error adding the address.
        - 401 Unauthorized: If the user is not authenticated.
    """
    user_repository = UsersRepository(db_session)
    user_address_service = UserAddressService(user_repository)
    new_address = await user_address_service.add_user_address(
        current_user.id, address_data
    )
    return new_address


# --- Get User Addresses ---
@router.get("/addresses", response_model=list[UserAddressRead])
async def get_user_addresses(
    db_session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(AuthService.get_current_user),
):
    """
    Retrieves all addresses associated with the authenticated user.

    Requires Authentication (JWT).

    Response (Success - 200 OK):
        - List[UserAddressRead]: A list of the user's addresses.

    Error Codes:
        - 401 Unauthorized: If the user is not authenticated.
    """
    user_repository = UsersRepository(db_session)
    # Assuming your Users model has a relationship 'addresses'
    addresses = current_user.addresses
    return addresses


# --- Update User Address ---
@router.put(
    "/addresses/{address_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserAddressRead,
)
async def update_user_address(
    address_id: UUID,
    address_update: UserAddressUpdate,
    db_session: AsyncSession = Depends(get_async_session),
):
    """
    Updates a specific address belonging to the current user.

    Requires Authentication (JWT).

    Request Body:
        - address_update (UserAddressUpdate): The updated address details.

    Response (Success - 200 OK):
        - UserAddressRead: The updated address object.

    Error Codes:
        - 400 Bad Request: If there is an error updating the address.
        - 401 Unauthorized: If the user is not authenticated.
        - 404 Not Found: If no address with the given address_id is found.
    """
    user_repository = UsersRepository(db_session)
    user_address_service = UserAddressService(user_repository)
    updated_address = await user_address_service.update_user_address(
        address_id, address_update
    )
    return updated_address


# --- Delete User Address ---
@router.delete("/addresses/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_address(
    address_id: UUID,
    db_session: AsyncSession = Depends(get_async_session),
):
    """
    Deletes a specific address from the current user's profile.

    Requires Authentication (JWT).

    Response (Success - 204 No Content): Indicates successful address deletion.

    Error Codes:
        - 401 Unauthorized: If the user is not authenticated.
        - 404 Not Found: If no address with the given address_id is found.
    """
    user_repository = UsersRepository(db_session)
    user_address_service = UserAddressService(user_repository)
    await user_address_service.delete_user_address(address_id)
