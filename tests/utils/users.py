# tests/utils/users.py
import random
import string

from sqlalchemy.orm import Session

from app.models.users import Roles, UserInfo, Users
from app.repositories.users import AuthRepository


def create_random_user(db_session: Session, login_length: int = 10) -> Users:
    """
    Creates a random user with a hashed password in the database.

    Args:
        db_session (Session): The database session.
        login_length (int, optional): Length of the random login to generate. Defaults to 10.

    Returns:
        Users: The created Users object.
    """
    random_login = "".join(random.choices(string.ascii_letters, k=login_length))
    hashed_password = AuthRepository.get_password_hash("testpassword")
    user = Users(login=random_login, password=hashed_password)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def create_random_user_info(
    db_session: Session,
    user: Users,
    first_name_length: int = 8,
    last_name_length: int = 10,
) -> UserInfo:
    """
    Creates random user info associated with a given user.

    Args:
        db_session (Session): The database session.
        user (Users): The user to associate the info with.
        first_name_length (int, optional): Length of the random first name. Defaults to 8.
        last_name_length (int, optional): Length of the random last name. Defaults to 10.

    Returns:
        UserInfo: The created UserInfo object.
    """
    random_first_name = "".join(
        random.choices(string.ascii_letters, k=first_name_length)
    )
    random_last_name = "".join(random.choices(string.ascii_letters, k=last_name_length))
    user_info = UserInfo(
        first_name=random_first_name,
        last_name=random_last_name,
        phone_number="1234567890",  # You can randomize this as needed
        email=f"{random_first_name}.{random_last_name}@example.com",
        user_id=user.id,
    )
    db_session.add(user_info)
    db_session.commit()
    db_session.refresh(user_info)
    return user_info


def create_random_role(
    db_session: Session, code_length: int = 6, name_length: int = 12
) -> Roles:
    """
    Creates a random role in the database.

    Args:
        db_session (Session): The database session.
        code_length (int, optional): Length of the random role code. Defaults to 6.
        name_length (int, optional): Length of the random role name. Defaults to 12.

    Returns:
        Roles: The created Roles object.
    """
    random_code = "".join(random.choices(string.ascii_lowercase, k=code_length))
    random_name = "".join(
        random.choices(string.ascii_letters + string.whitespace, k=name_length)
    )
    role = Roles(code=random_code, name=random_name)
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)
    return role
