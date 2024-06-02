# tests/orders/models/test_order_model.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import UUID

from app.models.orders import Order, OrderItems, OrderStatus
from app.models.orders.payments import Transactions
from app.models.products import Products
from app.models.users import User


@pytest.fixture
def test_product(session: AsyncSession):
    """Fixture to create a test product for other tests."""
    product = Products(name="Test Product", sku_product="SKU123")
    session.add(product)
    session.commit()
    session.refresh(product)
    yield product


@pytest.fixture
def test_user(session: AsyncSession):
    """Fixture to create a test user for other tests."""
    user = User(login="testuser", password="securepassword")
    session.add(user)
    session.commit()
    session.refresh(user)
    yield user


@pytest.mark.asyncio
async def test_order_creation(
    session: AsyncSession, test_product: Products, test_user: User
):
    """Test creating a new order."""
    order = Order(
        user_id=test_user.id, total_price=100.00, status_code=OrderStatus.Placed
    )
    session.add(order)
    await session.commit()
    assert order.id is not None


@pytest.mark.asyncio
async def test_order_creation_with_order_items(
    session: AsyncSession, test_product: Products, test_user: User
):
    """Test creating an order with associated order items."""
    order = Order(
        user_id=test_user.id, total_price=100.00, status_code=OrderStatus.Placed
    )
    order_item = OrderItems(
        order_id=order.id,
        article_id=UUID("00000000-0000-0000-0000-000000000001"),
        price=50.00,
    )
    order.order_items.append(order_item)
    session.add_all([order, order_item])
    await session.commit()
    assert order.id is not None
    assert order_item.id is not None


@pytest.mark.asyncio
async def test_order_creation_with_transaction(
    session: AsyncSession, test_product: Products, test_user: User
):
    """Test creating an order with associated transaction."""
    order = Order(
        user_id=test_user.id, total_price=100.00, status_code=OrderStatus.Placed
    )
    transaction = Transactions(order_id=order.id, amount=100.00, currency="USD")
    order.transactions.append(transaction)
    session.add_all([order, transaction])
    await session.commit()
    assert order.id is not None
    assert transaction.id is not None


@pytest.mark.asyncio
async def test_calculate_total_price(
    session: AsyncSession, test_product: Products, test_user: User
):
    """Test calculating the total price of an order item, including discounts."""
    order = Order(
        user_id=test_user.id, total_price=100.00, status_code=OrderStatus.Placed
    )
    order_item = OrderItems(
        order_id=order.id,
        article_id=UUID("00000000-0000-0000-0000-000000000001"),
        price=50.00,
    )
    session.add_all([order, order_item])
    await session.commit()

    # No discounts initially
    total_price = order_item.calculate_total_price()
    assert total_price == 50.00


# Add test cases for:
# - Preventing duplicate order creation (e.g., same order items for the same user)
# - Updating order status
# - Marking an order as complete
# - Cancelling an order
# - Returning an order
# - Tests for other Order model methods like get_items, get_total_price, etc.
