import requests

from app.core import config


def calculate_shipping(
    cep_destino: str,
    products: list
):
    payload = {
        "from": {
            "postal_code":
                config.MELHOR_ENVIO_CEP_ORIGEM
        },

        "to": {
            "postal_code":
                cep_destino
        },

        "products": products
    }

    response = requests.post(
        f"{config.MELHOR_ENVIO_BASE_URL}/shipment/calculate",
        json=payload,
        headers={
            "Authorization":
                f"Bearer {config.MELHOR_ENVIO_TOKEN}",
            "Accept":
                "application/json",
            "Content-Type":
                "application/json"
        }
    )

    response.raise_for_status()

    return response.json()
