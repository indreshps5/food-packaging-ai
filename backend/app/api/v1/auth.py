from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.infrastructure.database.repositories.user_repository_impl import (
    UserRepositoryImpl,
)
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    user_repository = UserRepositoryImpl(db)

    existing_username = user_repository.get_by_username(
        request.username
    )

    if existing_username is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists.",
        )

    existing_email = user_repository.get_by_email(
        request.email
    )

    if existing_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists.",
        )

    password_hash = hash_password(
        request.password
    )

    user = user_repository.create(
        username=request.username,
        email=request.email,
        password_hash=password_hash,
    )

    return {
        "status": "success",
        "message": "User registered successfully.",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        },
    }


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    user_repository = UserRepositoryImpl(db)

    user = user_repository.get_by_username(
        request.username
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    password_valid = verify_password(
        request.password,
        user.password_hash,
    )

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "username": user.username,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }