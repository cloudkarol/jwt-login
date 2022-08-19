from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from src.config.database import get_session
from src.models.user import UserModel
from src.entities import User
from src.services import UserService

router = APIRouter()


@router.get('')
async def get_users():
    return JSONResponse(content={'message': 'ok'})


@router.post('/register')
async def register_user(payload: UserModel, db_session: AsyncSession = Depends(get_session)):
    service = UserService(session=db_session)
    new_user = await service.register_user(payload.email, payload.password)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User already exists",
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'email': new_user.email})


@router.post('/login')
async def register_user(payload: UserModel, db_session: AsyncSession = Depends(get_session)):
    service = UserService(session=db_session)
    user = await service.authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password",
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'email': user.email})
