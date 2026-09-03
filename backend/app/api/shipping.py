from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.shipping import (
    ShippingCalculateRequest
)

from app.services.shipping_service import (
    calculate_shipping
)

router = APIRouter(
    prefix="/shipping",
    tags=["Shipping"]
)


@router.post("/calculate")
def calculate_shipping_route(
    payload: ShippingCalculateRequest,
    db: Session = Depends(get_db)
):
    return calculate_shipping(
        db,
        payload.cep,
        payload.items
    )
