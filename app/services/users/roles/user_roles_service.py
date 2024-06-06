from typing import Optional

from fastapi import HTTPException, status
from pydantic import UUID4

from app.models.users import Users
from app.repositories.users import UserRoleRepository, UsersRepository
from app.schemas.users import RoleCreate, RoleRead, RoleUpdate


class UserRolesService:
    """
    Service layer for managing user roles, providing a clear interface
    for role-related operations and leveraging the repository for data access.
    """

    def __init__(
        self,
        user_role_repository: UserRoleRepository,
        users_repository: UsersRepository,  # Inject dependency
    ):
        self.user_role_repository = user_role_repository
        self.users_repository = users_repository

    async def get_all_roles(self) -> list[RoleRead]:
        """Retrieves all roles."""
        return await self.user_role_repository.get_all_roles()

    async def create_role(self, role_data: RoleCreate) -> RoleRead:
        """Creates a new role."""
        # Add any validation or business logic here before creating the role.
        return await self.user_role_repository.create_role(role_data)

    async def get_role_by_id(self, role_id: UUID4) -> RoleRead:
        """Retrieves a role by its ID."""
        role = await self.user_role_repository.get_role_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role

    async def update_role(self, role_id: UUID4, role_data: RoleUpdate) -> RoleRead:
        """Updates a role."""
        # Add any authorization or validation logic here.
        return await self.user_role_repository.update_role(role_id, role_data)

    async def delete_role(self, role_id: UUID4) -> None:
        """Deletes a role."""
        # Add authorization or validation logic here, e.g.,
        # prevent deleting roles that are currently assigned to users.
        await self.user_role_repository.delete_role(role_id)

    async def assign_role_to_user(
        self, user_id: UUID4, role_id: UUID4, current_user: Optional[Users] = None
    ) -> None:
        """
        Assigns a role to a user, with authorization checks.
        """
        # Authorization Check (Example):
        if current_user and not self._is_authorized_to_manage_roles(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to assign roles.",
            )

        # Check if the user exists:
        if not await self.users_repository.get_by_id(
            self.users_repository.db_session, user_id
        ):
            raise HTTPException(status_code=404, detail="User not found")

        # Check if the role exists:
        if not await self.user_role_repository.get_role_by_id(role_id):
            raise HTTPException(status_code=404, detail="Role not found")

        await self.user_role_repository.assign_role_to_user(user_id, role_id)

    async def remove_role_from_user(
        self, user_id: UUID4, role_id: UUID4, current_user: Optional[Users] = None
    ) -> None:
        """
        Removes a role from a user, with authorization checks.
        """
        # Authorization Check (Example):
        if current_user and not self._is_authorized_to_manage_roles(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to remove roles.",
            )

        await self.user_role_repository.remove_role_from_user(user_id, role_id)

    def _is_authorized_to_manage_roles(
        self, current_user: Optional[Users] = None
    ) -> bool:
        """
        Checks if the current user has permissions to manage roles.
        You'll likely want to implement more sophisticated role-based
        authorization logic here.
        """
        # Placeholder - replace with your actual authorization logic
        return current_user.is_admin

    async def get_user_roles(self, user_id: UUID4) -> list[RoleRead]:
        """Retrieves the roles assigned to a user."""
        return await self.user_role_repository.get_user_roles(user_id)
