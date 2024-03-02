from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.models import (
    AdvancedSearchQuery,
    Clothes,
    ClothesCreate,
    ClothesUpdate,
    PaginationQuery,
    SortingQuery,
)
from app.models.sql import ClothesModel

router = APIRouter()


# Clothing Management Endpoints
@router.post("/clothes/", response_model=Clothes)
def create_clothes(clothes: ClothesCreate, db: Session = Depends(get_db)):
    db_clothes = ClothesModel(**clothes.dict())
    db.add(db_clothes)
    db.commit()
    db.refresh(db_clothes)
    return db_clothes


@router.get("/clothes/{clothes_id}", response_model=Clothes)
def read_clothes_by_id(clothes_id: int, db: Session = Depends(get_db)):
    return db.query(ClothesModel).filter(ClothesModel.id == clothes_id).first()


@router.get("/clothes/", response_model=list[Clothes])
async def read_clothes(
    pagination: PaginationQuery = Depends(),
    sorting: SortingQuery = Depends(),
    db: Session = Depends(get_db),
):
    clothes = (
        db.query(ClothesModel)
        .order_by(getattr(getattr(ClothesModel, sorting.sort_by), sorting.order)())
        .offset(pagination.skip)
        .limit(pagination.limit)
        .all()
    )
    return clothes


@router.put("/clothes/{clothes_id}")
def update_clothes(
    clothes_id: int, clothes: ClothesUpdate, db: Session = Depends(get_db)
):
    db_clothes = db.query(ClothesModel).filter(ClothesModel.id == clothes_id).first()
    if not db_clothes:
        raise HTTPException(status_code=404, detail="Clothes not found")
    for var, value in vars(clothes).items():
        setattr(db_clothes, var, value) if value else None
    db.commit()
    db.refresh(db_clothes)
    return db_clothes


@router.delete("/clothes/{clothes_id}")
def delete_clothes(clothes_id: int, db: Session = Depends(get_db)):
    db_clothes = db.query(ClothesModel).filter(ClothesModel.id == clothes_id).first()
    if not db_clothes:
        raise HTTPException(status_code=404, detail="Clothes not found")
    db.delete(db_clothes)
    db.commit()
    return {"detail": "Clothes deleted successfully"}


@router.get("/search/clothes/", response_model=list[Clothes])
async def search_clothes(
    size: str = Query(None),
    color: str = Query(None),
    brand: str = Query(None),
    advanced_search: AdvancedSearchQuery = Depends(),
    pagination: PaginationQuery = Depends(),
    sorting: SortingQuery = Depends(),
    db: Session = Depends(get_db),
):
    query = db.query(ClothesModel)
    # Existing filter conditions
    if size:
        query = query.filter(ClothesModel.size == size)
    if color:
        query = query.filter(ClothesModel.color == color)
    if brand:
        query = query.filter(ClothesModel.brand == brand)

    # Advanced filters
    if advanced_search.min_price:
        query = query.filter(ClothesModel.price >= advanced_search.min_price)
    if advanced_search.max_price:
        query = query.filter(ClothesModel.price <= advanced_search.max_price)
    if advanced_search.min_rating:
        query = query.filter(ClothesModel.average_rating >= advanced_search.min_rating)
    if advanced_search.material:
        query = query.filter(ClothesModel.material == advanced_search.material)

    # Apply pagination and sorting
    query = (
        query.order_by(getattr(getattr(ClothesModel, sorting.sort_by), sorting.order)())
        .offset(pagination.skip)
        .limit(pagination.limit)
    )
    return query.all()
