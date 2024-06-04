# app/services/users/user_service.py
from sqlalchemy.orm import UUID

from app.repositories.users import UserRoleRepository
from app.schemas.users import RoleAssign


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
    async def assign_role_to_user(self, user_id: UUID, role_assign: RoleAssign) -> None:
        """Assigns a role to a user."""
        await self.user_role_repository.assign_role_to_user(user_id, role_assign)

    async def remove_role_from_user(self, user_id: UUID, role_id: UUID) -> None:
        """Removes a role from a user."""
        await self.user_role_repository.remove_role_from_user(user_id, role_id)
