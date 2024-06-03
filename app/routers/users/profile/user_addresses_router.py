from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_async_session
from app.models.users import Users
from app.repositories.users import UsersRepository
from app.schemas.users import UserAddressUpdate
from app.services.users import AuthService, UsersService

router = APIRouter()


@router.post("/addresses", status_code=status.HTTP_201_CREATED)
async def add_user_address(
    address_data,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(AuthService.get_current_user),
):
    """
    Adds a new address to the user's profile.

    Requires Authentication (JWT).

    Request Body:
        - address_data (UserAddressCreate): A JSON object with the address details
                                          (street, city, postal code, etc.).

    Response (Success - 201 Created):
        - UserAddressUpdate (schema): The newly created address object in JSON format.
    """
    user_service = UsersService(UsersRepository(db_session))
    await user_service.add_or_update_address(
        db_session, current_user.id, address_data.dict()
    )
    return address_data


@router.put("/addresses")
async def update_user_address(
    address_id: UUID,
    address_update: UserAddressUpdate,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(AuthService.get_current_user),
):
    """
    Updates a specific address belonging to the current user.

    Requires Authentication (JWT).

    Request Body:
        - address_update (UserAddressUpdate): A JSON object with the updated
                                            address fields.

    Response (Success - 200 OK):
        - UserAddressUpdate (schema): The updated address object in JSON format.

    Error Codes:
        - 404 Not Found: If no address with the given address_id is found.
    """
    user_service = UsersService(UsersRepository(db_session))
    await user_service.add_or_update_address(
        db_session, current_user.id, address_update.model_dump(), address_id=address_id
    )
    return address_update


@router.delete("/addresses", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_address(
    address_id: UUID,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(AuthService.get_current_user),
):
    """
    Deletes a specific address from the current user's profile.

    Requires Authentication (JWT).

    Response (Success - 204 No Content): Indicates successful address deletion.

    Error Codes:
        - 404 Not Found: If no address with the given address_id is found.
    """
    address = next((a for a in current_user.addresses if a.id == address_id), None)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    await address.delete(db_session)
