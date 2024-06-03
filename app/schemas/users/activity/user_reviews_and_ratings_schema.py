from pydantic import UUID4, BaseModel


class UserReviewRatingBase(BaseModel):
    rating: int
    review: str


class UserReviewRatingCreate(UserReviewRatingBase):
    product_id: UUID4


class UserReviewRatingRead(UserReviewRatingBase):
    id: UUID4
    user_id: UUID4
    product_id: UUID4
