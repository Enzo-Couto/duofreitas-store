from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.auth import (
    LoginRequest,
    TokenResponse
)

from app.services.auth_service import (
    authenticate_user
)

from app.dependencies.auth import (
    get_current_admin
)

from app.models.admin_user import (
    AdminUser
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Realiza login do administrador",
    responses={
        401: {
            "description": "Email ou senha inválidos"
        }
    }
)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    token = authenticate_user(
        db,
        credentials.email,
        credentials.password
    )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos"
        )

    return token


@router.get(
    "/me",
    summary="Retorna o usuário autenticado"
)
def me(
    current_user: AdminUser = Depends(
        get_current_admin
    )
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }
