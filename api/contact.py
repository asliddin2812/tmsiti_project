from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import List, Literal, Optional
import os, shutil, uuid

from core.database import get_db
from utils.dependencies import admin_required
from models.contact import Contact
from schemas.contact import ContactResponse, ContactResponseDynamic, transform_contact_for_response
from utils.telegram import send_to_telegram

router = APIRouter(prefix="/contact", tags=["Bog'lanish"])

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("", response_model=ContactResponseDynamic)
async def create_contact(
    fio: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    category_uz: Optional[str] = Form(None),
    category_ru: Optional[str] = Form(None),
    category_en: Optional[str] = Form(None),
    message_uz: Optional[str] = Form(None),
    message_ru: Optional[str] = Form(None),
    message_en: Optional[str] = Form(None),
    file: UploadFile = File(None),
    lang: Literal["uz", "ru", "en"] = Query("uz"),
    db: Session = Depends(get_db)
):
    if lang == "uz" and (not category_uz or not message_uz):
        raise HTTPException(status_code=400, detail="category_uz va message_uz majburiy")
    if lang == "ru" and (not category_ru or not message_ru):
        raise HTTPException(status_code=400, detail="category_ru va message_ru majburiy")
    if lang == "en" and (not category_en or not message_en):
        raise HTTPException(status_code=400, detail="category_en va message_en majburiy")

    file_path = None
    if file and file.filename:
        ext = file.filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    contact = Contact(
        fio=fio,
        email=email,
        phone=phone,
        category_uz=category_uz,
        category_ru=category_ru,
        category_en=category_en,
        message_uz=message_uz,
        message_ru=message_ru,
        message_en=message_en,
        file=file_path
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)

    result = transform_contact_for_response(contact, lang)

    tg_msg = (
        f"📥 Yangi murojaat\n"
        f"👤 FIO: {result['fio']}\n"
        f"📧 Email: {result['email']}\n"
        f"📞 Tel: {result['phone']}\n"
        f"🗂 Kategoriya: {result['category']}\n"
        f"📝 Xabar: {result['message']}"
    )
    await send_to_telegram(tg_msg)

    return result

@router.get("", response_model=List[ContactResponse])
def get_all_contacts(
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    query = db.query(Contact)

    if search:
        filters = [
            Contact.fio.ilike(f"%{search}%"),
            Contact.email.ilike(f"%{search}%"),
            Contact.phone.ilike(f"%{search}%"),
            Contact.category_uz.ilike(f"%{search}%"),
            Contact.category_ru.ilike(f"%{search}%"),
            Contact.category_en.ilike(f"%{search}%")
        ]

        if search.isdigit():
            filters.append(Contact.id == int(search))

        query = query.filter(or_(*filters))

    contacts = query.order_by(Contact.created_at.desc()).all()
    return contacts

@router.delete("/{id}")
def delete_contact(id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    contact = db.query(Contact).get(id)
    if not contact:
        raise HTTPException(status_code=404, detail="Murojaat topilmadi")
    db.delete(contact)
    db.commit()
    return {"message": "O‘chirildi"}
