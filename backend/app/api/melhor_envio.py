# app/api/melhor_envio.py

from fastapi import APIRouter
from app.core.config import (
    MELHOR_ENVIO_CLIENT_ID,
    MELHOR_ENVIO_REDIRECT_URI
)

router = APIRouter(
    prefix="/melhor-envio",
    tags=["Melhor Envio"]
)

@router.get("/authorize")
def authorize():

    return {
        "url": (
            "https://sandbox.melhorenvio.com.br/oauth/authorize"
            f"?client_id={MELHOR_ENVIO_CLIENT_ID}"
            f"&redirect_uri={MELHOR_ENVIO_REDIRECT_URI}"
            "&response_type=code"
        )
    }
