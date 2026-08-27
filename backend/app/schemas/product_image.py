from pydantic import BaseModel


class ProductImageResponse(BaseModel):
    id: int
    image_url: str
    image_type: str

    model_config = {
        "from_attributes": True
    }
