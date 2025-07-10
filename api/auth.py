import string
import secrets
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.user import (
    Token, UserCreate, RegistrationResponse,
    PasswordReset, PasswordResetConfirm, EmailVerification,
    PasswordChange, UserUpdate, UserProfile, UserLogin
)
from models.user import User, UserRole, UserStatus
from core.security import get_password_hash, verify_password, create_access_token
from core.database import get_db
from core.config import settings
from utils.dependencies import get_current_user, admin_required

router = APIRouter(prefix="/auth", tags=["Autentifikatsiya"])

VERIFICATION_CODES = {}

def send_verification_code(email: str):
    code = ''.join(secrets.choice(string.digits) for _ in range(6))
    VERIFICATION_CODES[email] = (code, datetime.now(timezone.utc) + timedelta(minutes=10))  # saqlash va muddati

    msg = MIMEText(f"Sizning tasdiqlash kodingiz: {code}\nBu kod 10 daqiqa ichida amal qiladi.")
    msg['Subject'] = "Tasdiqlash Kodingiz"
    msg['From'] = settings.EMAIL_ADDRESS
    msg['To'] = email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        server.send_message(msg)

@router.post("/register", response_model=RegistrationResponse)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email allaqachon mavjud")
    if data.phone_number and db.query(User).filter(User.phone_number == data.phone_number).first():
        raise HTTPException(status_code=400, detail="Telefon raqam allaqachon mavjud")

    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + timedelta(hours=24)

    total_users = db.query(User).count()
    user_role = UserRole.admin if total_users == 0 else UserRole.user
    user_status = UserStatus.active if total_users == 0 else UserStatus.pending
    is_active = True if total_users == 0 else False
    email_verified = True if total_users == 0 else False

    user = User(
        email=data.email,
        full_name=data.full_name,
        phone_number=data.phone_number,
        password_hash=get_password_hash(data.password),
        gender=data.gender,
        role=user_role,
        status=user_status,
        is_active=is_active,
        email_verified=email_verified,
        email_verification_token=token,
        email_verification_expires=expires
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    if not email_verified:
        send_verification_code(user.email)

    return RegistrationResponse(
        user_id=user.id,
        email=user.email,
        verification_required=not email_verified
    )

@router.post("/verify-email")
def verify_email(email: str, code: str, db: Session = Depends(get_db)):
    if email not in VERIFICATION_CODES:
        raise HTTPException(status_code=400, detail="Tasdiqlash kodi topilmadi")
    stored_code, expiry = VERIFICATION_CODES[email]
    if datetime.now(timezone.utc) > expiry:
        del VERIFICATION_CODES[email]
        raise HTTPException(status_code=400, detail="Tasdiqlash kodi muddati o'tgan")
    if stored_code != code:
        raise HTTPException(status_code=400, detail="Noto‘g‘ri kod")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    user.is_active = True
    user.status = UserStatus.active
    user.email_verified = True
    user.email_verified_at = datetime.now(timezone.utc)
    db.commit()

    del VERIFICATION_CODES[email]
    return {"message": "Email tasdiqlandi, endi login qilishingiz mumkin"}

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email yoki parol noto‘g‘ri")

    now = datetime.now(timezone.utc)
    if user.locked_until and user.locked_until > now:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Hisobingiz vaqtincha bloklangan")
    if user.status == UserStatus.pending:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email manzilingiz tasdiqlanmagan")
    if user.status == UserStatus.suspended:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Hisobingiz bloklangan")

    user.login_attempts = 0
    user.last_login = now
    user.locked_until = None
    if user.status == UserStatus.pending and user.email_verified:
        user.status = UserStatus.active
    db.commit()

    token = create_access_token(data={
        "sub": user.email,
        "user_id": user.id,
        "role": user.role
    })

    expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60 if hasattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES") else 3600

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": expires_in
    }

@router.post("/forgot-password")
def forgot_password(data: PasswordReset, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        return {"message": "Agar email mavjud bo‘lsa, tiklash havolasi yuborildi"}

    reset_token = secrets.token_urlsafe(32)
    reset_expires = datetime.now(timezone.utc) + timedelta(hours=1)

    user.password_reset_token = reset_token
    user.password_reset_expires = reset_expires
    db.commit()

    reset_link = f"http://localhost:3000/reset-password?token={reset_token}"

    msg = MIMEText(f"Parolingizni tiklash uchun ushbu havolani bosing:\n\n{reset_link}\n\nHavola 1 soat amal qiladi.")
    msg['Subject'] = "Parolni tiklash havolasi"
    msg['From'] = settings.EMAIL_ADDRESS
    msg['To'] = user.email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        server.send_message(msg)

    return {"message": "Agar email mavjud bo‘lsa, tiklash havolasi yuborildi"}

@router.get("/profile", response_model=UserProfile)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/profile", response_model=UserProfile)
def update_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if data.phone_number and data.phone_number != current_user.phone_number:
        if db.query(User).filter(User.phone_number == data.phone_number).first():
            raise HTTPException(status_code=400, detail="Telefon raqam allaqachon mavjud")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)
    return current_user
