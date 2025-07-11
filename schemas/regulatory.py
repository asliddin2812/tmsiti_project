from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ShnqBase(BaseModel):
    subsystem: str = Field(..., min_length=1, max_length=50)
    group: str = Field(..., min_length=1, max_length=20)
    code: str = Field(..., max_length=20, pattern="^[a-zA-Z0-9]+$")
    title_uz: str = Field(..., min_length=1, max_length=255)
    title_ru: Optional[str] = Field(None, max_length=255)
    title_en: Optional[str] = Field(None, max_length=255)
    link: Optional[str] = Field(None, max_length=500)

class ShnqCreate(ShnqBase):
    pass

class ShnqUpdate(BaseModel):
    subsystem: Optional[str] = Field(None, min_length=3, max_length=50)
    group: Optional[str] = Field(None, min_length=2, max_length=20)
    code: Optional[str] = Field(None, max_length=20, pattern="^[a-zA-Z0-9]+$")
    title_uz: Optional[str] = Field(None, min_length=1, max_length=255)
    title_ru: Optional[str] = Field(None, max_length=255)
    title_en: Optional[str] = Field(None, max_length=255)
    link: Optional[str] = Field(None, max_length=500)

class ShnqResponse(BaseModel):
    id: int
    subsystem: str
    group: str
    code: str
    title: str  # lang asosida keladi (title_uz, title_ru yoki title_en o‘rniga)
    link: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class StandardBase(BaseModel):
    code: str = Field(..., max_length=20, pattern="^[a-zA-Z0-9]+$")
    title_uz: str = Field(..., min_length=1, max_length=255)
    title_ru: Optional[str] = Field(None, max_length=255)
    title_en: Optional[str] = Field(None, max_length=255)
    description_uz: str = Field(..., min_length=1)
    description_ru: Optional[str] = Field(None)
    description_en: Optional[str] = Field(None)
    link: Optional[str] = Field(None, max_length=500)

class StandardCreate(StandardBase):
    pass

class StandardUpdate(BaseModel):
    code: Optional[str] = Field(None, max_length=20, pattern="^[a-zA-Z0-9]+$")
    title_uz: Optional[str] = Field(None, min_length=1, max_length=255)
    title_ru: Optional[str] = Field(None, max_length=255)
    title_en: Optional[str] = Field(None, max_length=255)
    description_uz: Optional[str] = Field(None, min_length=1)
    description_ru: Optional[str] = Field(None)
    description_en: Optional[str] = Field(None)
    link: Optional[str] = Field(None, max_length=500)

class StandardResponse(StandardBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

class BuildingRegulationBase(BaseModel):
    number: str = Field(..., min_length=1, max_length=50)
    code: str = Field(..., max_length=20, pattern="^[a-zA-Z0-9]+$")
    title_uz: str = Field(..., min_length=1, max_length=255)
    title_ru: Optional[str] = Field(None, max_length=255)
    title_en: Optional[str] = Field(None, max_length=255)
    link: Optional[str] = Field(None, max_length=500)

class BuildingRegulationCreate(BuildingRegulationBase):
    pass

class BuildingRegulationUpdate(BaseModel):
    number: Optional[str] = Field(None, min_length=1, max_length=50)
    code: Optional[str] = Field(None, max_length=20, pattern="^[a-zA-Z0-9]+$")
    title_uz: Optional[str] = Field(None, min_length=1, max_length=255)
    title_ru: Optional[str] = Field(None, max_length=255)
    title_en: Optional[str] = Field(None, max_length=255)
    link: Optional[str] = Field(None, max_length=500)

class BuildingRegulationResponse(BaseModel):
    id: int
    code: str
    number: str
    title: str
    link: Optional[str] = None
    created_at: datetime


    class Config:
        from_attributes = True
        populate_by_name = True

class SmetaResursNormBase(BaseModel):
    srn_code: str = Field(..., max_length=20, pattern="^[a-zA-Z0-9]+$")
    srn_title_uz: str = Field(..., min_length=1, max_length=255)
    srn_title_ru: Optional[str] = Field(None, max_length=255)
    srn_title_en: Optional[str] = Field(None, max_length=255)
    main_shnq_code: Optional[str] = Field(None, max_length=20, pattern="^[a-zA-Z0-9]+$")
    main_shnq_title_uz: Optional[str] = Field(None, max_length=255)
    main_shnq_title_ru: Optional[str] = Field(None, max_length=255)
    main_shnq_title_en: Optional[str] = Field(None, max_length=255)
    additional_shnqs: Optional[str] = Field(None)
    file: Optional[str] = Field(None, max_length=500)

class SmetaResursNormCreate(SmetaResursNormBase):
    pass

class SmetaResursNormUpdate(BaseModel):
    srn_code: Optional[str] = Field(None, max_length=20, pattern="^[a-zA-Z0-9]+$")
    srn_title_uz: Optional[str] = Field(None, min_length=1, max_length=255)
    srn_title_ru: Optional[str] = Field(None, max_length=255)
    srn_title_en: Optional[str] = Field(None, max_length=255)
    main_shnq_code: Optional[str] = Field(None, max_length=20, pattern="^[a-zA-Z0-9]+$")
    main_shnq_title_uz: Optional[str] = Field(None, max_length=255)
    main_shnq_title_ru: Optional[str] = Field(None, max_length=255)
    main_shnq_title_en: Optional[str] = Field(None, max_length=255)
    additional_shnqs: Optional[str] = Field(None)
    file: Optional[str] = Field(None, max_length=500)

class SmetaResursNormResponse(SmetaResursNormBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

class TechnicalRegulationBase(BaseModel):
    code: str = Field(..., max_length=20, pattern="^[a-zA-Z0-9]+$")
    title_uz: str = Field(..., min_length=1, max_length=255)
    title_ru: Optional[str] = Field(None, max_length=255)
    title_en: Optional[str] = Field(None, max_length=255)
    description_uz: Optional[str]
    description_ru: Optional[str]
    description_en: Optional[str]
    link: Optional[str] = Field(None, max_length=500)
    file: Optional[str] = None

class TechnicalRegulationCreate(TechnicalRegulationBase):
    pass

class TechnicalRegulationUpdate(BaseModel):
    code: str = Field(..., max_length=20, pattern="^[a-zA-Z0-9]+$")
    title_uz: Optional[str]
    title_ru: Optional[str]
    title_en: Optional[str]
    description_uz: Optional[str]
    description_ru: Optional[str]
    description_en: Optional[str]
    link: Optional[str]
    file: Optional[str]

class TechnicalRegulationResponse(BaseModel):
    id: int
    code: str
    title: str
    description: Optional[str]
    link: Optional[str]
    file: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

class ReferenceBase(BaseModel):
    number: str = Field(..., min_length=1, max_length=50)
    title_uz: str = Field(..., min_length=1, max_length=255)
    title_ru: Optional[str] = Field(None, max_length=255)
    title_en: Optional[str] = Field(None, max_length=255)
    link: Optional[str] = Field(None, max_length=500)

class ReferenceCreate(ReferenceBase):
    pass

class ReferenceUpdate(BaseModel):
    number: Optional[str] = Field(None, min_length=1, max_length=50)
    title_uz: Optional[str] = Field(None, min_length=1, max_length=255)
    title_ru: Optional[str] = Field(None, max_length=255)
    title_en: Optional[str] = Field(None, max_length=255)
    link: Optional[str] = Field(None, max_length=500)

class ReferenceResponse(ReferenceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True
