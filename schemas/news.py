from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NewsBase(BaseModel):
    title_uz: str
    title_ru: str
    title_en: str
    content_uz: str
    content_ru: str
    content_en: str
    image: Optional[str] = None
    published_at: Optional[datetime] = None

class NewsCreate(NewsBase):
    pass

class NewsUpdate(BaseModel):
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    content_uz: Optional[str] = None
    content_ru: Optional[str] = None
    content_en: Optional[str] = None
    image: Optional[str] = None
    published_at: Optional[datetime] = None

class NewsResponse(BaseModel):
    id: int
    title: str
    content: str
    image: Optional[str]
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AntiCorruptionBase(BaseModel):
    title_uz: str
    title_ru: str
    title_en: str
    content_uz: str
    content_ru: str
    content_en: str
    file: Optional[str] = None

class AntiCorruptionCreate(AntiCorruptionBase):
    pass

class AntiCorruptionUpdate(BaseModel):
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    content_uz: Optional[str] = None
    content_ru: Optional[str] = None
    content_en: Optional[str] = None
    file: Optional[str] = None

class AntiCorruptionResponse(BaseModel):
    id: int
    title: str
    content: str
    file: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
