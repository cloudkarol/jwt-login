from uuid import uuid4, UUID
from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    email: EmailStr = Field()
    password: str = Field()

    class Config:
        orm_mode = True


class UserFullModel(UserModel):
    id: UUID = Field(uuid4())


class UserReadModel(BaseModel):
    id: UUID = Field(uuid4())
    email: EmailStr = Field()

    class Config:
        orm_mode = True
