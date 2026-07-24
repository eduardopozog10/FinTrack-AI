from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.auth.auth_service import AuthService
from app.database.database import get_session
from app.schemas.user import (
    UserRegister,
    UserRead,
    UserLogin,
    Token,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    "/register",
    response_model=UserRead,
)
def register(
    user: UserRegister,
    session: Session = Depends(get_session),
):
    try:
        return AuthService.register(
            session,
            user,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=Token,
)
def login(
    user: UserLogin,
    session: Session = Depends(get_session),
):
    try:
        return AuthService.login(
            session,
            user,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )