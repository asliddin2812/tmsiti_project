from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import superadmin_required
from models.user import User, UserRole
from schemas.user import UserResponse, AdminUserUpdate
from utils.dependencies import admin_required
from utils.pagination import paginate, PaginatedResponse

router = APIRouter(prefix="/admin/users", tags=["Admin - Foydalanuvchilar"])

@router.get("", response_model=PaginatedResponse[UserResponse])
def list_users(
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    query = db.query(User).order_by(User.created_at.desc())
    return paginate(query, page, size)

@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    return user

@router.put("/{id}", response_model=UserResponse)
def update_user(
    id: int,
    data: AdminUserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    update_data = data.dict(exclude_unset=True)

    if "role" in update_data and update_data["role"] != user.role:
        if current_user.role != UserRole.superadmin:
            raise HTTPException(status_code=403, detail="Faqat superadmin rolni o‘zgartira oladi")

    if update_data.get("role") == UserRole.superadmin and current_user.role != UserRole.superadmin:
        raise HTTPException(status_code=403, detail="Faqat superadminni admin qilish mumkin")

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/{id}")
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    db.delete(user)
    db.commit()
    return {"message": "Foydalanuvchi o‘chirildi"}
