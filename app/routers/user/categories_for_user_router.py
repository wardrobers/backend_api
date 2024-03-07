from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import UUID4

from ...database.session import get_db
from ...repositories.user.category_for_user_repository import CategoryForUserRepository
from ...schemas.user.categories_for_user_schema import (
    CategoryForUserCreate,
    CategoryForUserRead,
    CategoryForUserUpdate,
)

router = APIRouter()


@router.post(
    "/{user_uuid}/categories/",
    response_model=CategoryForUserRead,
    status_code=status.HTTP_201_CREATED,
)
def assign_category_to_user(
    category_assignment: CategoryForUserCreate, db: Session = Depends(get_db)
):
    """
    Assign a category to a user.
    """
    category_for_user_repository = CategoryForUserRepository(db)
    new_assignment = category_for_user_repository.assign_category_to_user(
        category_assignment.dict()
    )
    if not new_assignment:
        raise HTTPException(status_code=400, detail="Could not assign category to user")
    return new_assignment


@router.get("/{user_uuid}/categories/", response_model=list[CategoryForUserRead])
def list_categories_for_user(user_uuid: UUID4, db: Session = Depends(get_db)):
    """
    List all categories assigned to a user.
    """
    category_for_user_repository = CategoryForUserRepository(db)
    categories = category_for_user_repository.get_categories_by_user_uuid(user_uuid)
    return categories


@router.patch(
    "/{user_uuid}/categories/{category_assignment_uuid}",
    response_model=CategoryForUserRead,
)
def update_category_assignment(
    category_assignment_uuid: str,
    category_update: CategoryForUserUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a category assignment for a user.
    """
    category_for_user_repository = CategoryForUserRepository(db)
    updated_assignment = category_for_user_repository.update_category_assignment(
        category_assignment_uuid, category_update.dict()
    )
    if not updated_assignment:
        raise HTTPException(status_code=404, detail="Category assignment not found")
    return updated_assignment


@router.delete(
    "/{user_uuid}/categories/{category_assignment_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_category_assignment(
    category_assignment_uuid: str, db: Session = Depends(get_db)
):
    """
    Remove a category assignment from a user.
    """
    category_for_user_repository = CategoryForUserRepository(db)
    if not category_for_user_repository.remove_category_assignment(
        category_assignment_uuid
    ):
        raise HTTPException(
            status_code=404,
            detail="Category assignment not found or could not be removed",
        )
    return {"detail": "Category assignment removed successfully"}
