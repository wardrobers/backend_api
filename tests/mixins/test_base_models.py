# tests/common/test_base_models.py
import pytest
from sqlalchemy import Column, String, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import UUID

from app.database.session import get_async_session
from app.models.common import Base, BaseMixin
from app.models.orders.core import OrderItems, Orders
from app.models.products.core import Articles, Products, StockKeepingUnits
from app.models.users.core import UserInfo, Users


# Mocking for testing purposes
class MockModel(Base, BaseMixin):
    __tablename__ = "mock_model"
    name = Column(String)


@pytest.mark.asyncio
async def test_base_mixin_get_by_id():
    """Test retrieving a model instance by its ID."""
    async with get_async_session() as session:
        mock_instance = MockModel(name="Test Instance")
        session.add(mock_instance)
        await session.commit()

        retrieved_instance = await MockModel.get_by_id(session, mock_instance.id)
        assert retrieved_instance.id == mock_instance.id
        assert retrieved_instance.name == "Test Instance"


@pytest.mark.asyncio
async def test_base_mixin_get_by_id_nonexistent():
    """Test retrieving a non-existent model instance by ID."""
    async with get_async_session() as session:
        retrieved_instance = await MockModel.get_by_id(
            session, UUID("00000000-0000-0000-0000-000000000001")
        )
        assert retrieved_instance is None


@pytest.mark.asyncio
async def test_base_mixin_get_all():
    """Test retrieving all instances of a model."""
    async with get_async_session() as session:
        mock_instance1 = MockModel(name="Instance 1")
        mock_instance2 = MockModel(name="Instance 2")
        session.add_all([mock_instance1, mock_instance2])
        await session.commit()

        retrieved_instances = await MockModel.get_all(session)
        assert len(retrieved_instances) == 2


@pytest.mark.asyncio
async def test_base_mixin_get_by_ids():
    """Test retrieving multiple instances by their IDs."""
    async with get_async_session() as session:
        mock_instance1 = MockModel(name="Instance 1")
        mock_instance2 = MockModel(name="Instance 2")
        session.add_all([mock_instance1, mock_instance2])
        await session.commit()

        retrieved_instances = await MockModel.get_by_ids(
            session, [mock_instance1.id, mock_instance2.id]
        )
        assert len(retrieved_instances) == 2


@pytest.mark.asyncio
async def test_base_mixin_get_by_ids_empty():
    """Test retrieving instances with an empty list of IDs."""
    async with get_async_session() as session:
        retrieved_instances = await MockModel.get_by_ids(session, [])
        assert len(retrieved_instances) == 0


@pytest.mark.asyncio
async def test_base_mixin_create():
    """Test creating a new model instance."""
    async with get_async_session() as session:
        new_instance = MockModel(name="New Instance")
        created_instance = await new_instance.create(session)
        assert created_instance.id is not None
        assert created_instance.name == "New Instance"


@pytest.mark.asyncio
async def test_base_mixin_create_empty_data():
    """Test creating a new instance with empty data."""
    async with get_async_session() as session:
        new_instance = MockModel()
        created_instance = await new_instance.create(session)
        assert created_instance.id is not None
        # No name was set, so the name attribute should be None
        assert created_instance.name is None


@pytest.mark.asyncio
async def test_base_mixin_update():
    """Test updating an existing model instance."""
    async with get_async_session() as session:
        mock_instance = MockModel(name="Original Instance")
        session.add(mock_instance)
        await session.commit()

        await mock_instance.update(session, name="Updated Instance")
        updated_instance = await MockModel.get_by_id(session, mock_instance.id)
        assert updated_instance.name == "Updated Instance"


@pytest.mark.asyncio
async def test_base_mixin_update_nonexistent():
    """Test updating a non-existent model instance."""
    async with get_async_session() as session:
        mock_instance = MockModel(
            id=UUID("00000000-0000-0000-0000-000000000001"), name="Original Instance"
        )
        await mock_instance.update(session, name="Updated Instance")
        # No exception raised, update should just do nothing
        updated_instance = await MockModel.get_by_id(session, mock_instance.id)
        assert updated_instance is None


@pytest.mark.asyncio
async def test_base_mixin_soft_delete():
    """Test soft deleting a model instance."""
    async with get_async_session() as session:
        mock_instance = MockModel(name="Test Instance")
        session.add(mock_instance)
        await session.commit()

        await mock_instance.soft_delete(session)
        deleted_instance = await MockModel.get_by_id(session, mock_instance.id)
        assert deleted_instance.deleted_at is not None


