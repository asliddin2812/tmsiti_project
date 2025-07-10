from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ManagementSystemBase(BaseModel):
    title_uz: str
    title_ru: str
    title_en: str
    description_uz: str
    description_ru: str
    description_en: str

class ManagementSystemCreate(ManagementSystemBase):
    pass

class ManagementSystemUpdate(BaseModel):
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None

class ManagementSystemResponse(BaseModel):
    id: int
    pdf: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] = None
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True
