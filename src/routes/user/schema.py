from uuid import UUID

from pydantic import BaseModel, EmailStr, SecretStr


class User(BaseModel):
    id: UUID
    name: str
    email: EmailStr


class UserCreatePayload(BaseModel):
    name: str
    email: EmailStr
    password: SecretStr


class UserLoginPayload(BaseModel):
    email: EmailStr
    password: SecretStr
