from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import UserRoles
from app.models.users.roles.roles_model import Roles
from app.repositories.common import (
    BulkActionsMixin,
    CachingMixin,
    SearchMixin,
)
from app.schemas.users import RoleCreate, RoleRead, RoleUpdate


class UserRoleRepository(CachingMixin, BulkActionsMixin, SearchMixin):
    """Repository for managing user roles."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.model = Roles  # Define the model for this repository

    async def get_role_by_id(self, role_id: UUID) -> Optional[Roles]:
        """Retrieves a role by ID."""
        async with self.db_session as session:
            role = await session.execute(
                select(Roles).where(Roles.id == role_id, Roles.deleted_at.is_(None))
            )
            return role.scalars().first() if role else None

    async def get_all_roles(self) -> list[Roles]:
        """Retrieves all roles."""
        async with self.db_session as session:
            return await session.execute(
                select(Roles).where(Roles.deleted_at.is_(None))
            )

    async def create_role(self, role_data: RoleCreate) -> Roles:
        """Creates a new role."""
        async with self.db_session as session:
            new_role = Roles(**role_data.model_dump())
            session.add(new_role)
            await session.commit()
            await session.refresh(new_role)
            return new_role

    async def update_role(self, role_id: UUID, role_data: RoleUpdate) -> Roles:
        """Updates a role."""
        async with self.db_session as session:
            role = await self.get_role_by_id(role_id)
            if not role:
                raise HTTPException(status_code=404, detail="Role not found")
            await role.update(session, **role_data.model_dump(exclude_unset=True))
            await session.commit()
            await session.refresh(role)
            return role

    async def delete_role(self, role_id: UUID) -> None:
        """Deletes a role."""
        async with self.db_session as session:
            role = await self.get_role_by_id(role_id)
            if not role:
                raise HTTPException(status_code=404, detail="Role not found")
            await session.delete(role)
            await session.commit()

    async def assign_role_to_user(self, user_id: UUID, role_id: UUID) -> None:
        """Assigns a role to a user."""
        async with self.db_session as session:
            existing_role = await session.execute(
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
            session.add(new_user_role)
            await session.commit()

    async def remove_role_from_user(self, user_id: UUID, role_id: UUID) -> None:
        """Removes a role from a user."""
        async with self.db_session as session:
            role_to_delete = await session.execute(
                select(UserRoles).where(
                    UserRoles.user_id == user_id, UserRoles.role_id == role_id
                )
            )
            role_to_delete = role_to_delete.scalars().first()

            if not role_to_delete:
                raise HTTPException(
                    status_code=404, detail="User does not have this role"
                )

            await session.delete(role_to_delete)
            await session.commit()

    async def get_user_roles(self, user_id: UUID) -> list[RoleRead]:
        """Retrieves the roles assigned to a user."""
        async with self.db_session as session:
            return await session.execute(
                select(Roles)
                .join(UserRoles, UserRoles.role_id == Roles.id)
                .where(UserRoles.user_id == user_id)
            )
