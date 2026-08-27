from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse
)

from app.services.category_service import (
    get_categories,
    get_category_by_id,
    create_category,
    update_category,
    delete_category
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get(
    "",
    response_model=list[CategoryResponse]
)
def list_categories(
    db: Session = Depends(get_db)
):
    return get_categories(db)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = get_category_by_id(
        db,
        category_id
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    return category


@router.post(
    "",
    response_model=CategoryResponse
)
def create_new_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    return create_category(
        db,
        category
    )


@router.put(
    "/{category_id}",
    response_model=CategoryResponse
)
def update_existing_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db)
):
    updated = update_category(
        db,
        category_id,
        category
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    return updated


@router.delete("/{category_id}")
def remove_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = delete_category(
        db,
        category_id
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    return {
        "message": "Categoria removida"
    }
