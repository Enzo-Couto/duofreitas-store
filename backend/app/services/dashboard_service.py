from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.order import Order


def get_dashboard_stats(db: Session):

    total_orders = db.query(Order).count()

    # Status do pedido

    pending_orders = (
        db.query(Order)
        .filter(Order.status == "pending")
        .count()
    )

    processing_orders = (
        db.query(Order)
        .filter(Order.status == "processing")
        .count()
    )

    shipped_orders = (
        db.query(Order)
        .filter(Order.status == "shipped")
        .count()
    )

    delivered_orders = (
        db.query(Order)
        .filter(Order.status == "delivered")
        .count()
    )

    cancelled_orders = (
        db.query(Order)
        .filter(Order.status == "cancelled")
        .count()
    )

    # Status do pagamento

    pending_payments = (
        db.query(Order)
        .filter(Order.payment_status == "pending")
        .count()
    )

    approved_payments = (
        db.query(Order)
        .filter(Order.payment_status == "approved")
        .count()
    )

    refunded_payments = (
        db.query(Order)
        .filter(Order.payment_status == "refunded")
        .count()
    )

    cancelled_payments = (
        db.query(Order)
        .filter(Order.payment_status == "cancelled")
        .count()
    )

    revenue = (
        db.query(
            func.coalesce(
                func.sum(Order.total_amount),
                0
            )
        )
        .filter(
            Order.payment_status == "approved"
        )
        .scalar()
    )

    orders_by_day = (
        db.query(
            func.date(Order.created_at).label("date"),

            func.count(Order.id).label("count"),

            func.coalesce(
                func.sum(Order.total_amount),
                0
            ).label("revenue")
        )
        .group_by(
            func.date(Order.created_at)
        )
        .order_by(
            func.date(Order.created_at)
        )
        .all()
    )

    latest_orders = (
        db.query(Order)
        .order_by(Order.created_at.desc())
        .limit(10)
        .all()
    )

    return {
        "total_orders": total_orders,

        "pending_orders": pending_orders,
        "processing_orders": processing_orders,
        "shipped_orders": shipped_orders,
        "delivered_orders": delivered_orders,
        "cancelled_orders": cancelled_orders,

        "pending_payments": pending_payments,
        "approved_payments": approved_payments,
        "refunded_payments": refunded_payments,
        "cancelled_payments": cancelled_payments,

        "revenue": float(revenue),

        "orders_by_day": [
            {
                "date": str(row.date),
                "count": row.count,
                "revenue": float(row.revenue)
            }
            for row in orders_by_day
        ],

        "latest_orders": [
            {
                "id": order.id,
                "customer_name": order.customer_name,
                "status": order.status,
                "payment_status": order.payment_status,
                "total": float(order.total_amount),
                "created_at": order.created_at
            }
            for order in latest_orders
        ]
    }
