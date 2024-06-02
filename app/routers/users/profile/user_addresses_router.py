from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_async_session
from app.models.users.core.users_model import Users
from app.models.users.profile.user_addresses_model import UserAddresses
from app.routers.users import auth_handler

router = APIRouter()


@router.post("/addresses", status_code=status.HTTP_201_CREATED)
async def add_user_address(
    address_data,
    db: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(auth_handler.get_current_user),
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
    new_address = UserAddresses(user_id=current_user.id, **address_data.dict())
    db.add(new_address)
    await db.commit()
    await db.refresh(new_address)
    return new_address


@router.put("/addresses")
async def update_user_address(
    address_id: UUID,
    address_update,
    db: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(auth_handler.get_current_user),
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
    address = next((a for a in current_user.addresses if a.id == address_id), None)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    update_data = address_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(address, key, value)

    await db.commit()
    await db.refresh(address)
    return address


@router.delete("/addresses", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_address(
    address_id: UUID,
    db: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(auth_handler.get_current_user),
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

    await address.delete(db)
