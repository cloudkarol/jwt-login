from distutils.dep_util import newer_pairwise
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from src.services.base import BaseService
from src.entities import User
from sqlalchemy.future import select
from src.models.user import UserModel, UserFullModel


class UserService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session = session
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def save(self, user: User):
        self.session.add(user)
        await self.session.flush()
    
    async def get_by_id(self, _id):
        result = await self.session.execute(select(User).filter(User.id == _id))
        return result.scalars().first()

    async def get_by_email(self, _email):
        query = await self.session.execute(select(User).filter(User.email == _email))
        user_entity = query.scalars().one_or_none()
        if user_entity:
            return UserFullModel.from_orm(user_entity)
        else:
            return None

    async def register_user(self, email: str, password: str):
        existing_user = await self.get_by_email(email)
        if not existing_user:
            new_user = User(email=email, password=self._get_password_hash(password))
            await self.save(new_user)
            return new_user
        else:
            return None

    async def authenticate_user(self, email: str, password: str):
        user = await self.get_by_email(email)
        if not user:
            return False
        if not self._verify_password(password, user.password):
            return False
        return user

    def _get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def _verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)