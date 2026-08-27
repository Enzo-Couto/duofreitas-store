from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.category import Category
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate
)


def get_categories(db: Session):
    return db.query(Category).all()


def get_category_by_id(
    db: Session,
    category_id: int
):
    return (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )


def create_category(db, category_data):

    existing_name = (
        db.query(Category)
        .filter(Category.name == category_data.name)
        .first()
    )

    if existing_name:
        raise HTTPException(
            status_code=400,
            detail='Já existe uma categoria com este nome.'
        )

    existing_slug = (
        db.query(Category)
        .filter(Category.slug == category_data.slug)
        .first()
    )

    if existing_slug:
        raise HTTPException(
            status_code=400,
            detail='Já existe uma categoria com este slug.'
        )

    category = Category(
        **category_data.model_dump()
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def update_category(
    db,
    category_id,
    category_data
):
    category = get_category_by_id(
        db,
        category_id
    )

    existing_name = (
        db.query(Category)
        .filter(
            Category.name == category_data.name,
            Category.id != category_id
        )
        .first()
    )

    if existing_name:
        raise HTTPException(
            status_code=400,
            detail='Já existe uma categoria com este nome.'
        )

    existing_slug = (
        db.query(Category)
        .filter(
            Category.slug == category_data.slug,
            Category.id != category_id
        )
        .first()
    )

    if existing_slug:
        raise HTTPException(
            status_code=400,
            detail='Já existe uma categoria com este slug.'
        )

    category.name = category_data.name
    category.slug = category_data.slug

    db.commit()
    db.refresh(category)

    return category

def delete_category(
    db: Session,
    category_id: int
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if not category:
        return None

    db.delete(category)
    db.commit()

    return category
