from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database import get_session
from src.models.user import UserModel
from src.services import UserService, AuthService


router = APIRouter()
auth_service = AuthService()

@router.get('/info')
async def get_user(current_user = Depends(auth_service.get_current_user), db_session: AsyncSession = Depends(get_session)):
    service = UserService(session=db_session)
    user = await service.get_by_id(_id=current_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
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


@router.post('/token')
async def login_for_token(form: OAuth2PasswordRequestForm = Depends(), db_session: AsyncSession = Depends(get_session)):
    service = UserService(session=db_session)
    user = await service.authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password",
        )
    token = auth_service.create_access_token(user=user)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'token': token, 'type': 'bearer'})
