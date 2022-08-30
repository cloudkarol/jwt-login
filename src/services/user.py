from sqlalchemy.ext.asyncio import AsyncSession
from src.services import BaseService, AuthService
from src.entities import User
from sqlalchemy.future import select
from src.models.user import UserFullModel, UserReadModel

auth_service = AuthService()

class UserService(BaseService):
    def __init__(self, session: AsyncSession, auth_service: AuthService) -> None:
        super().__init__()
        self.session = session

    async def save(self, user: User):
        self.session.add(user)
        await self.session.flush()
    
    async def get_by_id(self, _id):
        query = await self.session.execute(select(User).filter(User.id == _id))
        user_entity = query.scalars().first()
        return UserReadModel.from_orm(user_entity)

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
            new_user = User(email=email, password=auth_service._get_password_hash(password))
            await self.save(new_user)
            return new_user
        else:
            return None

    async def authenticate_user(self, email: str, password: str):
        user = await self.get_by_email(email)
        if not user:
            return False
        if not auth_service._verify_password(password, user.password):
            return False
        return user

