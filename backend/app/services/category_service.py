from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate


def get_categories(db: Session):
    return db.query(Category).all()


def create_category(
    db: Session,
    category_data: CategoryCreate
):
    category = Category(
        name=category_data.name,
        slug=category_data.slug
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category
