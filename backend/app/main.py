from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import (
    CORS_ORIGINS,
    UPLOAD_DIR
)

from app.routers.auth_router import router as auth_router

from app.api.products import router as products_router
from app.api.categories import router as categories_router
from app.api.dashboard import router as dashboard_router
from app.api.orders import router as orders_router
from app.api.shipping import router as shipping_router
from app.api.melhor_envio import router as melhor_envio_router

# APP

app = FastAPI(
    title="Duo Freitas Store",
    version="1.0.0"
)

# UPLOADS

Path(UPLOAD_DIR).mkdir(
    parents=True,
    exist_ok=True
)

app.mount(
    "/uploads/products",
    StaticFiles(directory=UPLOAD_DIR),
    name="product_images"
)

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ROUTERS

app.include_router(auth_router)

app.include_router(products_router)

app.include_router(categories_router)

app.include_router(orders_router)

app.include_router(dashboard_router)

app.include_router(shipping_router)

app.include_router(melhor_envio_router)

# HEALTH CHECK

@app.get("/")
def root():
    return {
        "status": "online",
        "application": "Duo Freitas Store",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
