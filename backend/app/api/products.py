from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)
from sqlalchemy.orm import Session

from app.models.product_image import ProductImage
from app.services.image_service import save_product_image

from app.models.product import Product

from app.db.database import get_db

from app.schemas.product import (
    ProductResponse,
    ProductCreate,
    ProductUpdate
)

from app.services.product_service import (
    get_products,
    get_product_by_slug,
    get_product_by_id,
    create_product,
    update_product,
    delete_product
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
    image_type: str = Form("gallery"),
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
        image_url=image_url,
        image_type=image_type
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    return {
        "message": "Imagem enviada",
        "image_url": image_url
    }

@router.get("/id/{product_id}")
def get_product_by_id_route(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = get_product_by_id(
        db,
        product_id
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return product

@router.put("/{product_id}")
def update_product_route(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    product = update_product(
        db,
        product_id,
        product_data
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return product


@router.delete("/{product_id}")
def delete_product_route(
    product_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_product(
        db,
        product_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return {
        "message": "Produto removido"
    }


@router.delete("/images/{image_id}")
def delete_product_image(
    image_id: int,
    db: Session = Depends(get_db)
):
    image = (
        db.query(ProductImage)
        .filter(ProductImage.id == image_id)
        .first()
    )

    if not image:
        raise HTTPException(
            status_code=404,
            detail="Imagem não encontrada"
        )

    db.delete(image)
    db.commit()

    return {
        "message": "Imagem removida"
    }
