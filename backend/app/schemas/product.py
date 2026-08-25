from decimal import Decimal

from pydantic import BaseModel

from app.schemas.product_image import ProductImageResponse

class ProductCreate(BaseModel):
    name: str
    slug: str
    description: str
    price: Decimal
    stock: int
    active: bool = True


class ProductResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    price: float
    stock: int
    active: bool

    images: list[ProductImageResponse] = []

    model_config = {
        "from_attributes": True
    }
