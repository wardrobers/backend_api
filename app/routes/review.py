from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID as PyUUID
from ..dependencies import get_db
from ..models.pydantic import ReviewCreate, ReviewUpdate
from ..models.sqlalchemy import ReviewModel

router = APIRouter()


@router.post("/reviews/", response_model=ReviewCreate)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    new_review = ReviewModel(**review.dict())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@router.put("/reviews/{review_id}", response_model=ReviewUpdate)
def update_review(
    review_id: PyUUID, review: ReviewUpdate, db: Session = Depends(get_db)
):
    db_review = db.query(ReviewModel).filter(ReviewModel.uuid == review_id).first()
    if db_review:
        update_data = review.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_review, key, value)
        db.commit()
        db.refresh(db_review)
        return db_review
    raise HTTPException(status_code=404, detail="Review not found")


@router.get("/clothes/{clothe_uuid}/average_rating")
def get_average_rating(clothe_uuid: PyUUID, db: Session = Depends(get_db)):
    ratings = (
        db.query(ReviewModel.rating)
        .filter(ReviewModel.clothe_uuid == clothe_uuid)
        .all()
    )
    if ratings:
        avg_rating = sum(rating[0] for rating in ratings) / len(ratings)
        return {"average_rating": avg_rating}
    return {"average_rating": "No ratings yet"}
