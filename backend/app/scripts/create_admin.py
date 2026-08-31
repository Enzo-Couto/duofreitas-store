from app.db.database import SessionLocal

from app.models.admin_user import AdminUser

# força registro dos models
from app.models.category import Category
from app.models.product import Product
from app.models.product_image import ProductImage

from app.core.security import hash_password


db = SessionLocal()

email = "admin@duofreitas.com"

existing_user = (
    db.query(AdminUser)
    .filter(
        AdminUser.email == email
    )
    .first()
)

if existing_user:
    print("Admin já existe.")
    exit()

admin = AdminUser(
    name="Administrador",
    email=email,
    password_hash=hash_password(
        "Admin123@"
    )
)

db.add(admin)

db.commit()

print("Admin criado com sucesso!")
