from decimal import Decimal

from pydantic import BaseModel

from app.schemas.category import CategoryResponse
from app.schemas.product_image import ProductImageResponse

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    active: bool = True

    category_id: int | None = None

class ProductResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    price: float
    stock: int
    active: bool

    category: CategoryResponse | None = None

    images: list[ProductImageResponse] = []

    model_config = {
        "from_attributes": True
    }

class ProductUpdate(ProductCreate):
    pass
