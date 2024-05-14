from enum import Enum
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, and_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship, Session
from sqlalchemy.types import Enum as SQLAEnum

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)
from app.models.products import StockKeepingUnit, Article, Product
from app.models.users import User
from app.models.pricing import PriceFactors, PricingTier, PriceMultipliers


class OwnerType(Enum):
    Platform = "Platform"
    Lender = "Lender"
    Brand = "Brand"
    Partner = "Partner"


class Condition(Enum):
    New = "New"
    Excellent = "Excellent"
    Good = "Good"
    Fair = "Fair"
    Poor = "Poor"


class Article(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "article"

    article = Column(String, nullable=False)
    sku_article = Column(String, nullable=False)
    owner_type = Column(SQLAEnum(OwnerType), nullable=False)
    factory_number = Column(String, nullable=True)
    times_used = Column(Integer, nullable=False, default=0)
    hours_used = Column(Integer, nullable=False, default=0)
    min_rental_days = Column(Integer, nullable=False, default=2)
    buffer_days = Column(Integer, nullable=False, default=1)
    pre_rental_buffer = Column(Integer, nullable=True, default=0)
    for_cleaning = Column(Boolean, nullable=True, default=False)
    for_repair = Column(Boolean, nullable=True, default=False)
    condition = Column(SQLAEnum(Condition), nullable=False)

    # Foreign keys
    sku_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("stock_keeping_unit.id"),
        nullable=False,
    )
    status_code = mapped_column(
        String,
        ForeignKey("article_status.status_code"),
        nullable=False,
    )
    types_of_operation_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("types_of_operations.id"),
        nullable=False,
    )

    # Relationships
    specification = relationship("Specificatios", backref="article")
    cleaning_logs = relationship("CleaningLogs", backref="article")
    repair_logs = relationship("RepairLogs", backref="article")
    lender_payments = relationship("LenderPayments", backref="article")
    user_saved_items = relationship("UserSavedItems", backref="article")
    order_items = relationship("OrderItems", backref="article")

    NEW_ITEM_PREMIUM = 1.10

    def new_item_premium(self, db_session: Session) -> bool:
        """Checks if the product is considered new based on the condition of its articles."""
        article = (
            db_session.query(Article)
            .filter(Article.id == self.id)
            .first()
        )
        if article.condition == "New":
            return self.NEW_ITEM_PREMIUM
        else:
            return 1.0

    
    def get_price_for_rental_period(self, db_session: Session, rental_period_id: UUID, user_id: UUID = None) -> float:
        """
        Calculates the price for a specific rental period.
        """
        pricing_tier = (
            db_session.query(PricingTier)
            .filter(PricingTier.product_id == self.id)
            .first()
        )
        rental_period = (
            db_session.query(PriceFactors)
            .filter(PriceFactors.id == rental_period_id)
            .first()
        )

        if not pricing_tier or not rental_period:
            raise ValueError("Pricing tier or rental period not found.")

        # Base Rental Calculation
        base_price = pricing_tier.retail_price
        price_multiplier = next(
            (
                factor.percentage
                for factor in pricing_tier.price_factors
                if factor.rental_period == rental_period.value
            ),
            1.0,
        )
        rental_base = base_price * price_multiplier

        # Category Multiplier (e.g., lower price for accessories)
        category_multiplier = pricing_tier.price_multipliers.multiplier
        rental_base *= category_multiplier

        # New Item Premium (adjust if needed)
        if self.new_item_premium(): 
            rental_base *= 1.10  # 10% premium for new items

        # User Discounts
        if user_id:
            user = db_session.query(User).get(user_id)
            if user.is_first_order():
                rental_base *= 0.67  # 33% discount for first order
            elif user.is_new_customer():
                rental_base *= 0.50  # 50% discount for new customers (within first 500)

        # Promotion Application
        applied_promotion_discount = self.apply_promotions(db_session, user_id)
        rental_base *= (1 - applied_promotion_discount)

        # Additional Costs
        human_service_fee = 2.0  
        insurance_fee = 2.0
        tax_percentage = pricing_tier.tax_percentage
        tax_amount = rental_base * tax_percentage

        # Total Price
        total_price = rental_base + human_service_fee + insurance_fee + tax_amount

        return total_price
    
    def calculate_rental_price(self, rental_days: int, user_id=None):
        """Calculates the total price for renting an article for a specified number of days."""
        pricing_tier = self.get_pricing_tier()
        base_price = pricing_tier.retail_price
        price_multiplier = self.get_price_multiplier(rental_days, pricing_tier)
        category_multiplier = self.get_category_multiplier(pricing_tier)

        rental_price = base_price * price_multiplier * category_multiplier
        rental_price *= self.new_item_premium()
        rental_price += self.calculate_additional_costs(pricing_tier)
        rental_price -= Product.apply_user_discounts(user_id, rental_price)
        rental_price *= (1 - Product.apply_promotions(user_id))

        return rental_price

    def get_pricing_tier(self):
        """Retrieve the pricing tier associated with the article."""
        return self.db_session.query(PricingTier).filter_by(id=self.article.pricing_tier_id).first()

    def get_price_multiplier(self, rental_days, pricing_tier):
        """Retrieves the price multiplier based on the rental period from PriceFactors."""
        factor = self.db_session.query(PriceFactors).filter(
            and_(
                PriceFactors.pricing_tier_id == pricing_tier.id,
                PriceFactors.rental_period <= rental_days
            )
        ).order_by(PriceFactors.rental_period.desc()).first()
        return factor.percentage if factor else 1.0

    def get_category_multiplier(self, pricing_tier):
        """Applies a category-specific multiplier to adjust the pricing."""
        multiplier = self.db_session.query(PriceMultipliers).filter_by(id=pricing_tier.price_multiplier_id).first()
        return multiplier.multiplier if multiplier else 1.0

    def calculate_additional_costs(self, pricing_tier):
        """Calculates additional costs including taxes, insurance, and cleaning fees."""
        tax = pricing_tier.tax_percentage * pricing_tier.retail_price
        insurance = 2.00  # Fixed insurance cost
        cleaning = 2.00  # Fixed cleaning cost
        return tax + insurance + cleaning