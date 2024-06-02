# tests/products/services/test_product_service.py
from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import UUID

from app.models.products.core import Articles, Products, StockKeepingUnits, Variants
from app.models.products.product_details import ProductCategories
from app.schemas.product.category_schema import CategoryCreate
from app.schemas.product.product_schema import ProductCreate, ProductUpdate
from app.services.product_service import ProductService


@pytest.fixture
def mock_product_repository():
    """Mock product repository for testing."""
    mock_repo = MagicMock()
    mock_repo.create.return_value = Products(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        name="Test Product",
        sku_product="SKU123",
    )
    mock_repo.get_by_id.return_value = Products(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        name="Test Product",
        sku_product="SKU123",
    )
    mock_repo.get_all.return_value = [
        Products(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            name="Test Product",
            sku_product="SKU123",
        )
    ]
    mock_repo.get_by_ids.return_value = [
        Products(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            name="Test Product",
            sku_product="SKU123",
        )
    ]
    mock_repo.update.return_value = Products(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        name="Test Product",
        sku_product="SKU123",
    )
    mock_repo.soft_delete.return_value = Products(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        name="Test Product",
        sku_product="SKU123",
    )
    mock_repo.delete.return_value = None
    mock_repo.get_available_products.return_value = [
        Products(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            name="Test Product",
            sku_product="SKU123",
        )
    ]
    mock_repo.get_available_variants.return_value = [
        Variants(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            name="Variant 1",
            product_id=UUID("00000000-0000-0000-0000-000000000001"),
        )
    ]
    mock_repo.get_stock_count.return_value = 1
    mock_repo.retire_product.return_value = None
    return mock_repo


@pytest.fixture
def mock_stock_keeping_units_repository():
    """Mock StockKeepingUnits repository for testing."""
    mock_repo = MagicMock()
    mock_repo.create.return_value = StockKeepingUnits(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        sku_product="SKU123",
        sku_article="SKU123-A1",
    )
    return mock_repo


@pytest.fixture
def mock_article_repository():
    """Mock Article repository for testing."""
    mock_repo = MagicMock()
    mock_repo.create.return_value = Articles(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        sku_article="SKU123-A1",
        owner_type="Platform",
        condition="New",
    )
    return mock_repo


@pytest.fixture
def mock_variant_repository():
    """Mock Variant repository for testing."""
    mock_repo = MagicMock()
    mock_repo.create.return_value = Variants(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        name="Variant 1",
        product_id=UUID("00000000-0000-0000-0000-000000000001"),
    )
    return mock_repo


@pytest.fixture
def mock_product_category_repository():
    """Mock ProductCategory repository for testing."""
    mock_repo = MagicMock()
    mock_repo.create.return_value = ProductCategories(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        category_id=UUID("00000000-0000-0000-0000-000000000001"),
    )
    return mock_repo


@pytest.fixture
def product_service(
    mock_product_repository,
    mock_stock_keeping_units_repository,
    mock_article_repository,
    mock_variant_repository,
    mock_product_category_repository,
):
    """Fixture to create a ProductService instance for testing."""
    return ProductService(
        product_repository=mock_product_repository,
        stock_keeping_units_repository=mock_stock_keeping_units_repository,
        article_repository=mock_article_repository,
        variant_repository=mock_variant_repository,
        product_category_repository=mock_product_category_repository,
    )


def test_create_product(product_service):
    """Test creating a new product."""
    product_data = ProductCreate(name="Test Product 2", sku_product="SKU456")
    created_product = product_service.create_product(product_data)
    assert created_product.id == UUID("00000000-0000-0000-0000-000000000001")
    assert created_product.name == "Test Product 2"
    product_service.product_repository.create.assert_called_once_with(product_data)


def test_get_product_by_id(product_service):
    """Test retrieving a product by ID."""
    product_id = UUID("00000000-0000-0000-0000-000000000001")
    retrieved_product = product_service.get_product_by_id(product_id)
    assert retrieved_product.id == product_id
    product_service.product_repository.get_by_id.assert_called_once_with(product_id)


def test_get_all_products(product_service):
    """Test retrieving all products."""
    products = product_service.get_all_products()
    assert len(products) == 1
    product_service.product_repository.get_all.assert_called_once()


def test_get_products_by_ids(product_service):
    """Test retrieving products by a list of IDs."""
    product_ids = [UUID("00000000-0000-0000-0000-000000000001")]
    retrieved_products = product_service.get_products_by_ids(product_ids)
    assert len(retrieved_products) == 1
    product_service.product_repository.get_by_ids.assert_called_once_with(product_ids)


def test_update_product(product_service):
    """Test updating a product."""
    product_id = UUID("00000000-0000-0000-0000-000000000001")
    product_update = ProductUpdate(name="Updated Test Product")
    updated_product = product_service.update_product(product_id, product_update)
    assert updated_product.id == product_id
    assert updated_product.name == "Updated Test Product"
    product_service.product_repository.update.assert_called_once_with(
        product_id, product_update
    )


def test_soft_delete_product(product_service):
    """Test soft deleting a product."""
    product_id = UUID("00000000-0000-0000-0000-000000000001")
    product_service.soft_delete_product(product_id)
    product_service.product_repository.soft_delete.assert_called_once_with(product_id)


def test_delete_product(product_service):
    """Test deleting a product."""
    product_id = UUID("00000000-0000-0000-0000-000000000001")
    product_service.delete_product(product_id)
    product_service.product_repository.delete.assert_called_once_with(product_id)


def test_get_available_products(product_service):
    """Test getting available products."""
    category_id = UUID("00000000-0000-0000-0000-000000000001")
    available_products = product_service.get_available_products(category_id=category_id)
    assert len(available_products) == 1
    product_service.product_repository.get_available_products.assert_called_once_with(
        category_id
    )


def test_get_available_variants(product_service):
    """Test getting available variants for a product."""
    product_id = UUID("00000000-0000-0000-0000-000000000001")
    available_variants = product_service.get_available_variants(product_id)
    assert len(available_variants) == 1
    product_service.product_repository.get_available_variants.assert_called_once_with(
        product_id
    )


def test_get_stock_count(product_service):
    """Test getting the stock count for a product."""
    product_id = UUID("00000000-0000-0000-0000-000000000001")
    stock_count = product_service.get_stock_count(product_id)
    assert stock_count == 1
    product_service.product_repository.get_stock_count.assert_called_once_with(
        product_id
    )


def test_retire_product(product_service):
    """Test retiring a product."""
    product_id = UUID("00000000-0000-0000-0000-000000000001")
    product_service.retire_product(product_id)
    product_service.product_repository.retire_product.assert_called_once_with(
        product_id
    )


def test_create_product_with_category(product_service):
    """Test creating a product with a category."""
    product_data = ProductCreate(name="Test Product 3", sku_product="SKU789")
    category_data = CategoryCreate(name="Test Category")
    product_service.create_product_with_category(product_data, category_data)
    product_service.product_repository.create.assert_called_once_with(product_data)
    product_service.product_category_repository.create.assert_called_once_with(
        product_id=UUID("00000000-0000-0000-0000-000000000001"),
        category_id=UUID("00000000-0000-0000-0000-000000000001"),
    )
