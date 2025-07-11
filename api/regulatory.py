from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Dict, Any, Optional

from core.database import get_db
from utils.dependencies import admin_required
from utils.pagination import paginate, PaginatedResponse

from models.regulatory import *
from schemas.regulatory import *

router = APIRouter(prefix="/regulatory", tags=["Me'yoriy hujjatlar"])


def get_localized_field(item: Any, field_name: str, lang: str) -> str:
    return (
        getattr(item, f"{field_name}_{lang}", None)
        or getattr(item, f"{field_name}_uz", None)
        or ""
    )


def transform_item_for_response(item: Any, lang: str, field_mappings: Dict[str, str]) -> Dict[str, Any]:
    result = {}
    for attr in dir(item):
        if not attr.startswith("_") and not attr.endswith(("_uz", "_ru", "_en")):
            if hasattr(item, attr) and not callable(getattr(item, attr)):
                result[attr] = getattr(item, attr)
    for response_field, db_field in field_mappings.items():
        result[response_field] = get_localized_field(item, db_field, lang)
    return result


def create_item(db, model, schema):
    item = model(**schema.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(db, model, id, schema):
    item = db.query(model).filter(model.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    for k, v in schema.dict(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item


def delete_item(db, model, id):
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

# SHNQ
@router.get("/shnq", response_model=PaginatedResponse[ShnqResponse])
def list_shnq(page: int = 1, size: int = 10, lang: str = Query("uz"), search: str = Query(None), db: Session = Depends(get_db)):
    query = apply_search(db.query(Shnq), Shnq, search, ["title_uz", "title_ru", "title_en"])
    paginated = paginate(query, page, size)
    paginated.items = [transform_item_for_response(item, lang, {"title": "title"}) for item in paginated.items]
    return paginated

@router.post("/api/v1/regulatory/shnq", response_model=ShnqResponse)
async def create_shnq(shnq: ShnqCreate, db: Session = Depends(get_db)):
    try:
        db_shnq = Shnq(
            subsystem=shnq.subsystem,
            group=shnq.group,
            code=shnq.code,
            title_uz=shnq.title_uz,
            title_ru=shnq.title_ru,
            title_en=shnq.title_en,
            link=shnq.link
        )
        db.add(db_shnq)
        db.commit()
        db.refresh(db_shnq)
        return db_shnq
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating SHNQ: {str(e)}")


@router.put("/shnq/{id}", response_model=ShnqResponse)
def update_shnq(id: int, data: ShnqUpdate, db: Session = Depends(get_db), user=Depends(admin_required)):
    item = update_item(db, Shnq, id, data)
    return transform_item_for_response(item, "uz", {"title": "title"})

@router.delete("/shnq/{id}")
def delete_shnq(id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    return delete_item(db, Shnq, id)

# Standards
@router.get("/standards", response_model=PaginatedResponse[StandardResponse])
def list_standards(page: int = 1, size: int = 10, lang: str = Query("uz"), search: str = Query(None), db: Session = Depends(get_db)):
    query = apply_search(db.query(Standard), Standard, search, ["title_uz", "title_ru", "title_en", "description_uz", "description_ru", "description_en"])
    paginated = paginate(query, page, size)
    paginated.items = [transform_item_for_response(item, lang, {"title": "title", "description": "description"}) for item in paginated.items]
    return paginated

@router.post("/api/v1/regulatory/standard", response_model=StandardResponse)
async def create_standard(standard: StandardCreate, db: Session = Depends(get_db)):
    try:
        db_standard = Standard(**standard.dict())
        db.add(db_standard)
        db.commit()
        db.refresh(db_standard)
        return db_standard
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating Standard: {str(e)}")

@router.put("/standards/{id}", response_model=StandardResponse)
def update_standard(id: int, data: StandardUpdate, db: Session = Depends(get_db), user=Depends(admin_required)):
    item = update_item(db, Standard, id, data)
    return transform_item_for_response(item, "uz", {"title": "title", "description": "description"})

@router.delete("/standards/{id}")
def delete_standard(id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    return delete_item(db, Standard, id)

# SRN
@router.get("/srn", response_model=PaginatedResponse[SmetaResursNormResponse])
def list_srn(page: int = 1, size: int = 10, lang: str = Query("uz"), search: str = Query(None), db: Session = Depends(get_db)):
    query = apply_search(db.query(SmetaResursNorm), SmetaResursNorm, search, ["srn_title_uz", "srn_title_ru", "srn_title_en", "main_shnq_title_uz", "main_shnq_title_ru", "main_shnq_title_en"])
    paginated = paginate(query, page, size)
    paginated.items = [transform_item_for_response(item, lang, {"srn_title": "srn_title", "main_shnq_title": "main_shnq_title"}) for item in paginated.items]
    return paginated

@router.post("/srn", response_model=SmetaResursNormResponse)
def create_srn(data: SmetaResursNormCreate = Depends(), file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(admin_required)):
    item = create_item(db, SmetaResursNorm, data)
    return transform_item_for_response(item, "uz", {"srn_title": "srn_title", "main_shnq_title": "main_shnq_title"})

@router.put("/srn/{id}", response_model=SmetaResursNormResponse)
def update_srn(id: int, data: SmetaResursNormUpdate, db: Session = Depends(get_db), user=Depends(admin_required)):
    item = update_item(db, SmetaResursNorm, id, data)
    return transform_item_for_response(item, "uz", {"srn_title": "srn_title", "main_shnq_title": "main_shnq_title"})

@router.delete("/srn/{id}")
def delete_srn(id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    return delete_item(db, SmetaResursNorm, id)

# Building Regulations
@router.get("/building-regulations", response_model=PaginatedResponse[BuildingRegulationResponse])
def list_buildings(page: int = 1, size: int = 10, lang: str = Query("uz"), search: str = Query(None), db: Session = Depends(get_db)):
    query = apply_search(db.query(BuildingRegulation), BuildingRegulation, search, ["title_uz", "title_ru", "title_en"])
    paginated = paginate(query, page, size)
    paginated.items = [transform_item_for_response(item, lang, {"title": "title"}) for item in paginated.items]
    return paginated

@router.post("/building-regulations", response_model=BuildingRegulationResponse)
def create_building(data: BuildingRegulationCreate = Depends(), file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(admin_required)):
    item = create_item(db, BuildingRegulation, data)
    return transform_item_for_response(item, "uz", {"title": "title"})

@router.put("/building-regulations/{id}", response_model=BuildingRegulationResponse)
def update_building(id: int, data: BuildingRegulationUpdate, db: Session = Depends(get_db), user=Depends(admin_required)):
    item = update_item(db, BuildingRegulation, id, data)
    return transform_item_for_response(item, "uz", {"title": "title"})

@router.delete("/building-regulations/{id}")
def delete_building(id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    return delete_item(db, BuildingRegulation, id)

# Technical Regulations
@router.get("/technical", response_model=PaginatedResponse[TechnicalRegulationResponse])
def list_technical(page: int = 1, size: int = 10, lang: str = Query("uz"), search: str = Query(None), db: Session = Depends(get_db)):
    query = apply_search(db.query(TechnicalRegulation), TechnicalRegulation, search, ["title_uz", "title_ru", "title_en"])
    paginated = paginate(query, page, size)
    paginated.items = [transform_item_for_response(item, lang, {"title": "title", "description": "description"}) for item in paginated.items]
    return paginated

@router.post("/technical", response_model=TechnicalRegulationResponse)
def create_technical(data: TechnicalRegulationCreate = Depends(), file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(admin_required)):
    item = create_item(db, TechnicalRegulation, data)
    return transform_item_for_response(item, "uz", {"title": "title", "description": "description"})

@router.put("/technical/{id}", response_model=TechnicalRegulationResponse)
def update_technical(id: int, data: TechnicalRegulationUpdate, db: Session = Depends(get_db), user=Depends(admin_required)):
    item = update_item(db, TechnicalRegulation, id, data)
    return transform_item_for_response(item, "uz", {"title": "title", "description": "description"})

@router.delete("/technical/{id}")
def delete_technical(id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    return delete_item(db, TechnicalRegulation, id)

# Reference
@router.get("/reference", response_model=PaginatedResponse[ReferenceResponse])
def list_reference(page: int = 1, size: int = 10, lang: str = Query("uz"), search: str = Query(None), db: Session = Depends(get_db)):
    query = apply_search(db.query(Reference), Reference, search, ["title_uz", "title_ru", "title_en"])
    paginated = paginate(query, page, size)
    paginated.items = [transform_item_for_response(item, lang, {"title": "title"}) for item in paginated.items]
    return paginated

@router.post("/reference", response_model=ReferenceResponse)
def create_reference(data: ReferenceCreate = Depends(), file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(admin_required)):
    item = create_item(db, Reference, data)
    return transform_item_for_response(item, "uz", {"title": "title"})

@router.put("/reference/{id}", response_model=ReferenceResponse)
def update_reference(id: int, data: ReferenceUpdate, db: Session = Depends(get_db), user=Depends(admin_required)):
    item = update_item(db, Reference, id, data)
    return transform_item_for_response(item, "uz", {"title": "title"})

@router.delete("/reference/{id}")
def delete_reference(id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    return delete_item(db, Reference, id)
