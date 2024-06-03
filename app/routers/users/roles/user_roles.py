from fastapi import APIRouter, Depends, status
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_async_session
from app.repositories.users import UsersRepository
from app.schemas.users import RoleAssign
from app.services.users import RoleAction, UsersService

router = APIRouter()


@router.post("/roles", status_code=status.HTTP_204_NO_CONTENT)
async def assign_role_to_user(
    role_assign: RoleAssign,
    db_session: AsyncSession = Depends(get_async_session),
):
    """
    Assigns a role to the currently authenticated user.

    Requires Authentication (JWT).

    Response (Success - 204 No Content): Indicates successful role assignment.

    Error Codes:
        - 400 Bad Request: If the user already has the role.
        - 404 Not Found: If the role with the provided role_id does not exist.
    """
    user_repository = UsersRepository(db_session)
    user_service = UsersService(user_repository)
    await user_service.manage_roles(db_session, role_assign.role_id, RoleAction.ADD)


@router.delete("/roles", status_code=status.HTTP_204_NO_CONTENT)
async def remove_role_from_user(
    role_id: UUID,
    db_session: AsyncSession = Depends(get_async_session),
):
    """
    Removes a role from the currently authenticated user.

    Requires Authentication (JWT).

    Response (Success - 204 No Content): Indicates successful role removal.

    Error Codes:
        - 404 Not Found: If the user does not have the specified role.
    """
    user_repository = UsersRepository(db_session)
    user_service = UsersService(user_repository)
    await user_service.manage_roles(db_session, role_id, RoleAction.REMOVE)
