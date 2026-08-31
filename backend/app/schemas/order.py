from datetime import datetime
from pydantic import BaseModel

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: str

    customer_cpf: str

    cep: str
    street: str
    number: str
    complement: str | None = None
    neighborhood: str
    city: str
    state: str

    items: list[OrderItemCreate]

class OrderItemResponse(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: float

from datetime import datetime

class OrderResponse(BaseModel):
    id: int

    customer_name: str
    customer_email: str
    customer_phone: str

    customer_cpf: str

    cep: str
    street: str
    number: str
    complement: str | None = None
    neighborhood: str
    city: str
    state: str

    subtotal: float
    shipping_cost: float
    total_amount: float

    status: str
    payment_status: str

    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class OrderListResponse(BaseModel):
    id: int

    customer_name: str
    customer_phone: str

    total_amount: float

    status: str
    payment_status: str

    created_at: datetime

    items_count: int

    model_config = {
        "from_attributes": True
    }

class OrderDetailResponse(BaseModel):
    id: int

    customer_name: str
    customer_email: str
    customer_phone: str

    customer_cpf: str

    cep: str
    street: str
    number: str
    complement: str | None = None
    neighborhood: str
    city: str
    state: str

    subtotal: float
    shipping_cost: float
    total_amount: float

    status: str
    payment_status: str

    created_at: datetime

    items: list[OrderItemResponse]

    model_config = {
        "from_attributes": True
    }

class OrderStatusUpdate(BaseModel):
    status: str


class PaymentStatusUpdate(BaseModel):
    payment_status: str
