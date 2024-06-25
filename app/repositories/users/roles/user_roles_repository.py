from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.models.users import UserRoles
from app.models.users.roles.roles_model import Roles
from app.repositories.common import BulkActionsMixin, CachingMixin, SearchMixin
from app.schemas.users import RoleCreate, RoleRead, RoleUpdate


class UserRoleRepository(CachingMixin, BulkActionsMixin, SearchMixin):
    """Repository for managing user roles."""

    model = Roles

    def get_role_by_id(self, db_session: Session, role_id: UUID) -> Optional[Roles]:
        """Retrieves a role by ID."""

        role = db_session.execute(
            select(Roles).where(Roles.id == role_id, Roles.deleted_at.is_(None))
        )
        return role.scalars().first() if role else None

    def get_all_roles(self, db_session: Session) -> list[Roles]:
        """Retrieves all roles."""

        return db_session.execute(select(Roles).where(Roles.deleted_at.is_(None)))

    def create_role(self, db_session: Session, role_data: RoleCreate) -> Roles:
        """Creates a new role."""

        new_role = Roles(**role_data.model_dump())
        db_session.add(new_role)
        db_session.commit()
        db_session.refresh(new_role)
        return new_role

    def update_role(
        self, db_session: Session, role_id: UUID, role_data: RoleUpdate
    ) -> Roles:
        """Updates a role."""

        role = self.get_role_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        role.update(self.session, **role_data.model_dump(exclude_unset=True))
        db_session.commit()
        db_session.refresh(role)
        return role

    def delete_role(self, db_session: Session, role_id: UUID) -> None:
        """Deletes a role."""
        role = self.get_role_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        db_session.delete(role)
        db_session.commit()

    def assign_role_to_user(
        self, db_session: Session, user_id: UUID, role_id: UUID
    ) -> None:
        """Assigns a role to a user."""
        existing_role = db_session.execute(
            select(UserRoles).where(
                UserRoles.user_id == user_id, UserRoles.role_id == role_id
            )
        )
        if existing_role.scalars().first() is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role already assigned to user.",
            )

        new_user_role = UserRoles(user_id=user_id, role_id=role_id)
        db_session.add(new_user_role)
        db_session.commit()

    def remove_role_from_user(
        self, db_session: Session, user_id: UUID, role_id: UUID
    ) -> None:
        """Removes a role from a user."""
        role_to_delete = db_session.execute(
            select(UserRoles).where(
                UserRoles.user_id == user_id, UserRoles.role_id == role_id
            )
        )
        role_to_delete = role_to_delete.scalars().first()

        if not role_to_delete:
            raise HTTPException(status_code=404, detail="User does not have this role")

        db_session.delete(role_to_delete)
        db_session.commit()

    def get_user_roles(self, db_session: Session, user_id: UUID) -> list[RoleRead]:
        """Retrieves the roles assigned to a user."""
        return db_session.execute(
            select(Roles)
            .join(UserRoles, UserRoles.role_id == Roles.id)
            .where(UserRoles.user_id == user_id)
        )
