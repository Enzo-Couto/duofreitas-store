from pathlib import Path
from uuid import uuid4

UPLOAD_DIR = Path("uploads/products")


def save_product_image(file):
    extension = file.filename.split(".")[-1]

    filename = f"{uuid4()}.{extension}"

    filepath = UPLOAD_DIR / filename

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return f"/uploads/products/{filename}"
