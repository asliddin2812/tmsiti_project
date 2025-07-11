from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile, Form
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Dict, Any, Optional
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from core.database import get_db
from utils.dependencies import admin_required
from utils.pagination import paginate, PaginatedResponse
from models.regulatory import *
from schemas.regulatory import *

import os
from uuid import uuid4

router = APIRouter(prefix="/regulatory", tags=["Me'yoriy hujjatlar"])

def get_localized_field(item: Any, field_name: str, lang: str) -> str:
    return (
        getattr(item, f"{field_name}_{lang}", None)
        or getattr(item, f"{field_name}_uz", None)
        or ""
    )

from typing import Any, Dict

def transform_item_for_response(item: Any, lang: str, field_mappings: Dict[str, str]) -> Dict[str, Any]:
    result = {}

    for attr in dir(item):
        if (
            not attr.startswith("_")
            and not attr.endswith(("_uz", "_ru", "_en"))
            and attr not in ["metadata", "registry"]
        ):
            value = getattr(item, attr, None)
            if not callable(value):
                result[attr] = value

    for response_field, base_field in field_mappings.items():
        localized_field = f"{base_field}_{lang}"
        fallback_field = f"{base_field}_uz"
        result[response_field] = getattr(item, localized_field, None) or getattr(item, fallback_field, None) or ""

    return result



def create_item(db: Session, model, schema):
    try:
        item = model(**schema.dict())
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=422, detail="Bu code yoki boshqa noyob maydon allaqachon mavjud")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Xato yuz berdi: {str(e)}")

def update_item(db: Session, model, id: int, schema):
    item = db.query(model).filter(model.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    for k, v in schema.dict(exclude_unset=True).items():
        setattr(item, k, v)
    try:
        db.commit()
        db.refresh(item)
        return item
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=422, detail="Bu code yoki boshqa noyob maydon allaqachon mavjud")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Xato yuz berdi: {str(e)}")

