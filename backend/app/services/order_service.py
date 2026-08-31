from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product

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

    db.commit()
    db.refresh(order)

    return order


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