@pytest.mark.asyncio
async def test_base_mixin_soft_delete_already_deleted():
    """Test soft deleting a model instance that is already soft deleted."""
    async with get_async_session() as session:
        mock_instance = MockModel(name="Test Instance", deleted_at=func.now())
        session.add(mock_instance)
        await session.commit()

        await mock_instance.soft_delete(session)
        deleted_instance = await MockModel.get_by_id(session, mock_instance.id)
        # The deleted_at timestamp should remain the same
        assert deleted_instance.deleted_at == mock_instance.deleted_at


@pytest.mark.asyncio
async def test_base_mixin_delete():
    """Test permanently deleting a model instance."""
    async with get_async_session() as session:
        mock_instance = MockModel(name="Test Instance")
        session.add(mock_instance)
        await session.commit()

        await mock_instance.delete(session)
        deleted_instance = await MockModel.get_by_id(session, mock_instance.id)
        assert deleted_instance is None


@pytest.mark.asyncio
async def test_base_mixin_delete_already_deleted():
    """Test permanently deleting a model instance that is already soft deleted."""
    async with get_async_session() as session:
        mock_instance = MockModel(name="Test Instance", deleted_at=func.now())
        session.add(mock_instance)
        await session.commit()

        await mock_instance.delete(session)
        deleted_instance = await MockModel.get_by_id(session, mock_instance.id)
        assert deleted_instance is None


# Test cases for filtering, pagination, and other base mixin methods can be added here.


# Specific model tests for Users, UserInfo, Products, StockKeepingUnits, Articles, Orders, etc.
@pytest.mark.asyncio
async def test_user_creation_with_info(session: AsyncSession):
    """Test creating a new Users with associated UserInfo."""
    user = Users(login="testuser", password="securepassword")
    user_info = UserInfo(
        first_name="Test", last_name="Users", email="test@wardrobers.com"
    )
    user.info = user_info  # Set relationship
    session.add(user)
    await session.commit()

    assert user.id is not None
    assert user.info.id is not None


@pytest.mark.asyncio
async def test_user_creation_with_duplicate_email(session: AsyncSession):
    """Test preventing duplicate email for Users creation."""
    user1 = Users(login="user1", password="securepassword")
    user1.info = UserInfo(
        first_name="Users 1", last_name="Test", email="test@wardrobers.com"
    )
    user2 = Users(login="user2", password="securepassword")
    user2.info = UserInfo(
        first_name="Users 2", last_name="Test", email="test@wardrobers.com"
    )

    session.add(user1)
    await session.commit()

    session.add(user2)
    with pytest.raises(IntegrityError):
        await session.commit()


@pytest.mark.asyncio
async def test_product_creation_with_stock_and_article(session: AsyncSession):
    """Test creating a Product with associated StockKeepingUnits and Articles."""
    sku = StockKeepingUnits(sku_name="SKU123", free_articles_count=1)
    article = Articles(
        sku_id=sku.id, owner_type="Platform", condition="New", status_code="Available"
    )
    product = Products(
        name="Test Product",
        brand_id=UUID("00000000-0000-0000-0000-000000000001"),
        clothing_size_id=UUID("00000000-0000-0000-0000-000000000001"),
        size_and_fit_id=UUID("00000000-0000-0000-0000-000000000001"),
        status_code="Available",
        accessories_size_id=UUID("00000000-0000-0000-0000-000000000001"),
    )
    sku.variants.append(article)  # Set relationship
    product.variants.append(article)

    session.add_all([product, sku, article])
    await session.commit()

    assert product.id is not None
    assert sku.id is not None
    assert article.id is not None


@pytest.mark.asyncio
async def test_order_creation_with_order_items(session: AsyncSession):
    """Test creating an Orders with associated OrderItems."""
    product = Products(
        name="Test Product", sku_product="SKU123"
    )  # Add a Product for testing
    session.add(product)
    await session.commit()

    user = Users(login="testuser", password="securepassword")
    session.add(user)
    await session.commit()

    order = Orders(user_id=user.id, total_price=100.00)
    order_item = OrderItems(
        order_id=order.id,
        article_id=UUID("00000000-0000-0000-0000-000000000001"),
        price=50.00,
    )
    order.order_items.append(order_item)  # Set relationship

    session.add_all([order, order_item])
    await session.commit()

    assert order.id is not None
    assert order_item.id is not None
