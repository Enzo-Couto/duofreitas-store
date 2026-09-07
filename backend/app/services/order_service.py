from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product

from app.services.mercadopago_service import (
    create_checkout_preference
)

from app.schemas.order import OrderCreate

def create_order(
    db: Session,
    order_data: OrderCreate
):
    subtotal = Decimal("0")

    order_items = []

    for item in order_data.items:

        product = (
            db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )

        if not product:
            raise Exception(
                f"Produto {item.product_id} não encontrado"
            )

        item_total = (
            product.price *
            item.quantity
        )

        subtotal += item_total

        order_items.append({
            "product": product,
            "quantity": item.quantity,
            "unit_price": product.price
        })

    order = Order(
        customer_name=order_data.customer_name,
        customer_email=order_data.customer_email,
        customer_phone=order_data.customer_phone,
        customer_cpf=order_data.customer_cpf,

        cep=order_data.cep,
        street=order_data.street,
        number=order_data.number,
        complement=order_data.complement,
        neighborhood=order_data.neighborhood,
        city=order_data.city,
        state=order_data.state,

        subtotal=subtotal,
        shipping_cost=0,
        total_amount=subtotal
    )

    db.add(order)

    db.flush()

    for item in order_items:

        db.add(
            OrderItem(
                order_id=order.id,
                product_id=item["product"].id,
                quantity=item["quantity"],
                unit_price=item["unit_price"]
            )
        )

    checkout_items = []

    for item in order_items:

        checkout_items.append({
            "title": item["product"].name,
            "quantity": item["quantity"],
            "unit_price": float(
                item["unit_price"]
            )
        })

    payment = create_checkout_preference(
        order.id,
        checkout_items
    )

    print("PAYMENT RESPONSE:")
    print(payment)

    import json

    print(
        json.dumps(
            payment,
            indent=2,
            ensure_ascii=False,
            default=str
        )
    )

    order.mercadopago_payment_id = payment["id"]

    db.commit()
    db.refresh(order)

    return {
        "id": order.id,

        "customer_name": order.customer_name,
        "customer_email": order.customer_email,
        "customer_phone": order.customer_phone,

        "customer_cpf": order.customer_cpf,

        "cep": order.cep,
        "street": order.street,
        "number": order.number,
        "complement": order.complement,
        "neighborhood": order.neighborhood,
        "city": order.city,
        "state": order.state,

        "subtotal": float(order.subtotal),
        "shipping_cost": float(order.shipping_cost),
        "total_amount": float(order.total_amount),

        "status": order.status,
        "payment_status": order.payment_status,

        "mercadopago_payment_id": order.mercadopago_payment_id,

        "checkout_url": (
            payment.get("sandbox_init_point")
            or payment.get("init_point")
        ),

        "created_at": order.created_at
    }


from app.schemas.order import OrderListResponse

def get_orders(db: Session):
    orders = (
        db.query(Order)
        .order_by(Order.created_at.desc())
        .all()
    )

    return [
        OrderListResponse(
            id=order.id,
            customer_name=order.customer_name,
            customer_phone=order.customer_phone,
            total_amount=float(order.total_amount),
            status=order.status,
            payment_status=order.payment_status,
            created_at=order.created_at,
            items_count=len(order.order_items)
        )
        for order in orders
    ]
