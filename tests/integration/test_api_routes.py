# tests/integration/test_api_routes.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import UUID

from app.main import app

client = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Welcome to the Wardrobers API!"}


@pytest.mark.asyncio
async def test_create_user(test_user: UserRead):
    """Test creating a new user through API."""
    user_data = UserCreate(login="testuser2", password="securepassword")
    response = client.post("/users/register", json=user_data.dict())
    assert response.status_code == 201
    assert response.json()["login"] == "testuser2"


@pytest.mark.asyncio
async def test_create_user_invalid_data(test_user: UserRead):
    """Test creating a new user with invalid data through API."""
    user_data = UserCreate(login="", password="securepassword")
    response = client.post("/users/register", json=user_data.dict())
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_user_by_id(test_user: UserRead):
    """Test retrieving a user by ID through API."""
    response = client.get(f"/users/{test_user.uuid}")
    assert response.status_code == 200
    assert response.json()["login"] == "testuser"


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(test_user: UserRead):
    """Test retrieving a non-existent user by ID through API."""
    response = client.get("/users/00000000-0000-0000-0000-000000000002")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user(test_user: UserRead):
    """Test updating a user through API."""
    user_update = UserUpdate(login="updatedtestuser")
    response = client.put(f"/users/{test_user.uuid}", json=user_update.dict())
    assert response.status_code == 200
    assert response.json()["login"] == "updatedtestuser"


