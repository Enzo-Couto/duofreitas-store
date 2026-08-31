from fastapi import (
    APIRouter,
    Depends,
    HTTPException
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

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=TokenResponse
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
            status_code=401,
            detail="Email ou senha inválidos"
        )

    return token
