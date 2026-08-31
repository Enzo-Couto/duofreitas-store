from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers.auth_router import router as auth_router

from app.api.products import router as products_router
from app.api.categories import router as categories_router

from app.api.orders import router as orders_router

app = FastAPI(
    title="Duo Freitas Store"
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products_router)
app.include_router(categories_router)
app.include_router(auth_router)
app.include_router(orders_router)


@app.get("/")
def root():
    return {
        "status": "online"
    }

from fastapi.routing import APIRoute

@app.on_event("startup")
async def show_routes():
    print("\nROTAS REGISTRADAS:")
    for route in app.routes:
        if isinstance(route, APIRoute):
            print(route.path, route.methods)
