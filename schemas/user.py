from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Literal
from datetime import datetime
import re

from models.user import UserRole, UserStatus  # ✅ enumlardan foydalanamiz

Gender = Literal["male", "female", "other"]

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    phone_number: Optional[str] = Field(None, max_length=20)
    gender: Optional[Gender] = None

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8 or not re.search(r"[A-Z]", v) or not re.search(r"[a-z]", v) or not re.search(r"\d", v):
            raise ValueError("Parol kuchli bo‘lishi kerak (kamida 8 belgi, 1 ta katta harf, 1 ta kichik harf, 1 ta raqam)")
        return v

    @validator("phone_number")
    def validate_phone(cls, v):
        if v and not re.match(r"^\+998\d{9}$", v):
            raise ValueError("Telefon raqam formati noto‘g‘ri (masalan: +998901234567)")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = Field(None, max_length=500)
    bio: Optional[str] = Field(None, max_length=1000)
    gender: Optional[Gender] = None

class AdminUserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    is_active: Optional[bool] = None

    class Config:
        use_enum_values = True  # ✅ JSON chiqarishda enum.value ni ishlatadi

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[Gender] = None
    role: UserRole
    status: UserStatus
    is_active: bool
    email_verified: bool
    phone_verified: Optional[bool] = None
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    email_verified_at: Optional[datetime] = None
    phone_verified_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        use_enum_values = True  # ✅

class UserProfile(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[Gender] = None
    email_verified: bool
    phone_verified: Optional[bool] = None
    last_login: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)

    @validator("new_password")
    def validate_new_password(cls, v):
        if len(v) < 8 or not re.search(r"[A-Z]", v) or not re.search(r"[a-z]", v) or not re.search(r"\d", v):
            raise ValueError("Yangi parol kuchli bo‘lishi kerak (kamida 8 belgi, 1 ta katta harf, 1 ta kichik harf, 1 ta raqam)")
        return v

class PasswordReset(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)

    @validator("new_password")
    def validate_new_password(cls, v):
        if len(v) < 8 or not re.search(r"[A-Z]", v) or not re.search(r"[a-z]", v) or not re.search(r"\d", v):
            raise ValueError("Yangi parol kuchli bo‘lishi kerak (kamida 8 belgi, 1 ta katta harf, 1 ta kichik harf, 1 ta raqam)")
        return v

class EmailVerification(BaseModel):
    token: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class RegistrationResponse(BaseModel):
    message: str = "Foydalanuvchi muvaffaqiyatli ro‘yxatdan o‘tdi"
    user_id: int
    email: EmailStr
    verification_required: bool = True

class TokenData(BaseModel):
    email: Optional[EmailStr] = None
    user_id: Optional[int] = None
