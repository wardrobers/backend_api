from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.config import oauth2_scheme
from app.database.session import get_db
from app.models.users import Users
from app.repositories.users import UserRoleRepository
from app.schemas.users import RoleCreate, RoleRead, RoleUpdate
from app.services.users import AuthService, UserRolesService, UsersService

router = APIRouter()
auth_service = AuthService()
user_service = UsersService()
user_roles_service = UserRolesService()


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


@router.get("/", response_model=list[RoleRead])
def get_all_roles(
    db_session: Session = Depends(get_db),
):
    """
    Retrieves all roles.

    **Response (Success - 200 OK):**
        - `List[RoleRead]` (schema): A list of all available roles.
    """
    return user_roles_service.get_all_roles(db_session)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RoleRead)
def create_role(
    role_data: RoleCreate,
    db_session: Session = Depends(get_db),
):
    """
    Creates a new role.

    **Requires appropriate permissions.**

    **Request Body:**
        - `RoleCreate` (schema): The role data to create.

    **Response (Success - 201 Created):**
        - `RoleRead` (schema): The newly created role.

    **Error Codes:**
        - 400 Bad Request: If the role data is invalid or a role with the same code already exists.
        - 403 Forbidden: If the user doesn't have permission to create roles.
    """
    return user_roles_service.create_role(db_session, role_data)


@router.get("/{role_id}", response_model=RoleRead)
def get_role_by_id(
    role_id: UUID4,
    db_session: Session = Depends(get_db),
):
    """
    Retrieves a role by its ID.

    **Response (Success - 200 OK):**
        - `RoleRead` (schema): The role with the specified ID.

    **Error Codes:**
        - 404 Not Found: If no role with the provided ID is found.
    """
    return user_roles_service.get_role_by_id(db_session, role_id)


@router.put("/{role_id}", response_model=RoleRead)
def update_role(
    role_id: UUID4,
    role_data: RoleUpdate,
    db_session: Session = Depends(get_db),
):
    """
    Updates a role.

    **Requires appropriate permissions.**

    **Request Body:**
        - `RoleUpdate` (schema): The updated role data.

    **Response (Success - 200 OK):**
        - `RoleRead` (schema): The updated role.

    **Error Codes:**
        - 400 Bad Request: If the role data is invalid.
        - 403 Forbidden: If the user doesn't have permission to update roles.
        - 404 Not Found: If the role with the provided ID is not found.
    """
    return user_roles_service.update_role(db_session, role_id, role_data)


@router.delete(
    "/{role_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
def delete_role(
    role_id: UUID4,
    db_session: Session = Depends(get_db),
):
    """
    Deletes a role.

    **Requires appropriate permissions.**

    **Response (Success - 204 No Content):**
        - Indicates successful role deletion.

    **Error Codes:**
        - 403 Forbidden: If the user doesn't have permission to delete roles.
        - 404 Not Found: If the role with the provided ID is not found.
    """
    user_roles_service.delete_role(db_session, role_id)


@router.post(
    "/{role_id}/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def assign_role_to_user(
    role_id: UUID4,
    user_id: UUID4,
    current_user: Users = Depends(get_current_active_user),
    db_session: Session = Depends(get_db),
):
    """
    Assigns a role to a user.

    **Requires appropriate permissions.**

    **Response (Success - 204 No Content):**
        - Indicates successful role assignment.

    **Error Codes:**
        - 400 Bad Request: If the role is already assigned to the user.
        - 403 Forbidden: If the user doesn't have permission to assign roles.
        - 404 Not Found: If the user or role is not found.
    """
    user_roles_service.assign_role_to_user(db_session, user_id, role_id, current_user)


@router.delete(
    "/{role_id}/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def remove_role_from_user(
    role_id: UUID4,
    user_id: UUID4,
    current_user: Users = Depends(get_current_active_user),
    db_session: Session = Depends(get_db),
):
    """
    Removes a role from a user.

    **Requires appropriate permissions.**

    **Response (Success - 204 No Content):**
        - Indicates successful role removal.

    **Error Codes:**
        - 403 Forbidden: If the user doesn't have permission to remove roles.
        - 404 Not Found: If the user doesn't have the specified role.
    """
    user_roles_service.remove_role_from_user(db_session, user_id, role_id, current_user)
