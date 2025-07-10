from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as SqlEnum
from sqlalchemy.sql import func
from enum import Enum
from core.database import Base
from datetime import datetime

class UserRole(str, Enum):
    superadmin = "superadmin"  # ✅ Qo‘shildi
    admin = "admin"
    user = "user"
    moderator = "moderator"

class UserStatus(str, Enum):
    pending = "pending"
    active = "active"
    suspended = "suspended"
    banned = "banned"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=False)
    gender = Column(String, nullable=True)

    # Yangi qo‘shilgan ustunlar
    avatar_url = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    phone_verified = Column(Boolean, default=False)
    phone_verified_at = Column(DateTime, nullable=True)

    role = Column(SqlEnum(UserRole), default=UserRole.user, nullable=False)
    status = Column(SqlEnum(UserStatus), default=UserStatus.pending, nullable=False)
    is_active = Column(Boolean, default=True)

    email_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime, nullable=True)
    email_verification_token = Column(String, nullable=True)
    email_verification_expires = Column(DateTime, nullable=True)

    login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)

    password_reset_token = Column(String, nullable=True)
    password_reset_expires = Column(DateTime, nullable=True)

    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def can_login(self):
        now = datetime.utcnow()
        if not self.is_active or self.status in [UserStatus.suspended, UserStatus.banned]:
            return False
        if self.locked_until and self.locked_until > now:
            return False
        return True
