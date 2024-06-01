# tests/orders/services/test_order_processing_service.py
import pytest
from unittest.mock import MagicMock
from sqlalchemy import UUID, func
from datetime import timedelta

from app.services.order_processing_service import OrderProcessingService
from app.models.orders.core import Order, OrderStatus, OrderItems
from app.models.orders.payments import Transactions
from app.schemas.order.order_schema import OrderCreate, OrderRead, OrderUpdate
from app.schemas.order.order_status_schema import OrderStatusCreate, OrderStatusRead


@pytest.fixture
def mock_order_repository():
    """Mock order repository for testing."""
    mock_repo = MagicMock()
    mock_repo.create.return_value = Order(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        user_id=UUID("00000000-0000-0000-0000-000000000001"),
        total_price=100.00,
        status_code=OrderStatus.Placed,
    )
    mock_repo.get_by_id.return_value = Order(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        user_id=UUID("00000000-0000-0000-0000-000000000001"),
        total_price=100.00,
        status_code=OrderStatus.Placed,
    )
    mock_repo.get_all.return_value = [
        Order(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            user_id=UUID("00000000-0000-0000-0000-000000000001"),
            total_price=100.00,
            status_code=OrderStatus.Placed,
        )
    ]
    mock_repo.get_by_ids.return_value = [
        Order(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            user_id=UUID("00000000-0000-0000-0000-000000000001"),
            total_price=100.00,
            status_code=OrderStatus.Placed,
        )
    ]
    mock_repo.update.return_value = Order(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        user_id=UUID("00000000-0000-0000-0000-000000000001"),
        total_price=100.00,
        status_code=OrderStatus.Placed,
    )
    mock_repo.soft_delete.return_value = Order(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        user_id=UUID("00000000-0000-0000-0000-000000000001"),
        total_price=100.00,
        status_code=OrderStatus.Placed,
    )
    mock_repo.delete.return_value = None
    mock_repo.update_status.return_value = Order(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        user_id=UUID("00000000-0000-0000-0000-000000000001"),
        total_price=100.00,
        status_code=OrderStatus.Confirmed,
    )
    mock_repo.mark_as_complete.return_value = Order(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        user_id=UUID("00000000-0000-0000-0000-000000000001"),
        total_price=100.00,
        status_code=OrderStatus.Delivered,
    )
    mock_repo.cancel_order.return_value = Order(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        user_id=UUID("00000000-0000-0000-0000-000000000001"),
        total_price=100.00,
        status_code=OrderStatus.Cancelled,
    )
    mock_repo.return_order.return_value = Order(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        user_id=UUID("00000000-0000-0000-0000-000000000001"),
        total_price=100.00,
        status_code=OrderStatus.Returned,
    )
    return mock_repo


@pytest.fixture
def mock_order_items_repository():
    """Mock order items repository for testing."""
    mock_repo = MagicMock()
    mock_repo.create.return_value = OrderItems(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        order_id=UUID("00000000-0000-0000-0000-000000000001"),
        article_id=UUID("00000000-0000-0000-0000-000000000001"),
        price=50.00,
    )
    return mock_repo


@pytest.fixture
def mock_transaction_repository():
    """Mock transaction repository for testing."""
    mock_repo = MagicMock()
    mock_repo.create.return_value = Transactions(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        order_id=UUID("00000000-0000-0000-0000-000000000001"),
        amount=100.00,
        currency="USD",
    )
    return mock_repo


@pytest.fixture
def order_processing_service(
    mock_order_repository, mock_order_items_repository, mock_transaction_repository
):
    """Fixture to create an OrderProcessingService instance for testing."""
    return OrderProcessingService(
        order_repository=mock_order_repository,
        order_items_repository=mock_order_items_repository,
        transaction_repository=mock_transaction_repository,
    )


def test_create_order(order_processing_service):
    """Test creating a new order."""
    order_data = OrderCreate(
        user_id=UUID("00000000-0000-0000-0000-000000000001"), total_price=100.00
    )
    created_order = order_processing_service.create_order(order_data)
    assert created_order.id == UUID("00000000-0000-0000-0000-000000000001")
    assert created_order.user_id == UUID("00000000-0000-0000-0000-000000000001")
    order_processing_service.order_repository.create.assert_called_once_with(order_data)


def test_get_order_by_id(order_processing_service):
    """Test retrieving an order by ID."""
    order_id = UUID("00000000-0000-0000-0000-000000000001")
    retrieved_order = order_processing_service.get_order_by_id(order_id)
    assert retrieved_order.id == order_id
    order_processing_service.order_repository.get_by_id.assert_called_once_with(
        order_id
    )


def test_get_all_orders(order_processing_service):
    """Test retrieving all orders."""
    orders = order_processing_service.get_all_orders()
    assert len(orders) == 1
    order_processing_service.order_repository.get_all.assert_called_once()


def test_get_orders_by_ids(order_processing_service):
    """Test retrieving orders by a list of IDs."""
    order_ids = [UUID("00000000-0000-0000-0000-000000000001")]
    retrieved_orders = order_processing_service.get_orders_by_ids(order_ids)
    assert len(retrieved_orders) == 1
    order_processing_service.order_repository.get_by_ids.assert_called_once_with(
        order_ids
    )


def test_update_order(order_processing_service):
    """Test updating an order."""
    order_id = UUID("00000000-0000-0000-0000-000000000001")
    order_update = OrderUpdate(total_price=150.00)
    updated_order = order_processing_service.update_order(order_id, order_update)
    assert updated_order.id == order_id
    assert updated_order.total_price == 150.00
    order_processing_service.order_repository.update.assert_called_once_with(
        order_id, order_update
    )


def test_soft_delete_order(order_processing_service):
    """Test soft deleting an order."""
    order_id = UUID("00000000-0000-0000-0000-000000000001")
    order_processing_service.soft_delete_order(order_id)
    order_processing_service.order_repository.soft_delete.assert_called_once_with(
        order_id
    )


def test_delete_order(order_processing_service):
    """Test deleting an order."""
    order_id = UUID("00000000-0000-0000-0000-000000000001")
    order_processing_service.delete_order(order_id)
    order_processing_service.order_repository.delete.assert_called_once_with(order_id)


def test_update_order_status(order_processing_service):
    """Test updating the status of an order."""
    order_id = UUID("00000000-0000-0000-0000-000000000001")
    status_data = OrderStatusCreate(code="Confirmed", name="Confirmed")
    order_processing_service.update_order_status(order_id, status_data)
    order_processing_service.order_repository.update_status.assert_called_once_with(
        order_id, status_data
    )


def test_mark_order_as_complete(order_processing_service):
    """Test marking an order as complete."""
    order_id = UUID("00000000-0000-0000-0000-000000000001")
    order_processing_service.mark_order_as_complete(order_id)
    order_processing_service.order_repository.mark_as_complete.assert_called_once_with(
        order_id
    )


def test_cancel_order(order_processing_service):
    """Test cancelling an order."""
    order_id = UUID("00000000-0000-0000-0000-000000000001")
    order_processing_service.cancel_order(order_id)
    order_processing_service.order_repository.cancel_order.assert_called_once_with(
        order_id
    )


def test_return_order(order_processing_service):
    """Test returning an order."""
    order_id = UUID("00000000-0000-0000-0000-000000000001")
    order_processing_service.return_order(order_id)
    order_processing_service.order_repository.return_order.assert_called_once_with(
        order_id
    )


def test_create_order_item(order_processing_service):
    """Test creating a new order item."""
    order_id = UUID("00000000-0000-0000-0000-000000000001")
    article_id = UUID("00000000-0000-0000-0000-000000000001")
    start_date = func.now()
    end_date = start_date + timedelta(days=7)
    order_processing_service.create_order_item(
        order_id, article_id, start_date, end_date
    )
    order_processing_service.order_items_repository.create.assert_called_once_with(
        order_id=order_id,
        article_id=article_id,
        start_date=start_date,
        end_date=end_date,
    )


def test_create_transaction(order_processing_service):
    """Test creating a new transaction for an order."""
    order_id = UUID("00000000-0000-0000-0000-000000000001")
    amount = 100.00
    currency = "USD"
    order_processing_service.create_transaction(order_id, amount, currency)
    order_processing_service.transaction_repository.create.assert_called_once_with(
        order_id=order_id, amount=amount, currency=currency
    )
