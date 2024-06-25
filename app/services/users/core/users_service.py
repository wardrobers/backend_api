from typing import Optional

from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.models.users import Users
from app.repositories.users import UsersRepository
from app.schemas.users import UserLogin, UsersCreate, UsersRead, UsersUpdate
from app.services.users import AuthService

users_repository = UsersRepository()
auth_service = AuthService()


class UsersService:
    """
    Service layer for core user management operations, utilizing repositories
    with mixins for enhanced functionality and code reuse.
    """

    def get_user_by_id(self, db_session: Session, user_id: UUID4) -> UsersRead:
        """Retrieves a user by their ID."""
        user = users_repository.get_by_id(db_session, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UsersRead.model_validate(user)

    def get_user_by_login(self, db_session: Session, login: str) -> UsersRead:
        """Retrieves a user by their login."""
        user = users_repository.get_user_by_login(db_session, login)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UsersRead.model_validate(user)

    def get_all_users(self, db_session: Session) -> list[UsersRead]:
        """Retrieves all users."""
        users = users_repository.get_all(db_session)
        return [UsersRead.model_validate(user) for user in users]

    def create_user(self, db_session: Session, user_data: UsersCreate) -> UsersRead:
        """
        Registers a new user.
        """
        if user_data.password != user_data.password_confirmation:
            raise HTTPException(status_code=400, detail="Passwords don't match")

        existing_user = users_repository.get_user_by_login(db_session, user_data.login)
        if existing_user:
            raise HTTPException(status_code=400, detail="Login already in use")

        try:
            auth_service.validate_password_strength(user_data.password)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        user_data.password = auth_service.get_password_hash(user_data.password)
        new_user = users_repository.create(
            db_session, **user_data.model_dump(exclude={"password_confirmation"})
        )
        user_login = UsersRead(
            id=new_user.id, login=new_user.login, password=new_user.password
        )

        return UsersRead.model_validate(user_login)

    def update_user(
        self,
        db_session: Session,
        user_id: UUID4,
        user_data: UsersUpdate,
        current_user: Users,
    ) -> Users:
        """
        Updates a user's core information.
        """
        # Authorization check:
        if current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this user",
            )

        return users_repository.update(db_session, user_id, user_data)

    def authenticate_user(
        self, db_session: Session, login_data: UserLogin
    ) -> Optional[Users]:
        """Authenticates a user based on login and password."""
        user = users_repository.get_user_by_login(db_session, login_data.login)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if not auth_service.verify_password(login_data.password, user.password):
            return None
        return user

    def delete_user(
        self, db_session: Session, user_id: UUID4, current_user: Users
    ) -> None:
        """
        Deletes a user and associated data.
        """
        # Authorization check:
        if current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this user",
            )

        users_repository.delete(db_session, user_id)

    def toggle_notifications(
        self,
        db_session: Session,
        user_id: UUID4,
        enable_notifications: bool,
        current_user: Users,
    ) -> None:
        """Toggles user notifications on or off."""
        # Authorization check:
        if current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this user's notifications",
            )

        users_repository.toggle_notifications(db_session, user_id, enable_notifications)
