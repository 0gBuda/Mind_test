from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import create_access_token, get_current_user
from ..database import get_db
from .schemas import UserCreate, Token, UserResponse
from .crud import create_user, get_user_by_email, verify_password

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await create_user(db, user.username, user.email, user.password)
    return new_user


@router.post("/login", response_model=Token)
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/current_user", response_model=UserResponse)
async def get_current_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@router.post("/logout")
async def logout():
    return {"message": "Successfully logged out"}
