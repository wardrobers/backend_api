from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import UUID4

from ...database.session import get_db
from ...repositories.product.product_repository import ProductRepository
from ...schemas.product.product_schema import ProductCreate, ProductRead, ProductUpdate


router = APIRouter()


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, request: Request):
    db: Session = request.state.db
    product_repository = ProductRepository(db)
    new_product = product_repository.create_product(product)
    if not new_product:
        raise HTTPException(status_code=400, detail="Error creating the product")
    return new_product


@router.get("/get", response_model=ProductRead)
async def get_product(product_id: UUID4, request: Request):
    db: Session = request.state.db
    product_repository = ProductRepository(db)
    product = product_repository.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/get_all", response_model=list[ProductRead])
async def list_products(request: Request, skip: int = 0, limit: int = 100):
    db: Session = request.state.db
    product_repository = ProductRepository(db)
    products = product_repository.list_products(skip=skip, limit=limit)
    return products


@router.put("/update", response_model=ProductRead)
async def update_product(product_id: UUID4, product: ProductUpdate, request: Request):
    db: Session = request.state.db
    product_repository = ProductRepository(db)
    updated_product = product_repository.update_product(product_id, product)
    if not updated_product:
        raise HTTPException(
            status_code=404, detail="Product not found or update failed"
        )
    return updated_product


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: UUID4, request: Request):
    db: Session = request.state.db
    product_repository = ProductRepository(db)
    product_repository.delete_product(product_id)
    return {"detail": "Product successfully deleted"}


# Assuming you have the necessary methods in your repository for these actions
@router.post(
    "/add_category",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def add_category_to_product(
    product_id: UUID4, category_id: UUID4, request: Request
):
    db: Session = request.state.db
    product_repository = ProductRepository(db)
    product_repository.add_category_to_product(product_id, category_id)
    return {"detail": "Category added to product successfully"}


@router.delete(
    "/remove_category",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_category_from_product(
    product_id: UUID4, category_id: UUID4, request: Request
):
    db: Session = request.state.db
    product_repository = ProductRepository(db)
    product_repository.remove_category_from_product(product_id, category_id)
    return {"detail": "Category removed from product successfully"}


@router.post(
    "/add_material",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def add_material_to_product(
    product_id: UUID4, material_id: UUID4, request: Request
):
    db: Session = request.state.db
    product_repository = ProductRepository(db)
    product_repository.add_material_to_product(product_id, material_id)
    return {"detail": "Material added to product successfully"}


@router.delete(
    "/delete_material",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_material_from_product(
    product_id: UUID4, material_id: UUID4, request: Request
):
    db: Session = request.state.db
    product_repository = ProductRepository(db)
    product_repository.remove_material_from_product(product_id, material_id)
    return {"detail": "Material removed from product successfully"}


@router.post(
    "/add_color",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def add_color_to_product(product_id: UUID4, color_id: UUID4, request: Request):
    db: Session = request.state.db
    product_repository = ProductRepository(db)
    product_repository.add_color_to_product(product_id, color_id)
    return {"detail": "Color added to product successfully"}


@router.delete(
    "/delete_color",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_color_from_product(
    product_id: UUID4, color_id: UUID4, request: Request
):
    db: Session = request.state.db
    product_repository = ProductRepository(db)
    product_repository.remove_color_from_product(product_id, color_id)
    return {"detail": "Color removed from product successfully"}


@router.post(
    "/add_brand",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def add_brand_to_product(product_id: UUID4, brand_id: UUID4, request: Request):
    db: Session = request.state.db
    product_repository = ProductRepository(db)
    product_repository.add_brand_to_product(product_id, brand_id)
    return {"detail": "Brand added to product successfully"}


@router.delete(
    "/remove_brand",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_brand_from_product(
    product_id: UUID4, brand_id: UUID4, request: Request
):
    db: Session = request.state.db
    product_repository = ProductRepository(db)
    product_repository.remove_brand_from_product(product_id, brand_id)
    return {"detail": "Brand removed from product successfully"}
