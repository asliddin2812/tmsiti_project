from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Literal, Dict, Any, Optional
import os, uuid, shutil

from core.database import get_db
from models.news import News, AntiCorruption
from schemas.news import (
    NewsResponse, AntiCorruptionResponse
)
from utils.dependencies import admin_required
from utils.pagination import paginate, PaginatedResponse

router = APIRouter(prefix="/news", tags=["Xabarlar"])
UPLOAD_DIR = "uploads/news"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(file: UploadFile) -> str:
    filename = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return path

def get_localized_field(item: Any, field: str, lang: str) -> str:
    return getattr(item, f"{field}_{lang}", None) or getattr(item, f"{field}_uz", None) or ""

def transform_news_for_response(item: News, lang: str) -> Dict[str, Any]:
    return {
        "id": item.id,
        "title": get_localized_field(item, "title", lang),
        "content": get_localized_field(item, "content", lang),
        "image": item.image,
        "published_at": item.published_at,
        "created_at": item.created_at,
        "updated_at": item.updated_at
    }

def transform_anti_corruption_for_response(item: AntiCorruption, lang: str) -> Dict[str, Any]:
    return {
        "id": item.id,
        "title": get_localized_field(item, "title", lang),
        "content": get_localized_field(item, "content", lang),
        "file": item.file,
        "created_at": item.created_at,
        "updated_at": item.updated_at
    }

# 🟦 Anti-corruption
@router.get("/anti-corruption", response_model=PaginatedResponse[AntiCorruptionResponse])
def list_anti_corruption(
    page: int = 1,
    size: int = 10,
    lang: Literal["uz", "ru", "en"] = Query("uz"),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(AntiCorruption)
    if search:
        query = query.filter(or_(
            AntiCorruption.title_uz.ilike(f"%{search}%"),
            AntiCorruption.title_ru.ilike(f"%{search}%"),
            AntiCorruption.title_en.ilike(f"%{search}%")
        ))
    paginated = paginate(query.order_by(AntiCorruption.created_at.desc()), page, size)
    paginated.items = [transform_anti_corruption_for_response(i, lang) for i in paginated.items]
    return paginated

@router.post("/anti-corruption", response_model=AntiCorruptionResponse)
def create_anti_corruption(
    title_uz: str = Form(...),
    title_ru: str = Form(...),
    title_en: str = Form(...),
    content_uz: str = Form(...),
    content_ru: str = Form(...),
    content_en: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    file_path = save_uploaded_file(file)
    item = AntiCorruption(
        title_uz=title_uz, title_ru=title_ru, title_en=title_en,
        content_uz=content_uz, content_ru=content_ru, content_en=content_en,
        file=file_path
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return transform_anti_corruption_for_response(item, "uz")

@router.put("/anti-corruption/{id}", response_model=AntiCorruptionResponse)
def update_anti_corruption(
    id: int,
    title_uz: Optional[str] = Form(None),
    title_ru: Optional[str] = Form(None),
    title_en: Optional[str] = Form(None),
    content_uz: Optional[str] = Form(None),
    content_ru: Optional[str] = Form(None),
    content_en: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    item = db.query(AntiCorruption).filter(AntiCorruption.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    if title_uz: item.title_uz = title_uz
    if title_ru: item.title_ru = title_ru
    if title_en: item.title_en = title_en
    if content_uz: item.content_uz = content_uz
    if content_ru: item.content_ru = content_ru
    if content_en: item.content_en = content_en
    if file: item.file = save_uploaded_file(file)

    db.commit()
    db.refresh(item)
    return transform_anti_corruption_for_response(item, "uz")

@router.delete("/anti-corruption/{id}")
def delete_anti_corruption(id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    item = db.query(AntiCorruption).filter(AntiCorruption.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    db.delete(item)
    db.commit()
    return {"message": "O'chirildi"}

# 🟦 News
@router.get("", response_model=PaginatedResponse[NewsResponse])
def list_news(
    page: int = 1,
    size: int = 10,
    lang: Literal["uz", "ru", "en"] = Query("uz"),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(News)
    if search:
        query = query.filter(or_(
            News.title_uz.ilike(f"%{search}%"),
            News.title_ru.ilike(f"%{search}%"),
            News.title_en.ilike(f"%{search}%")
        ))
    paginated = paginate(query.order_by(News.published_at.desc().nullslast()), page, size)
    paginated.items = [transform_news_for_response(i, lang) for i in paginated.items]
    return paginated

@router.post("", response_model=NewsResponse)
def create_news(
    title_uz: str = Form(...),
    title_ru: str = Form(...),
    title_en: str = Form(...),
    content_uz: str = Form(...),
    content_ru: str = Form(...),
    content_en: str = Form(...),
    published_at: Optional[str] = Form(None),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    image_path = save_uploaded_file(image)
    item = News(
        title_uz=title_uz, title_ru=title_ru, title_en=title_en,
        content_uz=content_uz, content_ru=content_ru, content_en=content_en,
        published_at=published_at,
        image=image_path
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return transform_news_for_response(item, "uz")

@router.put("/{id}", response_model=NewsResponse)
def update_news(
    id: int,
    title_uz: Optional[str] = Form(None),
    title_ru: Optional[str] = Form(None),
    title_en: Optional[str] = Form(None),
    content_uz: Optional[str] = Form(None),
    content_ru: Optional[str] = Form(None),
    content_en: Optional[str] = Form(None),
    published_at: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    item = db.query(News).filter(News.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    if title_uz: item.title_uz = title_uz
    if title_ru: item.title_ru = title_ru
    if title_en: item.title_en = title_en
    if content_uz: item.content_uz = content_uz
    if content_ru: item.content_ru = content_ru
    if content_en: item.content_en = content_en
    if published_at: item.published_at = published_at
    if image: item.image = save_uploaded_file(image)

    db.commit()
    db.refresh(item)
    return transform_news_for_response(item, "uz")

@router.delete("/{id}")
def delete_news(id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    item = db.query(News).filter(News.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    db.delete(item)
    db.commit()
    return {"message": "Xabar o'chirildi"}
