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
) -> dict | None:

    email = email.lower().strip()

    user = (
        db.query(AdminUser)
        .filter(
            AdminUser.email == email
        )
        .first()
    )

    if (
        not user
        or not verify_password(
            password,
            user.password_hash
        )
    ):
        return None

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "type": "admin"
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
