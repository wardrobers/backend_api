import pytest
from sqlalchemy import inspect
from app.database.session import engine


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
