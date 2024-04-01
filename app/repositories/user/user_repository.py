from hashlib import sha256
from typing import Optional
from sqlalchemy.orm import Session
from uuid import uuid4  # Import the uuid library
from ...models.user.user_model import User  # Ensure correct import for User
from ...models.user.user_info_model import UserInfo
from ...schemas.user.user_schema import UserCreate, UserUpdate
from ...schemas.user.user_info_schema import UserInfoUpdate, UserInfoCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_uuid(self, uuid: str) -> Optional[User]:
        """Retrieve a user by their UUID."""
        return self.db.query(User).filter(User.uuid == uuid).first()

    def get_user_by_login(self, login: str) -> Optional[User]:
        """Retrieve a user by their login."""
        return self.db.query(User).filter(User.login == login).first()

    def create_user(
        self, user_data: UserCreate, user_info_data: Optional[UserInfoCreate] = None
    ) -> User:
        hashed_password = sha256(user_data.password.encode()).hexdigest()
        user_uuid = uuid4()
        new_user = User(
            uuid=user_uuid,  # Assign the generated UUID here
            login=user_data.login,
            password=hashed_password,
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update_user(self, uuid: str, user_data: UserUpdate) -> Optional[User]:
        """Update a user's details."""
        user = self.get_user_by_uuid(uuid)
        if user:
            update_data = user_data.dict(exclude_unset=True)
            # Separate user_info updates if present
            user_info_data = update_data.pop("user_info", None)
            if user_info_data:
                self.update_user_info(uuid, UserInfoUpdate(**user_info_data))
            if update_data:
                self.db.query(User).filter(User.uuid == uuid).update(update_data)
                self.db.commit()
            return self.get_user_by_uuid(uuid)
        return None

    def delete_user(self, uuid: str):
        """Delete a user by their UUID."""
        user = self.get_user_by_uuid(uuid)
        if user:
            self.db.delete(user)
            self.db.commit()

    def update_user_info(self, user_uuid: str, user_info_data: UserInfoUpdate):
        """Update a user's associated UserInfo."""
        user_info = (
            self.db.query(UserInfo).filter(UserInfo.user_uuid == user_uuid).first()
        )
        if user_info:
            for key, value in user_info_data.dict(exclude_unset=True).items():
                setattr(user_info, key, value)
            self.db.commit()

    def list_users(self, skip: int = 0, limit: int = 10) -> list[User]:
        """List users with pagination."""
        return self.db.query(User).offset(skip).limit(limit).all()
