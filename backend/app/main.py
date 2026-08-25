from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product_image import ProductImage
from app.models.category import Category

from app.api.products import router as products_router
from app.api.categories import router as categories_router


app = FastAPI(
    title="Duo Freitas Store"
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

app.include_router(products_router)
app.include_router(categories_router)

@app.get("/")
def root():
    return {
        "status": "online"
    }
