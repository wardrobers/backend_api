from typing import Optional

from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.models.users import Users
from app.repositories.users import UserRoleRepository, UsersRepository
from app.schemas.users import RoleCreate, RoleRead, RoleUpdate

user_role_repository = UserRoleRepository()
users_repository = UsersRepository()


class UserRolesService:
    """
    Service layer for managing user roles, providing a clear interface
    for role-related operations and leveraging the repository for data access.
    """

    def get_all_roles(self) -> list[RoleRead]:
        """Retrieves all roles."""
        return user_role_repository.get_all_roles()

    def create_role(self, db_session: Session, role_data: RoleCreate) -> RoleRead:
        """Creates a new role."""
        # Add any validation or business logic here before creating the role.
        return user_role_repository.create_role(db_session, role_data)

    def get_role_by_id(self, db_session: Session, role_id: UUID4) -> RoleRead:
        """Retrieves a role by its ID."""
        role = user_role_repository.get_role_by_id(db_session, role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role

    def update_role(
        self, db_session: Session, role_id: UUID4, role_data: RoleUpdate
    ) -> RoleRead:
        """Updates a role."""
        # Add any authorization or validation logic here.
        return user_role_repository.update_role(db_session, role_id, role_data)

    def delete_role(self, db_session: Session, role_id: UUID4) -> None:
        """Deletes a role."""
        # Add authorization or validation logic here, e.g.,
        # prevent deleting roles that are currently assigned to users.
        user_role_repository.delete(db_session, role_id)

    def assign_role_to_user(
        self,
        db_session: Session,
        user_id: UUID4,
        role_id: UUID4,
        current_user: Optional[Users] = None,
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
        if not users_repository.get_by_id(db_session, user_id):
            raise HTTPException(status_code=404, detail="User not found")

        # Check if the role exists:
        if not user_role_repository.get_role_by_id(role_id):
            raise HTTPException(status_code=404, detail="Role not found")

        user_role_repository.assign_role_to_user(db_session, user_id, role_id)

    def remove_role_from_user(
        self,
        db_session: Session,
        user_id: UUID4,
        role_id: UUID4,
        current_user: Optional[Users] = None,
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

        user_role_repository.remove_role_from_user(user_id, role_id)

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

    def get_user_roles(self, db_session: Session, user_id: UUID4) -> list[RoleRead]:
        """Retrieves the roles assigned to a user."""
        return user_role_repository.get_user_roles(db_session, user_id)
