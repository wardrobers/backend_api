from enum import Enum, auto
from sqlalchemy import Column, ForeignKey, String, Text, func, and_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship, joinedload, selectinload, Session

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)
from app.models.products import ProductCategories, StockKeepingUnit, Article, ArticleStatus, ProductStatus, Variants
from app.models.users import User
from app.models.promotions import UserPromotions, PromotionsAndDiscounts, PromotionsProducts
from app.models.pricing import PriceFactors, PricingTier, PriceMultipliers


class FilterKeys(Enum):
    category_id = auto()
    size_id = auto()
    brand_id = auto()
    material_id = auto()
    color_id = auto()
    price_range = auto()
    available_dates = auto()


class Product(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "products"

    sku_product = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    instructions = Column(String)

    # Foreign Keys
    sku_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("stock_keeping_unit.id"), nullable=False
    )
    brand_id = mapped_column(UUID(as_uuid=True), ForeignKey("brands.id"))
    clothing_size_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("clothing_sizes.id")
    )
    clasp_type_id = mapped_column(UUID(as_uuid=True), ForeignKey("clasp_types.id"))
    product_fit_id = mapped_column(UUID(as_uuid=True), ForeignKey("product_fit.id"))
    status_code = mapped_column(String, ForeignKey("product_status.code"))

    # Relationships
    types = relationship("ProductTypes", backref="products")
    photos = relationship("ProductPhotos", backref="products")
    variants = relationship("Variants", backref="products")
    user_reviews_and_ratings = relationship("UserReviewsAndRatings", backref="products")
    categories = relationship("ProductCategories", backref="products")
    promotions_products = relationship("PromotionsProducts", backref="products")
    pricing_tiers = relationship("PricingTier", backref="products")
    accessory_size = relationship("AccessoriesSize", backref="products")

    def __repr__(self):
        return f"<Product(uuid={self.id}, name='{self.name}', sku_product='{self.sku_product}')>"
    
    @classmethod
    def get_available_products(cls, db_session: Session, category=None, brand=None):
        """
        Retrieves products with available articles based on filters.
        Optimized to use EXISTS clause to check for stock directly in the query.
        """
        # Subquery for checking available articles
        article_subquery = (
            db_session.query(Article.id)
            .join(StockKeepingUnit, StockKeepingUnit.sku_product == Article.sku_article)
            .filter(Article.status_code == ArticleStatus.Available)
            .exists()
        )

        query = db_session.query(cls).options(selectinload(cls.variants))
        if category:
            query = query.join(ProductCategories).filter(ProductCategories.category_id == category)
        if brand:
            query = query.filter(cls.brand_id == brand)

        # Use the EXISTS clause to filter products with available stock
        query = query.filter(article_subquery)

        return query.all()
    
    @classmethod
    def get_available_variants(cls, db_session: Session, product_id):
        """
        Retrieves available variants of a product based on availability of articles,
        with optimized loading for related objects to prevent N+1 problems.
        """
        return db_session.query(Variants).options(joinedload(Variants.articles)).join(Product).filter(
            Product.id == product_id,
            Article.status_code == ArticleStatus.Available
        ).all()

    def get_stock_count(self, db_session: Session):
        """
        Calculates the available stock for the product.
        """
        return db_session.query(Article).join(StockKeepingUnit).filter(
            StockKeepingUnit.sku_product == self.sku_product, 
            Article.status_code == ArticleStatus.Available
        ).count()
        
    def check_stock_and_notify(self):
        """
        Checks stock levels and triggers notifications if needed.
        """
        if self.get_stock_count() < self.low_stock_threshold:
            # Send notification to admins or trigger restocking process
            pass

    def retire_product(self, db_session: Session):
        """
        Retires the product and marks associated articles as retired.
        """
        db_session.query(Article).join(StockKeepingUnit).filter(StockKeepingUnit.sku_product == self.sku_product).update({Article.status_code: ArticleStatus.Retired})
        db_session.commit()
    
    def apply_promotions(self, db_session: Session, user_id: UUID = None) -> float:
        """
        Applies product-specific and user-specific promotions, calculating the total discount percentage.
        This method considers both the validity and availability of promotions.
        """
        # Query for active product-specific promotions
        product_promotions = db_session.query(PromotionsAndDiscounts).join(
            PromotionsProducts, PromotionsProducts.promotion_id == PromotionsAndDiscounts.id
        ).filter(
            PromotionsProducts.product_id == self.id,
            PromotionsAndDiscounts.active == True,
            PromotionsAndDiscounts.valid_from <= func.now(),
            PromotionsAndDiscounts.valid_to >= func.now()
        )

        # Query for active user-specific promotions if user_id is provided
        if user_id:
            user_promotions = db_session.query(PromotionsAndDiscounts).join(
                UserPromotions, UserPromotions.promotion_id == PromotionsAndDiscounts.id
            ).filter(
                UserPromotions.user_id == user_id,
                PromotionsAndDiscounts.active == True,
                PromotionsAndDiscounts.valid_from <= func.now(),
                PromotionsAndDiscounts.valid_to >= func.now()
            )
            all_promotions = product_promotions.union(user_promotions)
        else:
            all_promotions = product_promotions

        total_discount = 0.0
        for promo in all_promotions:
            if promo.uses_left > 0:
                # Calculate the discount based on type
                if promo.discount_type == "Percentage":
                    total_discount += promo.discount_value  # Assume this is already a percentage value (e.g., 10 for 10%)
                elif promo.discount_type == "FixedAmount":
                    total_discount += self.calculate_fixed_discount(promo.discount_value)

                # Decrement uses left and save changes
                promo.uses_left -= 1
                db_session.commit()

        return total_discount

    def calculate_fixed_discount(self, discount_value):
        """
        Calculates the fixed amount discount as a percentage of the product's base price.
        This ensures that fixed amount discounts are accurately reflected in the total percentage discount.
        """
        base_price = self.get_base_price()
        return (discount_value / base_price) * 100 if base_price else 0

    def get_base_price(self, db_session: Session):
        """
        Retrieves the base price of the product from the pricing tier linked through the StockKeepingUnit.
        """
        # Retrieve the first SKU related to this product that has an associated pricing tier
        sku = db_session.query(StockKeepingUnit).join(PricingTier).filter(
            StockKeepingUnit.sku_product == self.sku_product
        ).first()

        # If an SKU with a pricing tier is found, return its retail price
        if sku and sku.pricing_tier:
            return sku.pricing_tier.retail_price
        
        # Return 0 if no pricing tier is found
        return 0