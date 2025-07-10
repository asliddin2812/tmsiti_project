from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Literal, Optional
from core.database import get_db
from models.institute import About, Management, Structure, StructuralDivision, Vacancy
from schemas.institute import (
    AboutResponse, ManagementResponse, StructureResponse,
    StructuralDivisionResponse, VacancyResponse
)
from utils.dependencies import admin_required
from utils.pagination import paginate, PaginatedResponse
import shutil
import uuid
import os

router = APIRouter(prefix="/institute", tags=["Institut"])

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_file(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename)[-1]
    filename = f"{uuid.uuid4()}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return f"/{path}"

@router.get("/about", response_model=List[AboutResponse])
def list_about(lang: Literal["uz", "ru", "en"] = Query("uz"), search: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(About)
    if search:
        query = query.filter(getattr(About, f"content_{lang}").ilike(f"%{search}%"))
    return query.all()

@router.post("/about", response_model=AboutResponse)
def create_about(content_uz: str = Form(...), content_ru: str = Form(...), content_en: str = Form(...), pdf_file: UploadFile = File(...)
, db: Session = Depends(get_db), user=Depends(admin_required)):
    pdf_url = save_file(pdf_file) if pdf_file else None
    item = About(content_uz=content_uz, content_ru=content_ru, content_en=content_en, pdf_url=pdf_url)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/about/{id}", response_model=AboutResponse)
def update_about(
        id: int,
        content_uz: Optional[str] = Form(None),
        content_ru: Optional[str] = Form(None),
        content_en: Optional[str] = Form(None),
        pdf_file: UploadFile = File(...),
        db: Session = Depends(get_db),
        user=Depends(admin_required)
):
    item = db.query(About).filter(About.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    if content_uz is not None:
        item.content_uz = content_uz
    if content_ru is not None:
        item.content_ru = content_ru
    if content_en is not None:
        item.content_en = content_en
    if pdf_file is not None:
        item.pdf_url = save_file(pdf_file)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/about/{id}")
def delete_about(id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    item = db.query(About).filter(About.id == id).first()
    if not item:
        raise HTTPException(404)
    db.delete(item)
    db.commit()
    return {"message": "O'chirildi"}

@router.get("/management", response_model=List[ManagementResponse])
def list_management(lang: Literal["uz", "ru", "en"] = Query("uz"), search: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Management)
    if search:
        query = query.filter(getattr(Management, f"position_{lang}").ilike(f"%{search}%"))
    return [
        ManagementResponse(
            full_name=i.full_name,
            position=getattr(i, f"position_{lang}"),
            profile_image=i.profile_image,
            reception_days=i.reception_days,
            phone=i.phone,
            email=i.email,
            specialization=getattr(i, f"specialization_{lang}")
        ) for i in query.all()
    ]

@router.post("/management", response_model=ManagementResponse)
def create_management(full_name: str = Form(...), position_uz: str = Form(...), position_ru: str = Form(...), position_en: str = Form(...), profile_image: UploadFile = File(...), reception_days: Optional[str] = Form(None), phone: Optional[str] = Form(None), email: Optional[str] = Form(None), specialization_uz: Optional[str] = Form(None), specialization_ru: Optional[str] = Form(None), specialization_en: Optional[str] = Form(None), order_index: Optional[int] = Form(0), db: Session = Depends(get_db), user=Depends(admin_required)):
    image_url = save_file(profile_image) if profile_image else None
    item = Management(full_name=full_name, position_uz=position_uz, position_ru=position_ru, position_en=position_en, profile_image=image_url, reception_days=reception_days, phone=phone, email=email, specialization_uz=specialization_uz, specialization_ru=specialization_ru, specialization_en=specialization_en, order_index=order_index)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.put("/management/{id}", response_model=ManagementResponse)
def update_management(id: int, full_name: Optional[str] = Form(None), position_uz: Optional[str] = Form(None), position_ru: Optional[str] = Form(None), position_en: Optional[str] = Form(None), profile_image: UploadFile = File(...), reception_days: Optional[str] = Form(None), phone: Optional[str] = Form(None), email: Optional[str] = Form(None), specialization_uz: Optional[str] = Form(None), specialization_ru: Optional[str] = Form(None), specialization_en: Optional[str] = Form(None), order_index: Optional[int] = Form(None), db: Session = Depends(get_db), user=Depends(admin_required)):
    item = db.query(Management).filter(Management.id == id).first()
    if not item:
        raise HTTPException(404)
    if full_name: item.full_name = full_name
    if position_uz: item.position_uz = position_uz
    if position_ru: item.position_ru = position_ru
    if position_en: item.position_en = position_en
    if profile_image: item.profile_image = save_file(profile_image)
    if reception_days: item.reception_days = reception_days
    if phone: item.phone = phone
    if email: item.email = email
    if specialization_uz: item.specialization_uz = specialization_uz
    if specialization_ru: item.specialization_ru = specialization_ru
    if specialization_en: item.specialization_en = specialization_en
    if order_index is not None: item.order_index = order_index
    db.commit()
    db.refresh(item)
    return item

@router.delete("/management/{id}")
def delete_management(id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    item = db.query(Management).filter(Management.id == id).first()
    if not item:
        raise HTTPException(404)
    db.delete(item)
    db.commit()
    return {"message": "O'chirildi"}

@router.get("/structure", response_model=List[StructureResponse])
def list_structure(lang: Literal["uz", "ru", "en"] = Query("uz"), search: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Structure)
    if search:
        query = query.filter(getattr(Structure, f"title_{lang}").ilike(f"%{search}%"))
    return [
        StructureResponse(
            id=i.id,
            title=getattr(i, f"title_{lang}"),
            pdf_url=i.pdf_url,
            created_at=i.created_at,
            updated_at=i.updated_at
        ) for i in query.all()
    ]

@router.post("/structure", response_model=StructureResponse)
def create_structure(title_uz: str = Form(...), title_ru: str = Form(...), title_en: str = Form(...), pdf_file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(admin_required)):
    pdf_url = save_file(pdf_file) if pdf_file else None
    item = Structure(title_uz=title_uz, title_ru=title_ru, title_en=title_en, pdf_url=pdf_url)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.put("/structure/{id}", response_model=StructureResponse)
def update_structure(id: int, title_uz: Optional[str] = Form(None), title_ru: Optional[str] = Form(None), title_en: Optional[str] = Form(None), pdf_file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(admin_required)):
    item = db.query(Structure).filter(Structure.id == id).first()
    if not item:
        raise HTTPException(404)
    if title_uz: item.title_uz = title_uz
    if title_ru: item.title_ru = title_ru
    if title_en: item.title_en = title_en
    if pdf_file: item.pdf_url = save_file(pdf_file)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/structure/{id}")
def delete_structure(id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    item = db.query(Structure).filter(Structure.id == id).first()
    if not item:
        raise HTTPException(404)
    db.delete(item)
    db.commit()
    return {"message": "O'chirildi"}

@router.get("/structural-divisions", response_model=List[StructuralDivisionResponse])
def list_structural_divisions(lang: Literal["uz", "ru", "en"] = Query("uz"), search: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(StructuralDivision)
    if search:
        query = query.filter(getattr(StructuralDivision, f"title_{lang}").ilike(f"%{search}%"))
    return [
        StructuralDivisionResponse(
            id=i.id,
            title=getattr(i, f"title_{lang}"),
            head_full_name=i.head_full_name,
            phone=i.phone,
            email=i.email,
            profile_image=i.profile_image,
            created_at=i.created_at,
            updated_at=i.updated_at
        ) for i in query.all()
    ]

@router.post("/structural-divisions", response_model=StructuralDivisionResponse)
def create_structural_division(title_uz: str = Form(...), title_ru: str = Form(...), title_en: str = Form(...), head_full_name: str = Form(...), phone: Optional[str] = Form(None), email: Optional[str] = Form(None), profile_image: Optional[UploadFile] = File(None), db: Session = Depends(get_db), user=Depends(admin_required)):
    image_url = save_file(profile_image) if profile_image else None
    item = StructuralDivision(title_uz=title_uz, title_ru=title_ru, title_en=title_en, head_full_name=head_full_name, phone=phone, email=email, profile_image=image_url)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.put("/structural-divisions/{id}", response_model=StructuralDivisionResponse)
def update_structural_division(id: int, title_uz: Optional[str] = Form(None), title_ru: Optional[str] = Form(None), title_en: Optional[str] = Form(None), head_full_name: Optional[str] = Form(None), phone: Optional[str] = Form(None), email: Optional[str] = Form(None), profile_image: Optional[UploadFile] = File(None), db: Session = Depends(get_db), user=Depends(admin_required)):
    item = db.query(StructuralDivision).filter(StructuralDivision.id == id).first()
    if not item:
        raise HTTPException(404)
    if title_uz: item.title_uz = title_uz
    if title_ru: item.title_ru = title_ru
    if title_en: item.title_en = title_en
    if head_full_name: item.head_full_name = head_full_name
    if phone: item.phone = phone
    if email: item.email = email
    if profile_image: item.profile_image = save_file(profile_image)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/structural-divisions/{id}")
def delete_structural_division(id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    item = db.query(StructuralDivision).filter(StructuralDivision.id == id).first()
    if not item:
        raise HTTPException(404)
    db.delete(item)
    db.commit()
    return {"message": "O'chirildi"}

@router.get("/vacancies", response_model=PaginatedResponse[VacancyResponse])
def list_vacancies(page: int = 1, size: int = 10, lang: Literal["uz", "ru", "en"] = Query("uz"), search: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Vacancy)
    if search:
        query = query.filter(getattr(Vacancy, f"title_{lang}").ilike(f"%{search}%"))
    result = paginate(query.order_by(Vacancy.created_at.desc()), page, size)
    return PaginatedResponse(
        items=[
            VacancyResponse(
                id=i.id,
                title=getattr(i, f"title_{lang}"),
                description=getattr(i, f"description_{lang}"),
                requirements=getattr(i, f"requirements_{lang}"),
                deadline=i.deadline,
                contact_email=i.contact_email,
                attachment=i.attachment,
                is_active=bool(i.is_active),
                created_at=i.created_at,
                updated_at=i.updated_at
            ) for i in result.items
        ],
        total=result.total,
        page=page,
        size=size,
        pages=result.pages
    )

@router.post("/vacancies", response_model=VacancyResponse)
def create_vacancy(title_uz: str = Form(...), title_ru: str = Form(...), title_en: str = Form(...), description_uz: str = Form(...), description_ru: str = Form(...), description_en: str = Form(...), requirements_uz: str = Form(...), requirements_ru: str = Form(...), requirements_en: str = Form(...), deadline: Optional[datetime] = Form(None), contact_email: str = Form(...), is_active: Optional[bool] = Form(True), attachment: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(admin_required)):
    file_url = save_file(attachment) if attachment else None
    item = Vacancy(title_uz=title_uz, title_ru=title_ru, title_en=title_en, description_uz=description_uz, description_ru=description_ru, description_en=description_en, requirements_uz=requirements_uz, requirements_ru=requirements_ru, requirements_en=requirements_en, deadline=deadline, contact_email=contact_email, attachment=file_url, is_active=is_active)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.put("/vacancies/{id}", response_model=VacancyResponse)
def update_vacancy(id: int, title_uz: Optional[str] = Form(None), title_ru: Optional[str] = Form(None), title_en: Optional[str] = Form(None), description_uz: Optional[str] = Form(None), description_ru: Optional[str] = Form(None), description_en: Optional[str] = Form(None), requirements_uz: Optional[str] = Form(None), requirements_ru: Optional[str] = Form(None), requirements_en: Optional[str] = Form(None), deadline: Optional[datetime] = Form(None), contact_email: Optional[str] = Form(None), is_active: Optional[bool] = Form(None), attachment: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(admin_required)):
    item = db.query(Vacancy).filter(Vacancy.id == id).first()
    if not item:
        raise HTTPException(404)
    if title_uz: item.title_uz = title_uz
    if title_ru: item.title_ru = title_ru
    if title_en: item.title_en = title_en
    if description_uz: item.description_uz = description_uz
    if description_ru: item.description_ru = description_ru
    if description_en: item.description_en = description_en
    if requirements_uz: item.requirements_uz = requirements_uz
    if requirements_ru: item.requirements_ru = requirements_ru
    if requirements_en: item.requirements_en = requirements_en
    if deadline: item.deadline = deadline
    if contact_email: item.contact_email = contact_email
    if is_active is not None: item.is_active = is_active
    if attachment: item.attachment = save_file(attachment)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/vacancies/{id}")
def delete_vacancy(id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    item = db.query(Vacancy).filter(Vacancy.id == id).first()
    if not item:
        raise HTTPException(404)
    db.delete(item)
    db.commit()
    return {"message": "O'chirildi"}
