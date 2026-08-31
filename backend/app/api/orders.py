from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.order import Order

from app.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderListResponse,
    OrderDetailResponse,
    OrderItemResponse,
    OrderStatusUpdate,
    PaymentStatusUpdate
)

from app.services.order_service import (
    create_order,
    get_orders
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    "",
    response_model=OrderResponse
)
def create_order_route(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    return create_order(
        db,
        order_data
    )


@router.get(
    "",
    response_model=list[OrderListResponse]
)
def list_orders(
    db: Session = Depends(get_db)
):
    return get_orders(db)


@router.get(
    "/{order_id}",
    response_model=OrderDetailResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    return OrderDetailResponse(
        id=order.id,

        customer_name=order.customer_name,
        customer_email=order.customer_email,
        customer_phone=order.customer_phone,

        customer_cpf=order.customer_cpf,

        cep=order.cep,
        street=order.street,
        number=order.number,
        complement=order.complement,
        neighborhood=order.neighborhood,
        city=order.city,
        state=order.state,

        subtotal=float(order.subtotal),
        shipping_cost=float(order.shipping_cost),
        total_amount=float(order.total_amount),

        status=order.status,
        payment_status=order.payment_status,

        created_at=order.created_at,

        items=[
            OrderItemResponse(
                product_id=item.product_id,
                product_name=item.product.name,
                quantity=item.quantity,
                unit_price=float(item.unit_price)
            )
            for item in order.order_items
        ]
    )


@router.patch(
    "/{order_id}/status",
    response_model=OrderDetailResponse
)
def update_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    order.status = payload.status

    db.commit()
    db.refresh(order)

    return get_order(
        order_id,
        db
    )


@router.patch(
    "/{order_id}/payment-status",
    response_model=OrderDetailResponse
)
def update_payment_status(
    order_id: int,
    payload: PaymentStatusUpdate,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    order.payment_status = payload.payment_status

    db.commit()
    db.refresh(order)

    return get_order(
        order_id,
        db
    )
