# app/schemas/shipping.py

from pydantic import BaseModel

class ShippingItem(BaseModel):
    product_id: int
    quantity: int


class ShippingCalculateRequest(BaseModel):
    cep: str
    items: list[ShippingItem]
