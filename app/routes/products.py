from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.models import (
    AdvancedSearchQuery,
    Brand,
    CatalogProductType,
    CatalogProductTypeList,
    CategoryList,
    Material,
    PaginationQuery,
    Price,
    Product,
    ProductCatalogPhoto,
    ProductCategory,
    ProductCategoryList,
    ProductMaterial,
    ProductMaterialList,
    ProductPhoto,
    ProductPhotoes,
    ProductsCatalog,
    ProductsCatalogs,
    ProductStatus,
    ProductType,
    Size,
    SortingQuery,
    rentalPeriod,
    rentalPeriods,
)
from app.models.sql import ClothesModel, Products

router = APIRouter()


# Clothing Management Endpoints
@router.post("/products_catalog/", response_model=ProductsCatalog)
def create_product_catalog(
    products_catalog: ProductsCatalog, db: Session = Depends(get_db)
):
    db_products = products_catalog(**Products.dict())
    db.add(db_products)
    db.commit()
    db.refresh(db_products)
    return db_products


@router.get("/products_catalog/{product_catalog_id}", response_model=ProductsCatalog)
def read_product_catalogs_by_id(product_catalog_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ProductsCatalog)
        .filter(ProductsCatalog.id == product_catalog_id)
        .first()
    )


@router.get("/products_catalogs/", response_model=list[ProductsCatalogs])
async def read_products_catalogs(
    pagination: PaginationQuery = Depends(),
    sorting: SortingQuery = Depends(),
    db: Session = Depends(get_db),
):
    products_catalogs = (
        db.query(ProductsCatalogs)
        .order_by(getattr(getattr(ProductsCatalogs, sorting.sort_by), sorting.order)())
        .offset(pagination.skip)
        .limit(pagination.limit)
        .all()
    )
    return products_catalogs


@router.put("/products_catalogs/{products_catalog_id}")
def update_products_catalog(
    products_catalog_id: int,
    products_catalogs: ProductsCatalogs,
    db: Session = Depends(get_db),
):
    db_products = (
        db.query(ProductsCatalogs)
        .filter(ProductsCatalogs.id == products_catalog_id)
        .first()
    )
    if not db_products:
        raise HTTPException(status_code=404, detail="Clothes not found")
    for var, value in vars(products_catalogs).items():
        setattr(db_products, var, value) if value else None
    db.commit()
    db.refresh(db_products)
    return db_products


@router.delete("/products_catalogs/{products_catalog_id}")
def delete_clothes(products_catalog_id: int, db: Session = Depends(get_db)):
    db_products = (
        db.query(ProductsCatalogs)
        .filter(ProductsCatalogs.id == products_catalog_id)
        .first()
    )
    if not db_products:
        raise HTTPException(status_code=404, detail="Clothes not found")
    db.delete(db_products)
    db.commit()
    return {"detail": "Clothes deleted successfully"}


@router.get("/search/products_catalogs/", response_model=list[ProductsCatalogs])
async def search_products_catalogs(
    size: str = Query(None),
    color: str = Query(None),
    brand: str = Query(None),
    advanced_search: AdvancedSearchQuery = Depends(),
    pagination: PaginationQuery = Depends(),
    sorting: SortingQuery = Depends(),
    db: Session = Depends(get_db),
):
    query = db.query(ProductsCatalogs)
    # Existing filter conditions
    if size:
        query = query.filter(ProductsCatalogs.size == size)
    if color:
        query = query.filter(ProductsCatalogs.color == color)
    if brand:
        query = query.filter(ProductsCatalogs.brand == brand)

    # Apply pagination and sorting
    query = (
        query.order_by(
            getattr(getattr(ProductsCatalogs, sorting.sort_by), sorting.order)()
        )
        .offset(pagination.skip)
        .limit(pagination.limit)
    )
    return query.all()
