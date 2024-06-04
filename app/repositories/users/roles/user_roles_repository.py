from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import UUID

from app.models.users import UserRoles
from app.models.users.roles.roles_model import Roles
from app.schemas.users import RoleAssign, RoleBase, RoleRead


class UserRoleRepository:
    """Repository for managing user roles."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_role_by_id(self, role_id: UUID) -> Optional[Roles]:
        """Retrieves a role by ID."""
        result = await self.db_session.execute(
            select(Roles).where(Roles.id == role_id, Roles.deleted_at.is_(None))
        )
        return result.scalars().first()

    async def get_all_roles(self) -> list[Roles]:
        """Retrieves all roles."""
        result = await self.db_session.execute(
            select(Roles).where(Roles.deleted_at.is_(None))
        )
        return result.scalars().all()

    async def create_role(self, role_data: RoleBase) -> Roles:
        """Creates a new role."""
        new_role = Roles(**role_data.model_dump())
        await new_role.create(self.db_session)
        return new_role

    async def update_role(self, role_id: UUID, role_data: RoleBase) -> Roles:
        """Updates a role."""
        role = await self.get_role_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        await role.update(self.db_session, **role_data.model_dump(exclude_unset=True))
        return role

    async def delete_role(self, role_id: UUID) -> None:
        """Deletes a role."""
        role = await self.get_role_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        await role.delete(self.db_session)

    async def assign_role_to_user(self, user_id: UUID, role_assign: RoleAssign) -> None:
        """Assigns a role to a user."""
        existing_role = await self.db_session.execute(
            select(UserRoles).where(
                UserRoles.user_id == user_id, UserRoles.role_id == role_assign.role_id
            )
        )
        if existing_role.scalars().first() is not None:
            raise HTTPException(
                status_code=400, detail="Role already assigned to user."
            )

        new_user_role = UserRoles(user_id=user_id, role_id=role_assign.role_id)
        await new_user_role.create(self.db_session)

    async def remove_role_from_user(self, user_id: UUID, role_id: UUID) -> None:
        """Removes a role from a user."""
        role_to_delete = await self.db_session.execute(
            select(UserRoles).where(
                UserRoles.user_id == user_id, UserRoles.role_id == role_id
            )
        )
        role_to_delete = role_to_delete.scalars().first()

        if not role_to_delete:
            raise HTTPException(status_code=404, detail="User does not have this role")

        await role_to_delete.delete(self.db_session)

    async def get_user_roles(self, user_id: UUID) -> list[RoleRead]:
        """Retrieves the roles assigned to a user."""
        roles = await self.db_session.execute(
            select(Roles)
            .join(UserRoles, UserRoles.role_id == Roles.id)
            .where(UserRoles.user_id == user_id)
        )
        return [RoleRead.model_validate(role) for role in roles.scalars().all()]