def delete_item(db: Session, model, id: int):
    item = db.query(model).filter(model.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    db.delete(item)
    db.commit()
    return {"message": "O'chirildi"}

def apply_search(query, model, search: Optional[str], fields: list):
    if search:
        filters = [getattr(model, field).ilike(f"%{search}%") for field in fields]
        return query.filter(or_(*filters))
    return query

def save_file(file: UploadFile, upload_dir: str = "uploads") -> str:
    try:
        os.makedirs(upload_dir, exist_ok=True)
        filename = f"{uuid4().hex}_{file.filename}"
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Faylni saqlashda xato: {str(e)}")

# SHNQ
@router.get("/shnq", response_model=PaginatedResponse[Dict[str, Any]])
def list_shnq(
    page: int = 1,
    size: int = 10,
    lang: str = Query("uz"),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    query = apply_search(db.query(Shnq), Shnq, search, ["title_uz", "title_ru", "title_en"])
    paginated = paginate(query, page, size)
    paginated.items = [transform_item_for_response(item, lang, {"title": "title"}) for item in paginated.items]
    return paginated
@router.post("/shnq", response_model=ShnqResponse)
def create_shnq(
    data: ShnqCreate = Depends(),
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    return create_item(db, Shnq, data)

@router.put("/shnq/{id}", response_model=ShnqResponse)
def update_shnq(id: int, data: ShnqUpdate, db: Session = Depends(get_db), user=Depends(admin_required)):
    item = update_item(db, Shnq, id, data)
    return transform_item_for_response(item, "uz", {"title": "title"})

@router.delete("/shnq/{id}")
def delete_shnq(id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    return delete_item(db, Shnq, id)

# Standards
from typing import Dict, Any


@router.get("/standards", response_model=PaginatedResponse[Dict[str, Any]])
def list_standards(
        page: int = 1,
        size: int = 10,
        lang: str = Query("uz"),
        search: str = Query(None),
        db: Session = Depends(get_db)
):
    query = apply_search(
        db.query(Standard),
        Standard,
        search,
        ["title_uz", "title_ru", "title_en", "description_uz", "description_ru", "description_en"]
    )
    paginated = paginate(query, page, size)

    # Tilga moslab title va description qaytarish
    paginated.items = [
        transform_item_for_response(item, lang, {
            "title": "title",
            "description": "description"
        }) for item in paginated.items
    ]

    return paginated


@router.post("/standards", response_model=StandardResponse)
def create_standard(
    data: StandardCreate = Depends(),
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    return create_item(db, Standard, data)

@router.put("/standards/{id}", response_model=StandardResponse)
def update_standard(id: int, data: StandardUpdate, db: Session = Depends(get_db), user=Depends(admin_required)):
    item = update_item(db, Standard, id, data)
    return transform_item_for_response(item, "uz", {"title": "title", "description": "description"})

@router.delete("/standards/{id}")
def delete_standard(id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    return delete_item(db, Standard, id)

# SRN
@router.get("/srn", response_model=PaginatedResponse[Dict[str, Any]])
def list_srn(
    page: int = 1,
    size: int = 10,
    lang: str = Query("uz"),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    query = apply_search(
        db.query(SmetaResursNorm),
        SmetaResursNorm,
        search,
        ["srn_title_uz", "srn_title_ru", "srn_title_en", "main_shnq_title_uz", "main_shnq_title_ru", "main_shnq_title_en"]
    )
    paginated = paginate(query, page, size)
    paginated.items = [
        transform_item_for_response(item, lang, {
            "srn_title": "srn_title",
            "main_shnq_title": "main_shnq_title"
        }) for item in paginated.items
    ]
    return paginated


@router.post("/srn", response_model=SmetaResursNormResponse)
def create_srn(
    data: SmetaResursNormCreate = Depends(),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    if file:
        data.file = save_file(file)
    return create_item(db, SmetaResursNorm, data)

@router.put("/srn/{id}", response_model=SmetaResursNormResponse)
def update_srn(
    id: int,
    data: SmetaResursNormUpdate = Depends(),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    if file:
        data.file = save_file(file)
    item = update_item(db, SmetaResursNorm, id, data)
    return transform_item_for_response(item, "uz", {"srn_title": "srn_title", "main_shnq_title": "main_shnq_title"})

@router.delete("/srn/{id}")
def delete_srn(id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    return delete_item(db, SmetaResursNorm, id)

# Building Regulations
@router.get("/building-regulations", response_model=PaginatedResponse[BuildingRegulationResponse])
def list_buildings(
    page: int = 1,
    size: int = 10,
    lang: str = Query("uz"),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    search_fields = [f"title_{lang}"]
    query = apply_search(db.query(BuildingRegulation), BuildingRegulation, search, search_fields)
    paginated = paginate(query, page, size)
    paginated.items = [
        transform_item_for_response(item, lang, {"title": "title"})
        for item in paginated.items
    ]
    return paginated




@router.post("/building-regulations", response_model=BuildingRegulationResponse)
def create_building(
    data: BuildingRegulationCreate,
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    item = create_item(db, BuildingRegulation, data)
    return transform_item_for_response(item, "uz", {"title": "title"})



@router.put("/building-regulations/{id}", response_model=BuildingRegulationResponse)
def update_building(
    id: int,
    data: BuildingRegulationUpdate,
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    item = update_item(db, BuildingRegulation, id, data)
    return transform_item_for_response(item, "uz", {"title": "title"})


@router.delete("/building-regulations/{id}")
def delete_building(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    return delete_item(db, BuildingRegulation, id)

# Technical Regulations
@router.get("/technical", response_model=list[TechnicalRegulationResponse])
def list_technical(
    db: Session = Depends(get_db),
    lang: str = Query("uz", enum=["uz", "ru", "en"])
):
    items = db.query(TechnicalRegulation).all()
    return [
        transform_item_for_response(item, lang, {"title": "title", "description": "description"})
        for item in items
    ]

# CREATE
@router.post("/technical", response_model=TechnicalRegulationResponse)
def create_technical(
    data: TechnicalRegulationCreate = Depends(),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    existing = db.query(TechnicalRegulation).filter(TechnicalRegulation.code == data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu code bilan yozuv allaqachon mavjud")

    if file:
        data.file = save_file(file)
    obj = TechnicalRegulation(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return transform_item_for_response(obj, "uz", {"title": "title", "description": "description"})

# UPDATE
@router.put("/technical/{id}", response_model=TechnicalRegulationResponse)
def update_technical(
    id: int,
    data: TechnicalRegulationUpdate = Depends(),
    file: UploadFile=File(...),
    db: Session = Depends(get_db)
):
    item = db.query(TechnicalRegulation).get(id)
    if not item:
        raise HTTPException(404, detail="Topilmadi")
    if file:
        data.file = save_file(file)
    for field, value in data.dict(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return transform_item_for_response(item, "uz", {"title": "title", "description": "description"})

# DELETE
@router.delete("/technical/{id}")
def delete_technical(id: int, db: Session = Depends(get_db)):
    item = db.query(TechnicalRegulation).get(id)
    if not item:
        raise HTTPException(404, detail="Topilmadi")
    db.delete(item)
    db.commit()
    return {"detail": "O‘chirildi"}
# Reference
@router.get("/reference")
def list_reference(
    page: int = 1,
    size: int = 10,
    lang: str = Query("uz"),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = apply_search(db.query(Reference), Reference, search, ["title_uz", "title_ru", "title_en"])
    paginated = paginate(query, page, size)
    paginated.items = [
        transform_item_for_response(item, lang, {"title": "title"})
        for item in paginated.items
    ]
    return paginated


@router.post("/reference", response_model=ReferenceResponse)
def create_reference(
    number: str = Form(...),
    title_uz: str = Form(...),
    title_ru: Optional[str] = Form(None),
    title_en: Optional[str] = Form(None),
    link: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    item = Reference(
        number=number,
        title_uz=title_uz,
        title_ru=title_ru,
        title_en=title_en,
        link=link
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/reference/{id}", response_model=ReferenceResponse)
def update_reference(
    id: int,
    number: Optional[str] = Form(None),
    title_uz: Optional[str] = Form(None),
    title_ru: Optional[str] = Form(None),
    title_en: Optional[str] = Form(None),
    link: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    item = db.query(Reference).filter(Reference.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    if number is not None:
        item.number = number
    if title_uz is not None:
        item.title_uz = title_uz
    if title_ru is not None:
        item.title_ru = title_ru
    if title_en is not None:
        item.title_en = title_en
    if link is not None:
        item.link = link

    db.commit()
    db.refresh(item)
    return item


@router.delete("/reference/{id}")
def delete_reference(id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    return delete_item(db, Reference, id)
