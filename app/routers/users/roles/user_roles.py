from fastapi import APIRouter, Depends, HTTPException, select, status
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.users import Roles, User
from app.routers.users import auth_handler

router = APIRouter()


@router.post("/roles", status_code=status.HTTP_204_NO_CONTENT)
async def assign_role_to_user(
    role_id: UUID,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth_handler.get_current_user),
):
    """
    Assigns a role to the currently authenticated user.

    Requires Authentication (JWT).

    Response (Success - 204 No Content): Indicates successful role assignment.

    Error Codes:
        - 400 Bad Request: If the user already has the role.
        - 404 Not Found: If the role with the provided role_id does not exist.
    """
    role = await db.execute(select(Roles).filter(Roles.id == role_id))
    role = role.scalars().first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role in current_user.roles:
        raise HTTPException(status_code=400, detail="User already has this role")

    current_user.roles.append(role)
    await db.commit()


@router.delete("/roles", status_code=status.HTTP_204_NO_CONTENT)
async def remove_role_from_user(
    role_id: UUID,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth_handler.get_current_user),
):
    """
    Removes a role from the currently authenticated user.

    Requires Authentication (JWT).

    Response (Success - 204 No Content): Indicates successful role removal.

    Error Codes:
        - 404 Not Found: If the user does not have the specified role.
    """
    role = next((r for r in current_user.roles if r.id == role_id), None)
    if not role:
        raise HTTPException(status_code=404, detail="User does not have this role")

    current_user.roles.remove(role)
    await db.commit()
