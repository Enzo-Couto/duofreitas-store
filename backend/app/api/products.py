from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.models.product_image import ProductImage
from app.services.image_service import save_product_image

from app.models.product import Product

from app.db.database import get_db

from app.schemas.product import (
    ProductResponse,
    ProductCreate
)

from app.services.product_service import (
    get_product_by_slug,
    get_products,
    create_product,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/")
def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return create_product(db, product)


@router.get("", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return get_products(db)


@router.get("/{slug}", response_model=ProductResponse)
def get_product(
    slug: str,
    db: Session = Depends(get_db)
):
    product = get_product_by_slug(
        db,
        slug
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return product


@router.post("/{product_id}/images")
def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    image_url = save_product_image(file)

    image = ProductImage(
        product_id=product.id,
        image_url=image_url
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    return {
        "message": "Imagem enviada",
        "image_url": image_url
    }
