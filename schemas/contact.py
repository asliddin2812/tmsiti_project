from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

API_PREFIX = "/api/v1"

class ContactResponse(BaseModel):
    id: int
    fio: str
    email: EmailStr
    phone: str
    category_uz: Optional[str]
    category_ru: Optional[str]
    category_en: Optional[str]
    message_uz: Optional[str]
    message_ru: Optional[str]
    message_en: Optional[str]
    file: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class ContactResponseDynamic(BaseModel):
    fio: str
    email: EmailStr
    phone: str
    category: str
    message: str
    file: Optional[str] = None

    class Config:
        from_attributes = True

def transform_contact_for_response(contact, lang: str):
    category = {
        "uz": contact.category_uz or "",
        "ru": contact.category_ru or "",
        "en": contact.category_en or ""
    }[lang]

    message = {
        "uz": contact.message_uz or "",
        "ru": contact.message_ru or "",
        "en": contact.message_en or ""
    }[lang]

    file_url = f"{API_PREFIX}/contact/file/{contact.file.split('/')[-1]}" if contact.file else None

    return {
        "fio": contact.fio,
        "email": contact.email,
        "phone": contact.phone,
        "category": category,
        "message": message,
        "file": file_url
    }
