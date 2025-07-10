from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile, Form
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Literal, Optional
import shutil
import uuid
import os

from core.database import get_db
from models.activities import ManagementSystem
from schemas.activities import ManagementSystemResponse
from utils.dependencies import admin_required
from utils.pagination import PaginatedResponse, paginate

router = APIRouter(prefix="/activities", tags=["Faoliyat"])

UPLOAD_DIR = "uploads/activities"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(file: UploadFile) -> str:
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return file_path

@router.get("", response_model=PaginatedResponse[ManagementSystemResponse])
def list_activities(
    page: int = 1,
    size: int = 10,
    lang: Literal["uz", "ru", "en"] = Query("uz"),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(
        ManagementSystem.id,
        getattr(ManagementSystem, f"title_{lang}").label("title"),
        getattr(ManagementSystem, f"description_{lang}").label("description"),
        ManagementSystem.pdf,
        ManagementSystem.created_at,
        ManagementSystem.updated_at,
    ).order_by(ManagementSystem.created_at.desc())

    if search:
        query = query.filter(or_(
            getattr(ManagementSystem, f"title_{lang}").ilike(f"%{search}%"),
            getattr(ManagementSystem, f"description_{lang}").ilike(f"%{search}%"),
        ))

    paginated = paginate(query, page, size)
    paginated.items = [ManagementSystemResponse(**item._mapping) for item in paginated.items]
    return paginated

@router.post("", response_model=ManagementSystemResponse)
def create_activity(
    title_uz: str = Form(...),
    title_ru: str = Form(...),
    title_en: str = Form(...),
    description_uz: str = Form(...),
    description_ru: str = Form(...),
    description_en: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    pdf_path = save_uploaded_file(file)
    item = ManagementSystem(
        title_uz=title_uz,
        title_ru=title_ru,
        title_en=title_en,
        description_uz=description_uz,
        description_ru=description_ru,
        description_en=description_en,
        pdf=pdf_path
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.put("/{id}", response_model=ManagementSystemResponse)
def update_activity(
    id: int,
    title_uz: Optional[str] = Form(None),
    title_ru: Optional[str] = Form(None),
    title_en: Optional[str] = Form(None),
    description_uz: Optional[str] = Form(None),
    description_ru: Optional[str] = Form(None),
    description_en: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    item = db.query(ManagementSystem).filter(ManagementSystem.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    if title_uz: item.title_uz = title_uz
    if title_ru: item.title_ru = title_ru
    if title_en: item.title_en = title_en
    if description_uz: item.description_uz = description_uz
    if description_ru: item.description_ru = description_ru
    if description_en: item.description_en = description_en
    if file:
        item.pdf = save_uploaded_file(file)

    db.commit()
    db.refresh(item)
    return item

@router.delete("/{id}")
def delete_activity(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    item = db.query(ManagementSystem).filter(ManagementSystem.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    db.delete(item)
    db.commit()
    return {"message": "O'chirildi"}
