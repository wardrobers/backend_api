# app/services/users/user_service.py
from fastapi import HTTPException
from sqlalchemy.orm import UUID

from app.repositories.users import UserRoleRepository
from app.schemas.users import RoleAssign, RoleBase


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
    async def get_all_roles(self):
        """Retrieves all roles."""
        return await self.user_role_repository.get_all_roles()

    async def create_role(self, role_data: RoleBase):
        """Creates a new role."""
        return await self.user_role_repository.create_role(role_data)

    async def assign_role_to_user(self, user_id: UUID, role_assign: RoleAssign) -> None:
        """
        Assigns a role to a user, ensuring both exist and handling specific logic.
        """
        role = await self.user_role_repository.get_role_by_id(role_assign.role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        # Example of complex business logic:
        # - Check if the user already has the role.
        # - Check if the user is allowed to be assigned this role (based on permissions).
        # - Log the role assignment action.
        # ... 

        await self.user_role_repository.assign_role_to_user(user_id, role_assign)
