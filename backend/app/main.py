from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Força o carregamento dos models
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem

from app.api.products import router as products_router

app = FastAPI(
    title="Duo Freitas Store"
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

app.include_router(products_router)

@app.get("/")
def root():
    return {
        "status": "online"
    }
