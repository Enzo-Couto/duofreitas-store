from sqlalchemy.orm import Session, joinedload

from app.models.product import Product
from app.schemas.product import ProductCreate


def get_products(db: Session):
    return (
        db.query(Product)
        .options(
            joinedload(Product.images),
            joinedload(Product.category)
        )
        .filter(Product.active == True)
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
    product = Product(
        name=product_data.name,
        slug=product_data.slug,
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
