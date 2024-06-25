from typing import Optional

from sqlalchemy import func, update
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session, joinedload

from app.models.products import (
    Articles,
    ArticleStatus,
    Categories,
    ProductCategories,
    Products,
    Sizing,
    StockKeepingUnits,
    Variants,
)
from app.repositories.common import BaseMixin, BulkActionsMixin, SearchMixin
from app.schemas.common import PaginatedResponse
from app.schemas.products import (
    ProductCreate,
    ProductUpdate,
    SizingCreate,
    VariantCreate,
)


class ProductsRepository(BaseMixin, BulkActionsMixin, SearchMixin):
    """
    Repository responsible for all database operations related to the Products model.
    """

    model = Products

    # --- Product-Specific Retrieval Methods ---

    def get_available_products(
        self,
        db_session: Session,
        category_id: Optional[UUID] = None,
        brand_id: Optional[UUID] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatedResponse:
        """
        Retrieves products with available stock based on filters, using pagination.
        """
        filters = {}
        relationships = {}
        if category_id:
            relationships["categories"] = ("category_id", category_id)
        if brand_id:
            filters["brand_id"] = brand_id

        return self.paginate(
            db_session=db_session,
            page=page,
            page_size=page_size,
            filters=filters,
            relationships=relationships,
        )

    def get_product_details(
        self, db_session: Session, product_id: UUID
    ) -> Optional[Products]:
        """
        Retrieves a product with all its details (variants, sizing, etc.).
        """
        product = (
            db_session.query(Products)
            .options(
                joinedload(Products.brands),
                joinedload(Products.categories)
                .joinedload(ProductCategories.categories)
                .joinedload(Categories.materials),
                joinedload(Products.variants)
                .joinedload(Variants.sizing)
                .joinedload(Sizing.size_system),
            )
            .filter(Products.id == product_id, Products.deleted_at.is_(None))
            .first()
        )
        return product

    def get_available_variants(
        self, db_session: Session, product_id: UUID
    ) -> list[Variants]:
        """
        Retrieves available variants of a product based on availability of articles.
        """
        return (
            db_session.query(Variants)
            .options(joinedload(Variants.articles))
            .join(self.model)
            .filter(
                self.model.id == product_id,
                Articles.status_code == ArticleStatus.Available,
            )
            .all()
        )

    # --- Inventory and Stock Management ---

    def get_stock_count_for_variant(self, db_session: Session, variant_id: UUID) -> int:
        """
        Calculates the stock count for a specific variant.
        """
        return (
            db_session.query(func.count(Articles.id))
            .join(StockKeepingUnits, Articles.sku_id == StockKeepingUnits.id)
            .join(Variants, Variants.sku_id == StockKeepingUnits.id)
            .filter(
                Variants.id == variant_id,
                Articles.status_code == ArticleStatus.Available,
            )
            .scalar()
        )

    def decrement_stock_for_variant(
        self, db_session: Session, variant_id: UUID, quantity: int
    ):
        """
        Decrements the stock count for a specific variant (e.g., after an order).
        """
        # Ensure atomicity for stock updates. This example assumes a simplified stock update logic.
        # You might need a more complex approach (e.g., using transactions) for a production-ready system.
        db_session.execute(
            update(StockKeepingUnits)
            .where(
                StockKeepingUnits.id == variant_id,
                StockKeepingUnits.free_articles_count >= quantity,
            )
            .values(
                free_articles_count=StockKeepingUnits.free_articles_count - quantity
            )
        )
        db_session.commit()

    # --- Product Filtering and Search ---
    def filter_products(
        self,
        db_session: Session,
        category_ids: Optional[list[UUID]] = None,
        brand_ids: Optional[list[UUID]] = None,
        color_ids: Optional[list[UUID]] = None,
        size_system_ids: Optional[list[UUID]] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        search_term: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatedResponse:
        """
        Provides advanced filtering and search capabilities for products.
        """
        filters = {}
        relationships = {}

        if category_ids:
            relationships["categories"] = ("category_id", category_ids)
        if brand_ids:
            filters["brand_id"] = brand_ids

        if color_ids:
            relationships["variants"] = ("color_id", color_ids)
        if size_system_ids:
            relationships["variants_sizing"] = ("size_system_id", size_system_ids)
        if price_min is not None:
            filters["price_min"] = price_min
        if price_max is not None:
            filters["price_max"] = price_max

        # Apply search if a search term is provided
        if search_term:
            search_results = self.search(
                db_session=db_session,
                search_term=search_term,
                fields=["name", "description"],
                relationships=relationships,
                fuzzy_threshold=2,
                ranking=True,
            )
            return PaginatedResponse(
                items=search_results,
                page=page,
                page_size=page_size,
                total_count=len(search_results),
            )
        else:
            return self.paginate(
                db_session=db_session,
                page=page,
                page_size=page_size,
                filters=filters,
                relationships=relationships,
            )

    # --- Product Creation and Updates ---

    def create_product(
        self, db_session: Session, product_data: ProductCreate
    ) -> Products:
        """
        Creates a new product with associated variants and other details.
        Handles database transactions and relationships.
        """
        # with db_session.begin():
        # Create the product
        new_product = self.create(
            db_session, **product_data.model_dump(exclude={"variants"})
        )

        # Create variants
        for variant_data in product_data.variants:
            new_variant = self._create_variant(db_session, new_product, variant_data)
            for sizing_data in variant_data.sizing:
                self._create_sizing(db_session, new_variant.id, sizing_data)

        db_session.refresh(new_product)
        return new_product

    def _create_variant(
        self, db_session: Session, product: Products, variant_data: VariantCreate
    ) -> Variants:
        """
        Creates a variant associated with the given product.
        """
        # Create the variant
        new_variant = Variants(**variant_data.model_dump(exclude={"sizing"}))
        db_session.add(new_variant)
        db_session.commit()
        db_session.refresh(new_variant)
        return new_variant

    def _create_sizing(
        self, db_session: Session, variant: Variants, sizing_data: SizingCreate
    ):
        """
        Creates a sizing option for the given variant.
        """
        # Create the sizing
        new_sizing = Sizing(**sizing_data.model_dump(exclude_unset=True))
        db_session.add(new_sizing)
        db_session.commit()
        db_session.refresh(new_sizing)
        return new_sizing

    def update_product(
        self, db_session: Session, product_id: UUID, product_data: ProductUpdate
    ) -> Products:
        """
        Updates an existing product and its related data.
        """
        with db_session.begin():
            product = self.get_by_id(db_session, product_id)
            if not product:
                raise ValueError(f"Product not found with ID: {product_id}")

            # Update the product itself
            self.update(
                db_session, product, **product_data.model_dump(exclude_unset=True)
            )

            # Update or create variants (consider using bulk_upsert for efficiency)
            self._update_or_create_variants(db_session, product, product_data.variants)

            return product

    def _update_or_create_variants(
        self, db_session: Session, product: Products, variant_data: list[VariantCreate]
    ):
        """
        Updates or creates variants for a product.
        This is a simplified example, you might need a more complex strategy for handling variant updates.
        """
        for data in variant_data:
            variant_id = data.get("id")
            if variant_id:
                # Update existing variant
                variant = db_session.query(Variants).get(variant_id)
                if variant:
                    self.update(
                        db_session, variant, **data.model_dump(exclude_unset=True)
                    )
                    self._update_or_create_sizing(db_session, variant, data.sizing)
            else:
                # Create new variant
                self._create_variant(db_session, product, data)

    def _update_or_create_sizing(
        self, db_session: Session, variant: Variants, sizing_data: list[SizingCreate]
    ):
        """
        Updates or creates sizing options for a variant.
        """
        for data in sizing_data:
            sizing_id = data.get("id")
            if sizing_id:
                # Update existing sizing
                sizing = db_session.query(Sizing).get(sizing_id)
                if sizing:
                    self.update(
                        db_session, sizing, **data.model_dump(exclude_unset=True)
                    )
            else:
                # Create new sizing
                self._create_sizing(db_session, variant, data)
