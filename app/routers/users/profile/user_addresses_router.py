# backend_API/app/routers/users/profile/user_addresses_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.config import oauth2_scheme
from app.database.session import get_db
from app.models.users import Users
from app.schemas.users import UserAddressCreate, UserAddressRead, UserAddressUpdate
from app.services.users import AuthService
from app.services.users.profile.user_addresses_service import UserAddressesService

router = APIRouter()
auth_service = AuthService()
user_address_service = UserAddressesService()


def get_current_active_user(
    db_session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> Users:
    """Dependency to get the currently authenticated user from the JWT token."""
    user = auth_service.get_current_user(db_session, token)
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


def get_current_user_id(
    current_user: Users = Depends(get_current_active_user),
) -> UUID4:
    """Dependency to get the user_id of the current user."""
    return current_user.id


# --- Add User Address ---
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserAddressRead)
def add_user_address(
    address_data: UserAddressCreate,
    current_user: Users = Depends(get_current_active_user),
    db_session: Session = Depends(get_db),
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
    return user_address_service.create_user_address(
        db_session, current_user.id, address_data
    )


# --- Get User Addresses ---
@router.get("/{address_id}", response_model=UserAddressRead)
def get_address(
    address_id: UUID4,
    db_session: Session = Depends(get_db),
):
    """
    Retrieves address by its UUID.

    **Requires Authentication (JWT).**

    **Response (Success - 200 OK):**
        - `UserAddressRead` (schema): User's address.
    """
    return user_address_service.get_address(db_session, address_id)


# @router.get("/", response_model=list[UserAddressRead])
# def get_all_user_addresses(
#     current_user: Users = Depends(AuthService.get_current_user),
#     db_session: Session = Depends(get_db),
# ):
#     """
#     Retrieves all addresses associated with the authenticated user.

#     **Requires Authentication (JWT).**

#     **Response (Success - 200 OK):**
#         - `List[UserAddressRead]` (schema): A list of the user's addresses.
#     """
#     return user_address_service.get_all_user_addresses(db_session, current_user.id)


# # --- Update User Address ---
# @router.put(
#     "/{address_id}", status_code=status.HTTP_200_OK, response_model=UserAddressRead
# )
# def update_user_address(
#     address_id: UUID4,
#     address_update: UserAddressUpdate,
#     current_user: Users = Depends(AuthService.get_current_user),
#     db_session: Session = Depends(get_db),
# ):
#     """
#     Updates a specific address belonging to the current user.

#     **Requires Authentication (JWT).**

#     **Request Body:**
#         - `address_update` (UserAddressUpdate): The updated address details.

#     **Response (Success - 200 OK):**
#         - `UserAddressRead` (schema): The updated address object.

#     **Error Codes:**
#         - 400 Bad Request: If there's an error updating the address.
#         - 401 Unauthorized: If the user is not authenticated.
#         - 403 Forbidden: If the user is not authorized to update the address.
#         - 404 Not Found: If the address with the given `address_id` is not found for the user.
#     """
#     return user_address_service.update_user_address(
#         db_session, current_user.id, address_id, address_update
#     )


# # --- Delete User Address ---
# @router.delete(
#     "/{address_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
# )
# def delete_user_address(
#     address_id: UUID4,
#     current_user: Users = Depends(AuthService.get_current_user),
#     db_session: Session = Depends(get_db),
# ):
#     """
#     Deletes a specific address from the current user's profile.

#     **Requires Authentication (JWT).**

#     **Response (Success - 204 No Content):**
#         - Indicates successful address deletion.

#     **Error Codes:**
#         - 401 Unauthorized: If the user is not authenticated.
#         - 403 Forbidden: If the user is not authorized to delete the address.
#         - 404 Not Found: If the address with the given `address_id` is not found for the user.
#     """
#     user_address_service.delete_user_address(db_session, current_user.id, address_id)