@pytest.mark.asyncio
async def test_update_user_invalid_data(test_user: UserRead):
    """Test updating a user with invalid data through API."""
    user_update = UserUpdate(login="")
    response = client.put(f"/users/{test_user.uuid}", json=user_update.dict())
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_soft_delete_user(test_user: UserRead):
    """Test soft deleting a user through API."""
    response = client.delete(f"/users/{test_user.uuid}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_user(test_user: UserRead):
    """Test deleting a user through API."""
    response = client.delete(
        f"/users/{test_user.uuid}", json=UserDelete(uuid=test_user.uuid).dict()
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_create_order(test_user: UserRead, test_product: ProductRead):
    """Test creating a new order through API."""
    order_data = OrderCreate(user_id=test_user.uuid, total_price=100.00)
    response = client.post("/orders", json=order_data.dict())
    assert response.status_code == 201
    assert response.json()["total_price"] == 100.00


@pytest.mark.asyncio
async def test_create_order_invalid_data(
    test_user: UserRead, test_product: ProductRead
):
    """Test creating a new order with invalid data through API."""
    order_data = OrderCreate(user_id=test_user.uuid, total_price=-100.00)
    response = client.post("/orders", json=order_data.dict())
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_order_by_id(test_order: OrderRead):
    """Test retrieving an order by ID through API."""
    response = client.get(f"/orders/{test_order.uuid}")
    assert response.status_code == 200
    assert response.json()["total_price"] == 100.00


@pytest.mark.asyncio
async def test_get_order_by_id_not_found(test_order: OrderRead):
    """Test retrieving a non-existent order by ID through API."""
    response = client.get("/orders/00000000-0000-0000-0000-000000000002")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_product(test_category: CategoryRead, test_brand: BrandRead):
    """Test creating a new product through API."""
    product_data = ProductCreate(
        name="Test Product 2",
        sku_product="SKU456",
        status_code="Available",
        products_catalog_id=UUID("00000000-0000-0000-0000-000000000001"),
        color_id=UUID("00000000-0000-0000-0000-000000000001"),
        size_id=UUID("00000000-0000-0000-0000-000000000001"),
        base_price=50.00,
    )
    response = client.post("/products", json=product_data.dict())
    assert response.status_code == 201
    assert response.json()["name"] == "Test Product 2"


@pytest.mark.asyncio
async def test_create_product_with_category(test_brand: BrandRead):
    """Test creating a new product with a category through API."""
    category_data = CategoryCreate(name="Test Category 2")
    response = client.post("/categories", json=category_data.dict())
    assert response.status_code == 201
    category_id = response.json()["uuid"]

    product_data = ProductCreate(
        name="Test Product 3",
        sku_product="SKU789",
        status_code="Available",
        products_catalog_id=UUID("00000000-0000-0000-0000-000000000002"),
        color_id=UUID("00000000-0000-0000-0000-000000000002"),
        size_id=UUID("00000000-0000-0000-0000-000000000002"),
        base_price=60.00,
    )
    response = client.post("/products", json=product_data.dict())
    assert response.status_code == 201
    product_id = response.json()["uuid"]

    product_category_data = ProductCategoryCreate(
        products_catalog_id=product_id, category_id=category_id
    )
    response = client.post("/products/categories", json=product_category_data.dict())
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_product_with_materials(
    test_category: CategoryRead, test_brand: BrandRead
):
    """Test creating a new product with materials through API."""
    product_data = ProductCreate(
        name="Test Product 4",
        sku_product="SKU1011",
        status_code="Available",
        products_catalog_id=UUID("00000000-0000-0000-0000-000000000003"),
        color_id=UUID("00000000-0000-0000-0000-000000000003"),
        size_id=UUID("00000000-0000-0000-0000-000000000003"),
        base_price=70.00,
    )
    response = client.post("/products", json=product_data.dict())
    assert response.status_code == 201
    product_id = response.json()["uuid"]

    material_data = ProductMaterialCreate(
        product_id=product_id,
        material_id=UUID("00000000-0000-0000-0000-000000000001"),
        percent=100,
    )
    response = client.post("/products/materials", json=material_data.dict())
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_product_invalid_data(
    test_category: CategoryRead, test_brand: BrandRead
):
    """Test creating a new product with invalid data through API."""
    product_data = ProductCreate(
        name="",
        sku_product="SKU1011",
        status_code="Available",
        products_catalog_id=UUID("00000000-0000-0000-0000-000000000004"),
        color_id=UUID("00000000-0000-0000-0000-000000000004"),
        size_id=UUID("00000000-0000-0000-0000-000000000004"),
        base_price=70.00,
    )
    response = client.post("/products", json=product_data.dict())
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_product_by_id(test_product: ProductRead):
    """Test retrieving a product by ID through API."""
    response = client.get(f"/products/{test_product.uuid}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"


@pytest.mark.asyncio
async def test_get_product_by_id_not_found(test_product: ProductRead):
    """Test retrieving a non-existent product by ID through API."""
    response = client.get("/products/00000000-0000-0000-0000-000000000002")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_category(test_product: ProductRead):
    """Test creating a new category through API."""
    category_data = CategoryCreate(name="Test Category 3")
    response = client.post("/categories", json=category_data.dict())
    assert response.status_code == 201
    assert response.json()["name"] == "Test Category 3"


@pytest.mark.asyncio
async def test_create_category_invalid_data(test_product: ProductRead):
    """Test creating a new category with invalid data through API."""
    category_data = CategoryCreate(name="")
    response = client.post("/categories", json=category_data.dict())
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_brand(test_product: ProductRead):
    """Test creating a new brand through API."""
    brand_data = BrandCreate(name="Test Brand 1")
    response = client.post("/brands", json=brand_data.dict())
    assert response.status_code == 201
    assert response.json()["name"] == "Test Brand 1"


@pytest.mark.asyncio
async def test_create_brand_invalid_data(test_product: ProductRead):
    """Test creating a new brand with invalid data through API."""
    brand_data = BrandCreate(name="")
    response = client.post("/brands", json=brand_data.dict())
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_color(test_product: ProductRead):
    """Test creating a new color through API."""
    color_data = ColorCreate(color="Red")
    response = client.post("/colors", json=color_data.dict())
    assert response.status_code == 201
    assert response.json()["color"] == "Red"


@pytest.mark.asyncio
async def test_create_color_invalid_data(test_product: ProductRead):
    """Test creating a new color with invalid data through API."""
    color_data = ColorCreate(color="")
    response = client.post("/colors", json=color_data.dict())
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_size(test_product: ProductRead):
    """Test creating a new size through API."""
    size_data = SizeCreate(
        back_length=10.0,
        sleeve_length=20.0,
        leg_length=30.0,
        size_eu_code="S",
        size_uk_code="S",
        size_us_code="S",
        size_it_code="S",
    )
    response = client.post("/sizes", json=size_data.dict())
    assert response.status_code == 201
    assert response.json()["back_length"] == 10.0


@pytest.mark.asyncio
async def test_create_size_invalid_data(test_product: ProductRead):
    """Test creating a new size with invalid data through API."""
    size_data = SizeCreate(
        back_length=-10.0,
        sleeve_length=20.0,
        leg_length=30.0,
        size_eu_code="S",
        size_uk_code="S",
        size_us_code="S",
        size_it_code="S",
    )
    response = client.post("/sizes", json=size_data.dict())
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_product_type(test_product: ProductRead):
    """Test creating a new product type through API."""
    product_type_data = ProductTypeCreate(name="T-shirt")
    response = client.post("/product_types", json=product_type_data.dict())
    assert response.status_code == 201
    assert response.json()["name"] == "T-shirt"


@pytest.mark.asyncio
async def test_create_product_type_invalid_data(test_product: ProductRead):
    """Test creating a new product type with invalid data through API."""
    product_type_data = ProductTypeCreate(name="")
    response = client.post("/product_types", json=product_type_data.dict())
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_rental_period(test_product: ProductRead):
    """Test creating a new rental period through API."""
    rental_period_data = RentalPeriodCreate(name="One Week")
    response = client.post("/rental_periods", json=rental_period_data.dict())
    assert response.status_code == 201
    assert response.json()["name"] == "One Week"


@pytest.mark.asyncio
async def test_create_rental_period_invalid_data(test_product: ProductRead):
    """Test creating a new rental period with invalid data through API."""
    rental_period_data = RentalPeriodCreate(name="")
    response = client.post("/rental_periods", json=rental_period_data.dict())
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_price(
    test_product: ProductRead, test_rental_period: RentalPeriodRead
):
    """Test creating a new price for a product through API."""
    price_data = PriceCreate(
        product_id=test_product.uuid,
        time_period_id=test_rental_period.uuid,
        time_value=7,
        price=50.00,
    )
    response = client.post("/prices", json=price_data.dict())
    assert response.status_code == 201
    assert response.json()["price"] == 50.00


@pytest.mark.asyncio
async def test_create_price_invalid_data(
    test_product: ProductRead, test_rental_period: RentalPeriodRead
):
    """Test creating a new price for a product with invalid data through API."""
    price_data = PriceCreate(
        product_id=test_product.uuid,
        time_period_id=test_rental_period.uuid,
        time_value=-7,
        price=50.00,
    )
    response = client.post("/prices", json=price_data.dict())
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_product_photo(test_product: ProductRead):
    """Test creating a new product photo through API."""
    product_photo_data = ProductPhotoCreate(
        product_id=test_product.uuid,
        showcase=False,
    )
    response = client.post("/products/photos", json=product_photo_data.dict())
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_product_photo_invalid_data(test_product: ProductRead):
    """Test creating a new product photo with invalid data through API."""
    product_photo_data = ProductPhotoCreate(
        product_id=test_product.uuid,
        showcase="invalid",
    )
    response = client.post("/products/photos", json=product_photo_data.dict())
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_user_info(test_user: UserRead):
    """Test creating user info for a user through API."""
    user_info_data = UserInfoCreate(
        name="Test",
        surname="Users",
        email="test@example.com",
    )
    response = client.post(f"/users/{test_user.uuid}/info", json=user_info_data.dict())
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_user_info_invalid_data(test_user: UserRead):
    """Test creating user info with invalid data through API."""
    user_info_data = UserInfoCreate(
        name="",
        surname="Users",
        email="test@example.com",
    )
    response = client.post(f"/users/{test_user.uuid}/info", json=user_info_data.dict())
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_update_user_info(test_user: UserRead):
    """Test updating user info for a user through API."""
    user_info_update = UserInfoBase(
        name="Updated Test",
        surname="Updated Users",
    )
    response = client.put(f"/users/{test_user.uuid}/info", json=user_info_update.dict())
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Test"


@pytest.mark.asyncio
async def test_update_user_info_invalid_data(test_user: UserRead):
    """Test updating user info with invalid data through API."""
    user_info_update = UserInfoBase(
        name="",
        surname="Users",
    )
    response = client.put(f"/users/{test_user.uuid}/info", json=user_info_update.dict())
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_subscription(test_user: UserRead):
    """Test creating a subscription for a user through API."""
    subscription_data = SubscriptionCreate(
        user_id=test_user.uuid,
        subscription_type_id=UUID("00000000-0000-0000-0000-000000000001"),
        subscription_start="2023-06-01T00:00:00",
        subscription_finish="2023-07-01T00:00:00",
        count_free_orders=10,
        count_orders_available_by_subscription=20,
        count_orders_closed_by_subscription=0,
    )
    response = client.post(
        f"/users/{test_user.uuid}/subscriptions", json=subscription_data.dict()
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_subscription_invalid_data(test_user: UserRead):
    """Test creating a subscription for a user with invalid data through API."""
    subscription_data = SubscriptionCreate(
        user_id=test_user.uuid,
        subscription_type_id=UUID("00000000-0000-0000-0000-000000000001"),
        subscription_start="2023-07-01T00:00:00",
        subscription_finish="2023-06-01T00:00:00",
        count_free_orders=10,
        count_orders_available_by_subscription=20,
        count_orders_closed_by_subscription=0,
    )
    response = client.post(
        f"/users/{test_user.uuid}/subscriptions", json=subscription_data.dict()
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_user_activity(test_user: UserRead):
    """Test retrieving user activity through API."""
    response = client.get(f"/users/{test_user.uuid}/activity")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "total_confirmed_orders" in response.json()


@pytest.mark.asyncio
async def test_get_user_activity_not_found(test_user: UserRead):
    """Test retrieving user activity that does not exist through API."""
    response = client.get("/users/00000000-0000-0000-0000-000000000002/activity")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_category_for_user(test_user: UserRead):
    """Test creating a category for a user through API."""
    category_for_user_data = CategoryForUserCreate(
        user_id=test_user.uuid,
        category_id=UUID("00000000-0000-0000-0000-000000000001"),
    )
    response = client.post(
        f"/users/{test_user.uuid}/categories", json=category_for_user_data.dict()
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_category_for_user_invalid_data(test_user: UserRead):
    """Test creating a category for a user with invalid data through API."""
    category_for_user_data = CategoryForUserCreate(
        user_id=test_user.uuid,
        category_id="invalid_uuid",
    )
    response = client.post(
        f"/users/{test_user.uuid}/categories", json=category_for_user_data.dict()
    )
    assert response.status_code == 400


# Add test cases for other endpoints and their edge cases, focusing on:
# - Invalid input handling (empty values, wrong data types, etc.)
# - Error handling (404 Not Found, 400 Bad Request, 500 Internal Server Error, etc.)
# - Concurrency testing (for endpoints with potential race conditions or database conflicts)

# Integration Tests for:
# - Authenticated routes (token validation, permissions)
# - Database interactions (data consistency, relationship integrity)
# - Complex scenarios (e.g., ordering a product, managing subscriptions)
