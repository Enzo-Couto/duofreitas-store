from sqlalchemy.orm import Session

from app.models.admin_user import AdminUser

from app.core.security import (
    verify_password,
    create_access_token
)


def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = (
        db.query(AdminUser)
        .filter(
            AdminUser.email == email
        )
        .first()
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash
    ):
        return None

    token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
