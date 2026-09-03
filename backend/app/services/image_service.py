from pathlib import Path
from uuid import uuid4

from app.core.config import UPLOAD_DIR


def save_product_image(file, product_id: int):
    extension = file.filename.split(".")[-1]

    product_dir = Path(UPLOAD_DIR) / str(product_id)

    product_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = f"{uuid4()}.{extension}"

    filepath = product_dir / filename

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return (
        f"/uploads/products/"
        f"{product_id}/"
        f"{filename}"
    )
