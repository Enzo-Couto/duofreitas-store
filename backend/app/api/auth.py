from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.admin_user import AdminUser

from app.schemas.auth import (
    LoginRequest,
    TokenResponse
)

from app.core.security import (
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Login do administrador"
)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    admin = (
        db.query(AdminUser)
        .filter(
            AdminUser.email == credentials.email
        )
        .first()
    )

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

    if not verify_password(
        credentials.password,
        admin.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

    access_token = create_access_token(
        {
            "sub": str(admin.id),
            "email": admin.email
        }
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )
