from sqlalchemy.orm import Session
from .models import CategoryForUser
from .schemas import CategoryForUserUpdate  # Assuming an existing schema or need to create
from typing import Optional

class CategoryForUserRepository:
    def __init__(self, db: Session):
        self.db = db

    def assign_category_to_user(self, category_user_data: dict) -> CategoryForUser:
        new_assignment = CategoryForUser(**category_user_data)
        self.db.add(new_assignment)
        self.db.commit()
        return new_assignment

    def get_categories_by_user_uuid(self, user_uuid: str) -> list[CategoryForUser]:
        return self.db.query(CategoryForUser).filter(CategoryForUser.user_uuid == user_uuid).all()

    def update_category_assignment(self, assignment_uuid: str, category_user_data: dict) -> Optional[CategoryForUser]:
        """Update category assignment for a user."""
        assignment = self.db.query(CategoryForUser).filter(CategoryForUser.uuid == assignment_uuid).first()
        if assignment:
            for key, value in category_user_data.items():
                setattr(assignment, key, value)
            self.db.commit()
            return assignment
        return None