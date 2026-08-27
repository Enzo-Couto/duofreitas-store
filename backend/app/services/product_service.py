from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

from slugify import slugify

from app.models.product import Product
from app.schemas.product import (
    ProductCreate,
    ProductUpdate
)


def get_products(db: Session):
    return (
        db.query(Product)
        .options(
            joinedload(Product.images),
            joinedload(Product.category)
        )
        .all()
    )


def get_product_by_slug(
    db: Session,
    slug: str
):
    return (
        db.query(Product)
        .options(
            joinedload(Product.images),
            joinedload(Product.category)
        )
        .filter(Product.slug == slug)
        .first()
    )


def create_product(
    db: Session,
    product_data: ProductCreate
):
    existing_name = (
        db.query(Product)
        .filter(Product.name == product_data.name)
        .first()
    )

    if existing_name:
        raise HTTPException(
            status_code=400,
            detail='Já existe um produto com este nome.'
        )

    slug = slugify(product_data.name)

    existing_slug = (
        db.query(Product)
        .filter(Product.slug == slug)
        .first()
    )

    if existing_slug:
        raise HTTPException(
            status_code=400,
            detail='Já existe um produto com este nome (slug duplicado).'
        )

    product = Product(
        name=product_data.name,
        slug=slug,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
        active=product_data.active,
        category_id=product_data.category_id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product

def get_product_by_id(
    db: Session,
    product_id: int
):
    return (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

def update_product(
    db: Session,
    product_id: int,
    product_data: ProductUpdate
):
    product = get_product_by_id(
        db,
        product_id
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail='Produto não encontrado.'
        )

    existing_name = (
        db.query(Product)
        .filter(
            Product.name == product_data.name,
            Product.id != product_id
        )
        .first()
    )

    if existing_name:
        raise HTTPException(
            status_code=400,
            detail='Já existe um produto com este nome.'
        )

    slug = slugify(product_data.name)

    existing_slug = (
        db.query(Product)
        .filter(
            Product.slug == slug,
            Product.id != product_id
        )
        .first()
    )

    if existing_slug:
        raise HTTPException(
            status_code=400,
            detail='Já existe um produto com este nome (slug duplicado).'
        )

    product.name = product_data.name
    product.slug = slug
    product.description = product_data.description
    product.price = product_data.price
    product.stock = product_data.stock
    product.active = product_data.active
    product.category_id = product_data.category_id

    db.commit()
    db.refresh(product)

    return product

def delete_product(
    db: Session,
    product_id: int
):
    product = get_product_by_id(
        db,
        product_id
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail='Produto não encontrado.'
        )

    db.delete(product)
    db.commit()

    return True
