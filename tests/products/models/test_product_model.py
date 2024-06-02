# tests/products/models/test_product_model.py
import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import UUID

from app.models.pricing import PricingTier
from app.models.products.core import (
    Articles,
    ArticleStatus,
    Products,
    StockKeepingUnits,
    Variants,
)
from app.models.products.inventorization import OccasionalCategories
from app.models.products.product_details import ProductCategories
from app.models.promotions import PromotionsAndDiscounts, PromotionsVariants


@pytest.fixture
def test_product_category(session: AsyncSession):
    """Fixture to create a test product category for other tests."""
    category = ProductCategories(
        category_id=UUID("00000000-0000-0000-0000-000000000001")
    )
    session.add(category)
    session.commit()
    session.refresh(category)
    yield category


@pytest.fixture
def test_occasional_category(session: AsyncSession):
    """Fixture to create a test occasional category for other tests."""
    category = OccasionalCategories(name="Event")
    session.add(category)
    session.commit()
    session.refresh(category)
    yield category


@pytest.mark.asyncio
async def test_product_creation(session: AsyncSession):
    """Test creating a new product."""
    product = Products(name="Test Product", sku_product="SKU123")
    session.add(product)
    await session.commit()
    assert product.id is not None


@pytest.mark.asyncio
async def test_product_creation_with_category(
    session: AsyncSession, test_product_category
):
    """Test creating a product with a category."""
    product = Products(name="Test Product", sku_product="SKU123")
    product.categories.append(test_product_category)
    session.add(product)
    await session.commit()
    assert product.id is not None
    assert test_product_category in product.categories


@pytest.mark.asyncio
async def test_product_creation_with_occasional_category(
    session: AsyncSession, test_occasional_category
):
    """Test creating a product with an occasional category."""
    product = Products(name="Test Product", sku_product="SKU123")
    product.occasional_categories.append(test_occasional_category)
    session.add(product)
    await session.commit()
    assert product.id is not None
    assert test_occasional_category in product.occasional_categories


@pytest.mark.asyncio
async def test_product_creation_with_duplicate_sku(session: AsyncSession):
    """Test preventing duplicate SKU for product creation."""
    product1 = Products(name="Test Product 1", sku_product="SKU123")
    product2 = Products(name="Test Product 2", sku_product="SKU123")

    session.add(product1)
    await session.commit()

    session.add(product2)
    with pytest.raises(IntegrityError):
        await session.commit()


@pytest.mark.asyncio
async def test_get_available_products(session: AsyncSession, test_product_category):
    """Test retrieving available products."""
    sku = StockKeepingUnits(sku_product="SKU123", sku_article="SKU123-A1")
    article = Articles(
        sku_article="SKU123-A1",
        owner_type="Platform",
        condition="New",
        status_code=ArticleStatus.Available,
    )
    product = Products(name="Test Product", sku_product="SKU123")
    product.categories.append(test_product_category)
    product.sku = sku
    sku.articles.append(article)

    session.add_all([product, sku, article])
    await session.commit()

    available_products = Products.get_available_products(
        session, category=test_product_category.category_id
    )
    assert len(available_products) == 1
    assert available_products[0].id == product.id


@pytest.mark.asyncio
async def test_get_available_variants(session: AsyncSession):
    """Test retrieving available variants of a product."""
    product = Products(name="Test Product", sku_product="SKU123")
    variant = Variants(name="Variant 1", product_id=product.id)
    sku = StockKeepingUnits(sku_product="SKU123", sku_article="SKU123-A1")
    article = Articles(
        sku_article="SKU123-A1",
        owner_type="Platform",
        condition="New",
        status_code=ArticleStatus.Available,
    )
    variant.articles.append(article)
    sku.variants.append(variant)
    product.sku = sku
    product.variants.append(variant)

    session.add_all([product, sku, article, variant])
    await session.commit()

    available_variants = Products.get_available_variants(session, product.id)
    assert len(available_variants) == 1
    assert available_variants[0].id == variant.id
    assert available_variants[0].articles[0].id == article.id


