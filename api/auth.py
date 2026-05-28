from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from motor.motor_asyncio import AsyncIOMotorDatabase

from database import get_db
from repository.user_repository import UserRepository
from schemas.user_schema import RefreshRequest, TokenResponse, UserCreate, UserResponse
from services.auth_service import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_user_repo(db: AsyncIOMotorDatabase = Depends(get_db)):
    return UserRepository(db)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, repo: UserRepository = Depends(get_user_repo)):
    if await repo.get_by_username(user_data.username):
        raise HTTPException(status_code=400, detail="Користувач вже існує")
    user = await repo.create(user_data)
    return UserResponse(username=user["username"])


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserCreate, repo: UserRepository = Depends(get_user_repo)):
    user = await repo.get_by_username(user_data.username)
    if not user or not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невірні облікові дані")

    return TokenResponse(
        access_token=create_access_token({"sub": user["username"]}),
        refresh_token=create_refresh_token({"sub": user["username"]}),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(request_data: RefreshRequest, repo: UserRepository = Depends(get_user_repo)):
    try:
        payload = decode_token(request_data.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невірний тип токена")
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невірний токен")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невірний refresh token")

    user = await repo.get_by_username(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Користувача не знайдено")

    return TokenResponse(
        access_token=create_access_token({"sub": username}),
        refresh_token=create_refresh_token({"sub": username}),
    )