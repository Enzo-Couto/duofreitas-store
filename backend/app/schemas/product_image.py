from pydantic import BaseModel


class ProductImageResponse(BaseModel):
    id: int
    image_url: str
    is_primary: bool

    model_config = {
        "from_attributes": True
    }
