from sqlalchemy.orm import Session

from app.models.product import Product

from app.services.melhor_envio_service import (
    calculate_shipping as calculate_melhor_envio
)


def calculate_shipping(
    db: Session,
    cep: str,
    items: list
):
    total_weight = 0
    total_height = 0
    total_width = 0
    total_length = 0

    for item in items:

        products = [
            {
                "id": "1",
                "width": max_width,
                "height": total_height,
                "length": total_length,
                "weight": total_weight,
                "insurance_value": 1,
                "quantity": 1
            }
        ]

        if not product:
            continue

        total_weight += (
            float(product.weight)
            * item.quantity
        )

        total_height = max(
            total_height,
            product.height
        )

        total_width = max(
            total_width,
            product.width
        )

        total_length += (
            product.length
            * item.quantity
        )

    return calculate_melhor_envio(
        cep,
        products
    )
