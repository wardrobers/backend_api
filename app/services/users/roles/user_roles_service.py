# app/services/users/user_service.py
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import UUID

from app.repositories.users import UserRoleRepository
from app.schemas.users import RoleAction, RoleCreate, RoleRead, RoleUpdate
from app.services.users import AuthService


class UserRolesService:
    """
    Service layer for core user management operations.
    """

    def __init__(
        self,
        user_role_repository: UserRoleRepository,
    ):
        self.user_role_repository = user_role_repository

    # --- User Role Operations ---
    async def get_all_roles(self) -> list[RoleRead]:
        """Retrieves all roles."""
        roles = await self.user_role_repository.get_all_roles()
        return [RoleRead.from_orm(role) for role in roles]

    async def create_role(self, role_data: RoleCreate) -> RoleRead:
        """Creates a new role."""
        role = await self.user_role_repository.create_role(role_data)
        return RoleRead.from_orm(role)

    async def get_role_by_id(self, role_id: UUID) -> RoleRead:
        """Retrieves a role by its ID."""
        role = await self.user_role_repository.get_role_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return RoleRead.from_orm(role)

    async def update_role(self, role_id: UUID, role_data: RoleUpdate) -> RoleRead:
        """Updates a role."""
        role = await self.user_role_repository.update_role(role_id, role_data)
        return RoleRead.from_orm(role)

    async def delete_role(self, role_id: UUID) -> None:
        """Deletes a role."""
        await self.user_role_repository.delete_role(role_id)

    async def assign_role_to_user(self, user_id: UUID, role_id: UUID) -> None:
        """
        Assigns a role to a user, ensuring both exist and handling specific logic.
        """
        user = await self.users_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        role = await self.user_role_repository.get_role_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        await self.user_role_repository.assign_role_to_user(user_id, role_id)

    async def remove_role_from_user(self, user_id: UUID, role_id: UUID) -> None:
        """Removes a role from a user."""
        await self.user_role_repository.remove_role_from_user(user_id, role_id)

    async def manage_roles(
        self, db_session: AsyncSession, role_id: UUID, action: RoleAction
    ):
        """Manages roles for the current user."""
        current_user = await AuthService.get_current_user(db_session)
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )

        role = await self.user_role_repository.get_role_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        if action == RoleAction.ADD:
            await self.assign_role_to_user(db_session, current_user.id, role_id)
        elif action == RoleAction.REMOVE:
            await self.remove_role_from_user(db_session, current_user.id, role_id)
        else:
            raise ValueError("Invalid Role Action")
