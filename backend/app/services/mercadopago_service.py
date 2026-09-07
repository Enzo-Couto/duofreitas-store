import os
import mercadopago

ACCESS_TOKEN = os.getenv(
    "MERCADOPAGO_ACCESS_TOKEN"
)

if not ACCESS_TOKEN:
    raise Exception(
        "MERCADOPAGO_ACCESS_TOKEN não configurado"
    )

sdk = mercadopago.SDK(
    ACCESS_TOKEN
)

def create_pix_payment(
    amount: float,
    description: str,
    payer_email: str,
    payer_name: str,
    payer_cpf: str
):
    payment_data = {
        "transaction_amount": float(amount),
        "description": description,
        "payment_method_id": "pix",
        "payer": {
            "email": payer_email,
            "first_name": payer_name,
            "identification": {
                "type": "CPF",
                "number": payer_cpf
            }
        }
    }

    payment = sdk.payment().create(
        payment_data
    )

    return payment["response"]

def create_checkout_preference(
    order_id: int,
    items: list
):
    preference_data = {
        "items": items,
        "external_reference": str(order_id)
    }

    result = sdk.preference().create(
        preference_data
    )

    return result["response"]
