from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ========== ABOUT ==========
class AboutBase(BaseModel):
    content_uz: str
    content_ru: str
    content_en: str
    pdf_url: Optional[str] = None

class AboutCreate(AboutBase):
    pass

class AboutUpdate(BaseModel):
    content_uz: Optional[str]
    content_ru: Optional[str]
    content_en: Optional[str]
    pdf_url: Optional[str]

class AboutResponse(AboutBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ========== MANAGEMENT ==========
class ManagementBase(BaseModel):
    full_name: str
    position_uz: str
    position_ru: str
    position_en: str
    profile_image: Optional[str]
    reception_days: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    specialization_uz: Optional[str]
    specialization_ru: Optional[str]
    specialization_en: Optional[str]
    order_index: Optional[int] = 0

class ManagementCreate(ManagementBase):
    pass

class ManagementUpdate(BaseModel):
    full_name: Optional[str]
    position_uz: Optional[str]
    position_ru: Optional[str]
    position_en: Optional[str]
    profile_image: Optional[str]
    reception_days: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    specialization_uz: Optional[str]
    specialization_ru: Optional[str]
    specialization_en: Optional[str]
    order_index: Optional[int]

class ManagementResponse(ManagementBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ========== STRUCTURE ==========
class StructureBase(BaseModel):
    title_uz: str
    title_ru: str
    title_en: str
    pdf_url: Optional[str]

class StructureCreate(StructureBase):
    pass

class StructureUpdate(BaseModel):
    title_uz: Optional[str]
    title_ru: Optional[str]
    title_en: Optional[str]
    pdf_url: Optional[str]

class StructureResponse(StructureBase):
    id: int
    title_uz: str
    title_ru: str
    title_en: str
    pdf_url: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ========== STRUCTURAL DIVISIONS ==========
class StructuralDivisionBase(BaseModel):
    title_uz: str
    title_ru: str
    title_en: str
    head_full_name: str
    phone: Optional[str]
    email: Optional[EmailStr]
    profile_image: Optional[str]

class StructuralDivisionCreate(StructuralDivisionBase):
    pass

class StructuralDivisionUpdate(BaseModel):
    title_uz: Optional[str]
    title_ru: Optional[str]
    title_en: Optional[str]
    head_full_name: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    profile_image: Optional[str]

class StructuralDivisionResponse(StructuralDivisionBase):
    id: int
    title_uz: str
    title_ru: str
    title_en: str
    head_full_name: str
    phone: Optional[str]
    email: Optional[EmailStr]
    profile_image: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ========== VACANCIES ==========
class VacancyBase(BaseModel):
    title_uz: str
    title_ru: str
    title_en: str
    description_uz: str
    description_ru: str
    description_en: str
    requirements_uz: str
    requirements_ru: str
    requirements_en: str
    deadline: Optional[datetime]
    contact_email: EmailStr
    attachment: Optional[str]
    is_active: Optional[bool] = True

class VacancyCreate(VacancyBase):
    pass

class VacancyUpdate(BaseModel):
    title_uz: Optional[str]
    title_ru: Optional[str]
    title_en: Optional[str]
    description_uz: Optional[str]
    description_ru: Optional[str]
    description_en: Optional[str]
    requirements_uz: Optional[str]
    requirements_ru: Optional[str]
    requirements_en: Optional[str]
    deadline: Optional[datetime]
    contact_email: Optional[EmailStr]
    attachment: Optional[str]
    is_active: Optional[bool]

class VacancyResponse(VacancyBase):
    id: int
    title_uz: str
    title_ru: str
    title_en: str
    description_uz: str
    description_ru: str
    description_en: str
    requirements_uz: str
    requirements_ru: str
    requirements_en: str
    deadline: Optional[datetime]
    contact_email: EmailStr
    attachment: Optional[str]
    is_active: Optional[bool]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True