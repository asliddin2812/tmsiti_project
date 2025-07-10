from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.user import User, UserRole

def get_current_user_dependency(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return current_user

def admin_required(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    lang = request.query_params.get("lang", "uz")
    messages = {
        "uz": "Bu amal faqat superadminlar uchun ruxsat etilgan",
        "ru": "Это действие разрешено только администраторам",
        "en": "This action is allowed only for admins"
    }
    if current_user.role != UserRole.superadmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=messages.get(lang, messages["uz"]))
    return current_user

def moderator_required(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    lang = request.query_params.get("lang", "uz")
    messages = {
        "uz": "Bu amal faqat moderator va adminlar uchun ruxsat etilgan",
        "ru": "Это действие разрешено только модераторам и администраторам",
        "en": "This action is allowed only for moderators and admins"
    }
    if current_user.role not in [UserRole.admin, UserRole.moderator]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=messages.get(lang, messages["uz"]))
    return current_user

def get_lang(request: Request) -> str:
    return request.query_params.get("lang", "uz")
