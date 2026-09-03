import os

from dotenv import load_dotenv

load_dotenv()

# APP

APP_NAME = os.getenv(
    "APP_NAME",
    "Duo Freitas Store"
)

APP_VERSION = os.getenv(
    "APP_VERSION",
    "1.0.0"
)

DEBUG = (
    os.getenv(
        "DEBUG",
        "true"
    ).lower() == "true"
)

# DATABASE

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

# CORS

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        ""
    ).split(",")
    if origin.strip()
]

# JWT

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "change-me"
)

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "1440"
    )
)

# MELHOR ENVIO

MELHOR_ENVIO_CLIENT_ID = os.getenv(
    "MELHOR_ENVIO_CLIENT_ID"
)

MELHOR_ENVIO_CLIENT_SECRET = os.getenv(
    "MELHOR_ENVIO_CLIENT_SECRET"
)

MELHOR_ENVIO_REDIRECT_URI = os.getenv(
    "MELHOR_ENVIO_REDIRECT_URI"
)

MELHOR_ENVIO_TOKEN = os.getenv(
    "MELHOR_ENVIO_TOKEN"
)

MELHOR_ENVIO_SANDBOX = (
    os.getenv(
        "MELHOR_ENVIO_SANDBOX",
        "true"
    ).lower() == "true"
)

MELHOR_ENVIO_BASE_URL = (
    "https://sandbox.melhorenvio.com.br/api/v2/me"
    if MELHOR_ENVIO_SANDBOX
    else
    "https://www.melhorenvio.com.br/api/v2/me"
)

SECRET_KEY = os.getenv(
    "SECRET_KEY"
)

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "1440"
    )
)

UPLOAD_DIR = os.getenv(
    "UPLOAD_DIR",
    "/storage/products"
)
