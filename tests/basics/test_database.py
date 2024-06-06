import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.products import Articles, Products, Variants
from app.models.users import UserInfo, Users


@pytest.mark.parametrize(
    "model_name",
    [
        "users",
        "user_info",
        "user_roles",
        "roles",
        "products",
        "product_categories",
        "categories",
        "brands",
        "product_types",
        "types",
        "variants",
        "stock_keeping_units",
        "articles",
        "article_status",
        "product_status",
        "sizing",
        "size_systems",
        "product_fit",
        "accessories_size",
        "colors",
        "materials",
        "product_materials",
        "product_photos",
        "occasional_categories",
        "product_occasional_categories",
        "promotions_and_discounts",
        "promotions_variants",
        "user_promotions",
        "user_saved_items",
        "user_reviews_and_ratings",
        "user_activity",
        "types_from_user",
        "cleaning_logs",
        "repair_logs",
        "subscription_periods",
        "subscription_types",
        "subscriptions",
        "order_items",
        "order_status",
        "orders",
        "transactions",
        "payment_methods",
        "revolut_details",
        "stripe_details",
        "lender_payments",
        "shipping_details",
        "delivery_options",
        "peer_to_peer_logistics",
        "role_permissions",
        "permissions",
        "data_privacy_consents",
        "categories_for_user",
        "price_factors",
        "pricing_tiers",
        "price_multipliers",
        "order_promotions",
        "order_items_promotions",
        "promotions_occasional_categories",
    ],
)
def test_database_schema_consistency(model_name):
    """Verify that each SQLAlchemy model class correctly reflects the underlying database structure."""
    engine = engine
    inspector = inspect(engine)
    db_columns = {col["name"] for col in inspector.get_columns(model_name)}
    model_columns = {
        col.name
        for col in getattr(
            __import__("app.models." + model_name.replace("_", "."), fromlist=[""]),
            model_name.title(),
        ).__table__.columns
    }
    assert (
        db_columns == model_columns
    ), f"{model_name.title()} model fields do not match with DB schema."


# --- Tests for Data Integrity and Constraints ---


@pytest.mark.asyncio
async def test_unique_user_login(db_session: AsyncSession):
    """Test the unique constraint on the Users.login field."""
    user1 = Users(login="testuser", password="testpassword")
    db_session.add(user1)
    await db_session.commit()

    user2 = Users(login="testuser", password="anotherpassword")
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        await db_session.commit()


@pytest.mark.asyncio
async def test_user_info_relationship(db_session: AsyncSession):
    """Test the one-to-one relationship between Users and UserInfo."""
    user = Users(login="testuser", password="testpassword")
    user_info = UserInfo(
        first_name="Test", last_name="User", email="test@example.com", user=user
    )
    db_session.add(user)  # No need to add user_info explicitly
    await db_session.commit()

    retrieved_user = await db_session.get(Users, user.id)
    assert retrieved_user.info is not None
    assert retrieved_user.info.email == "test@example.com"


@pytest.mark.asyncio
async def test_product_variant_article_relationship(db_session: AsyncSession):
    """Test the relationships between Products, Variants, and Articles."""
    product = Products(name="Test Product")
    variant = Variants(product=product, name="Test Variant")
    article = Articles(
        variant=variant,
        owner_type="Platform",
        condition="New",
        status_code="Available",
        # ... Other required fields for Articles ...
    )
    db_session.add(product)  # Add the product, cascading will add variant and article
    await db_session.commit()

    retrieved_product = await db_session.get(Products, product.id)
    assert retrieved_product.variants is not None
    assert retrieved_product.variants[0].articles is not None


# ... Add more data integrity tests for other models and relationships ...

# --- Tests for Data Validation within Models ---
# You can add tests here to verify that model validation (if you have any custom validation logic)
# works as expected. For example:

# @pytest.mark.asyncio
# async def test_product_name_validation(db_session: AsyncSession):
#     """Test that the product name validation prevents empty names."""
#     with pytest.raises(ValueError):
#         product = Products(name="")