@pytest.mark.asyncio
async def test_get_stock_count(session: AsyncSession):
    """Test calculating available stock for a product."""
    sku = StockKeepingUnits(sku_product="SKU123", sku_article="SKU123-A1")
    article1 = Articles(
        sku_article="SKU123-A1",
        owner_type="Platform",
        condition="New",
        status_code=ArticleStatus.Available,
    )
    article2 = Articles(
        sku_article="SKU123-A2",
        owner_type="Platform",
        condition="New",
        status_code=ArticleStatus.Available,
    )
    product = Products(name="Test Product", sku_product="SKU123")
    product.sku = sku
    sku.articles.extend([article1, article2])

    session.add_all([product, sku, article1, article2])
    await session.commit()

    stock_count = product.get_stock_count(session)
    assert stock_count == 2


@pytest.mark.asyncio
async def test_retire_product(session: AsyncSession):
    """Test retiring a product and marking associated articles as retired."""
    sku = StockKeepingUnits(sku_product="SKU123", sku_article="SKU123-A1")
    article = Articles(
        sku_article="SKU123-A1",
        owner_type="Platform",
        condition="New",
        status_code=ArticleStatus.Available,
    )
    product = Products(name="Test Product", sku_product="SKU123")
    product.sku = sku
    sku.articles.append(article)

    session.add_all([product, sku, article])
    await session.commit()

    product.retire_product(session)
    retired_article = session.query(Articles).filter(Articles.id == article.id).first()
    assert retired_article.status_code == ArticleStatus.Retired


@pytest.mark.asyncio
async def test_check_stock_and_notify(session: AsyncSession):
    """Test checking stock levels and triggering notifications (mocked)."""
    sku = StockKeepingUnits(sku_product="SKU123", sku_article="SKU123-A1")
    article = Articles(
        sku_article="SKU123-A1",
        owner_type="Platform",
        condition="New",
        status_code=ArticleStatus.Available,
    )
    product = Products(
        name="Test Product", sku_product="SKU123", low_stock_threshold=1
    )  # Set low threshold
    product.sku = sku
    sku.articles.append(article)

    session.add_all([product, sku, article])
    await session.commit()

    # Mock notification logic (would typically send an email or trigger a task)
    with pytest.raises(NotImplementedError):
        product.check_stock_and_notify()


@pytest.mark.asyncio
async def test_apply_promotions(session: AsyncSession):
    """Test applying promotions to a product."""
    # Add a product
    product = Products(name="Test Product", sku_product="SKU123")
    session.add(product)
    await session.commit()

    # Add a variant
    variant = Variants(name="Variant 1", product_id=product.id)
    session.add(variant)
    await session.commit()

    # Add a promotion
    promotion = PromotionsAndDiscounts(
        code="SUMMER10",
        discount_type="Percentage",
        discount_value=10.0,
        valid_from="2023-06-01",
        valid_to="2023-09-30",
        max_uses=10,
        uses_left=10,
    )
    session.add(promotion)
    await session.commit()

    # Link promotion to the variant
    promotion_variant = PromotionsVariants(
        variant_id=variant.id, promotion_id=promotion.id
    )
    session.add(promotion_variant)
    await session.commit()

    # Apply promotions
    total_discount = product.apply_promotions(
        session, user_id=UUID("00000000-0000-0000-0000-000000000001")
    )
    assert total_discount == 10.0

    # Check if promotion is applied to product
    product = session.query(Products).filter(Products.id == product.id).first()
    assert product.promotions_products[0].promotion_id == promotion.id


@pytest.mark.asyncio
async def test_calculate_rental_price(session: AsyncSession):
    """Test calculating the rental price of a product."""
    product = Products(name="Test Product", sku_product="SKU123")
    pricing_tier = PricingTier(retail_price=50.00)
    product.pricing_tiers.append(pricing_tier)
    session.add(product)
    await session.commit()

    rental_price = product.calculate_rental_price(session, rental_days=3)
    assert rental_price > 50.00  # Assuming price multiplier is greater than 1
    assert rental_price < 60.00  # Assuming price multiplier is less than 1.2


# Add test cases for other methods of the product model, like:
# - get_base_price
# - new_item_premium
# - get_pricing_tier
# - get_price_multiplier
# - get_category_multiplier
# - calculate_additional_costs
# - calculate_vat
# - get_occasional_category_names
