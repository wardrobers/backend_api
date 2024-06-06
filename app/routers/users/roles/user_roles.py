from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_async_session
from app.models.users import Users
from app.repositories.users import UserRoleRepository
from app.schemas.users import RoleCreate, RoleRead, RoleUpdate
from app.services.users import AuthService, UserRolesService

router = APIRouter()


# Dependency to get user roles service
async def get_user_roles_service(
    db_session: AsyncSession = Depends(get_async_session),
):
    user_role_repository = UserRoleRepository(db_session)
    return UserRolesService(user_role_repository)


@router.get("/", response_model=list[RoleRead])
async def get_all_roles(
    user_roles_service: UserRolesService = Depends(get_user_roles_service),
):
    """
    Retrieves all roles.

    **Response (Success - 200 OK):**
        - `List[RoleRead]` (schema): A list of all available roles.
    """
    return await user_roles_service.get_all_roles()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RoleRead)
async def create_role(
    role_data: RoleCreate,
    user_roles_service: UserRolesService = Depends(get_user_roles_service),
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
    return await user_roles_service.create_role(role_data)


@router.get("/{role_id}", response_model=RoleRead)
async def get_role_by_id(
    role_id: UUID4,
    user_roles_service: UserRolesService = Depends(get_user_roles_service),
):
    """
    Retrieves a role by its ID.

    **Response (Success - 200 OK):**
        - `RoleRead` (schema): The role with the specified ID.

    **Error Codes:**
        - 404 Not Found: If no role with the provided ID is found.
    """
    return await user_roles_service.get_role_by_id(role_id)


@router.put("/{role_id}", response_model=RoleRead)
async def update_role(
    role_id: UUID4,
    role_data: RoleUpdate,
    user_roles_service: UserRolesService = Depends(get_user_roles_service),
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
    return await user_roles_service.update_role(role_id, role_data)


@router.delete(
    "/{role_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_role(
    role_id: UUID4,
    user_roles_service: UserRolesService = Depends(get_user_roles_service),
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
    await user_roles_service.delete_role(role_id)


@router.post(
    "/{role_id}/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def assign_role_to_user(
    role_id: UUID4,
    user_id: UUID4,
    current_user: Users = Depends(AuthService.get_current_user),
    user_roles_service: UserRolesService = Depends(get_user_roles_service),
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
    await user_roles_service.assign_role_to_user(user_id, role_id, current_user)


@router.delete(
    "/{role_id}/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def remove_role_from_user(
    role_id: UUID4,
    user_id: UUID4,
    current_user: Users = Depends(AuthService.get_current_user),
    user_roles_service: UserRolesService = Depends(get_user_roles_service),
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
    await user_roles_service.remove_role_from_user(user_id, role_id, current_user)
