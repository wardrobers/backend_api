# tests/integration/test_api_routes.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.schemas.users import (
    PasswordChange,
    PasswordResetConfirm,
    UserLogin,
    UsersCreate,
    UsersRead,
    UsersUpdate,
    UserInfoCreate,
    UserInfoUpdate,
    RoleCreate,
    RoleUpdate,
    UserAddressCreate,
    UserAddressUpdate,
) 
from app.models.users import Users, UserInfo, Roles, UserAddresses
from app.services.users import AuthService 
from tests.utils.users import create_random_user, create_random_user_info, create_random_role

client = TestClient(app)

# --- Helper Function to get access token ---
async def get_access_token(db_session: AsyncSession, user_data: UserLogin):
    auth_service = AuthService(db_session) 
    user = await auth_service.authenticate_user(user_data)
    if not user:
        return None
    return auth_service.create_access_token(data={"sub": user.login})

# --- Test Fixtures --- 

@pytest.fixture
async def test_user(db_session: AsyncSession) -> Users:
    return await create_random_user(db_session)

@pytest.fixture
async def test_user_info(db_session: AsyncSession, test_user: Users) -> UserInfo:
    return await create_random_user_info(db_session, test_user)

@pytest.fixture
async def test_role(db_session: AsyncSession) -> Roles:
    return await create_random_role(db_session)

@pytest.fixture
async def test_address(db_session: AsyncSession, test_user: Users) -> UserAddresses:
    address_data = UserAddressCreate(
        address_line1="123 Test St",
        city="Test City",
        country="Test Country",
        postal_code="12345",
        address_type="Both", # Or another appropriate type
    )
    address = UserAddresses(**address_data.model_dump(), user_id=test_user.id)
    db_session.add(address)
    await db_session.commit()
    await db_session.refresh(address)
    return address

@pytest.fixture
async def access_token(db_session: AsyncSession, test_user: Users):
    user_data = UserLogin(login=test_user.login, password="testpassword")
    return await get_access_token(db_session, user_data)

# --- Tests ---

@pytest.mark.asyncio
async def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Welcome to the Wardrobers API!"}

# --- User Tests ---
@pytest.mark.asyncio
async def test_register_user():
    user_data = UsersCreate(login="newuser", password="securepassword", password_confirmation="securepassword")
    response = client.post("/auth/register", json=user_data.model_dump())
    assert response.status_code == 201
    assert response.json()["login"] == "newuser"

@pytest.mark.asyncio
async def test_register_user_invalid_data():
    user_data = UsersCreate(login="", password="short", password_confirmation="short")
    response = client.post("/auth/register", json=user_data.model_dump())
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_login_user(test_user: Users):
    user_data = UserLogin(login=test_user.login, password="testpassword")
    response = client.post("/auth/login", data=user_data.model_dump())
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_user_invalid_credentials(test_user: Users):
    user_data = UserLogin(login=test_user.login, password="wrongpassword")
    response = client.post("/auth/login", data=user_data.model_dump())
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user(test_user: Users, access_token: str):
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["id"] == str(test_user.id)

@pytest.mark.asyncio
async def test_update_current_user(db_session: AsyncSession, test_user: Users, access_token: str):
    user_update = UsersUpdate(login="updateduser")
    response = client.put("/users/me", headers={"Authorization": f"Bearer {access_token}"}, json=user_update.model_dump())
    assert response.status_code == 200
    assert response.json()["login"] == "updateduser"

@pytest.mark.asyncio
async def test_update_current_user_invalid_data(access_token: str):
    user_update = UsersUpdate(login="")  # Invalid login
    response = client.put("/users/me", headers={"Authorization": f"Bearer {access_token}"}, json=user_update.model_dump())
    assert response.status_code == 422  # Expect a validation error

@pytest.mark.asyncio
async def test_delete_current_user(db_session: AsyncSession, test_user: Users, access_token: str):
    response = client.delete("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 204
    # Verify the user is soft-deleted 
    deleted_user = await Users.get_by_id(db_session, test_user.id)
    assert deleted_user.deleted_at is not None

# --- User Info Tests ---
@pytest.mark.asyncio
async def test_update_current_user_info(access_token: str):
    user_info_update = UserInfoUpdate(first_name="Updated First Name")
    response = client.put(
        "/users/me/info", 
        headers={"Authorization": f"Bearer {access_token}"}, 
        json=user_info_update.model_dump()
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated First Name"

@pytest.mark.asyncio
async def test_update_current_user_info_invalid_data(access_token: str):
    user_info_update = UserInfoUpdate(first_name="") # Invalid first name
    response = client.put(
        "/users/me/info",
        headers={"Authorization": f"Bearer {access_token}"},
        json=user_info_update.model_dump(),
    )
    assert response.status_code == 422 # Expect a validation error

# --- Role Tests ---
@pytest.mark.asyncio
async def test_get_all_roles(access_token: str):
    response = client.get("/users/roles/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_role(access_token: str):
    role_data = RoleCreate(code="test_role", name="Test Role")
    response = client.post("/users/roles/", headers={"Authorization": f"Bearer {access_token}"}, json=role_data.model_dump())
    assert response.status_code == 201
    assert response.json()["code"] == "test_role"

@pytest.mark.asyncio
async def test_get_role_by_id(test_role: Roles, access_token: str):
    response = client.get(f"/users/roles/{test_role.id}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["id"] == str(test_role.id)

@pytest.mark.asyncio
async def test_update_role(test_role: Roles, access_token: str):
    role_update = RoleUpdate(name="Updated Role Name")
    response = client.put(
        f"/users/roles/{test_role.id}", 
        headers={"Authorization": f"Bearer {access_token}"}, 
        json=role_update.model_dump()
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Role Name"

@pytest.mark.asyncio
async def test_delete_role(test_role: Roles, access_token: str):
    response = client.delete(f"/users/roles/{test_role.id}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 204

# --- User Address Tests ---
@pytest.mark.asyncio
async def test_add_user_address(access_token: str):
    address_data = UserAddressCreate(
        address_line1="456 New St",
        city="New City",
        country="New Country",
        postal_code="67890",
        address_type="Billing", # Or another type
    )
    response = client.post(
        "/users/addresses/",
        headers={"Authorization": f"Bearer {access_token}"},
        json=address_data.model_dump(),
    )
    assert response.status_code == 201
    assert response.json()["address_line1"] == "456 New St"

@pytest.mark.asyncio
async def test_get_all_user_addresses(access_token: str):
    response = client.get("/users/addresses/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert len(response.json()) == 1  # Assuming you have one test address

@pytest.mark.asyncio
async def test_update_user_address(test_address: UserAddresses, access_token: str):
    address_update = UserAddressUpdate(address_line1="Updated Address")
    response = client.put(
        f"/users/addresses/{test_address.id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=address_update.model_dump(),
    )
    assert response.status_code == 200
    assert response.json()["address_line1"] == "Updated Address"

@pytest.mark.asyncio
async def test_delete_user_address(test_address: UserAddresses, access_token: str):
    response = client.delete(
        f"/users/addresses/{test_address.id}", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 204 

# ... Add tests for other API endpoints (products, orders, subscriptions) ...