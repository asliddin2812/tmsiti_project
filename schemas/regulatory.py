from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# === SHNQ ===
class ShnqBase(BaseModel):
    subsystem: str
    group: str
    code: str
    title_uz: str
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    link: Optional[str] = None

class ShnqCreate(ShnqBase):
    pass

class ShnqUpdate(BaseModel):
    subsystem: Optional[str] = None
    group: Optional[str] = None
    code: Optional[str] = None
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    link: Optional[str] = None

class ShnqResponse(ShnqBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

# === STANDARD ===
class StandardBase(BaseModel):
    code: str
    title_uz: str
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    description_uz: str
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    link: Optional[str] = None

class StandardCreate(StandardBase):
    pass

class StandardUpdate(BaseModel):
    code: Optional[str] = None
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    link: Optional[str] = None

class StandardResponse(StandardBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

# === BUILDING REGULATION ===
class BuildingRegulationBase(BaseModel):
    number: str
    code: str
    title_uz: str
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    link: Optional[str] = None

class BuildingRegulationCreate(BuildingRegulationBase):
    pass

class BuildingRegulationUpdate(BaseModel):
    number: Optional[str] = None
    code: Optional[str] = None
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    link: Optional[str] = None

class BuildingRegulationResponse(BuildingRegulationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

# === SMETA RESURS NORM ===
class SmetaResursNormBase(BaseModel):
    srn_code: str
    srn_title_uz: str
    srn_title_ru: Optional[str] = None
    srn_title_en: Optional[str] = None
    main_shnq_code: Optional[str] = None
    main_shnq_title_uz: Optional[str] = None
    main_shnq_title_ru: Optional[str] = None
    main_shnq_title_en: Optional[str] = None
    additional_shnqs: Optional[str] = None
    file: Optional[str] = None

class SmetaResursNormCreate(SmetaResursNormBase):
    pass

class SmetaResursNormUpdate(BaseModel):
    srn_code: Optional[str] = None
    srn_title_uz: Optional[str] = None
    srn_title_ru: Optional[str] = None
    srn_title_en: Optional[str] = None
    main_shnq_code: Optional[str] = None
    main_shnq_title_uz: Optional[str] = None
    main_shnq_title_ru: Optional[str] = None
    main_shnq_title_en: Optional[str] = None
    additional_shnqs: Optional[str] = None
    file: Optional[str] = None

class SmetaResursNormResponse(SmetaResursNormBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

# === TECHNICAL REGULATION ===
class TechnicalRegulationBase(BaseModel):
    code: str
    title_uz: str
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    link: Optional[str] = None

class TechnicalRegulationCreate(TechnicalRegulationBase):
    pass

class TechnicalRegulationUpdate(BaseModel):
    code: Optional[str] = None
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    link: Optional[str] = None

class TechnicalRegulationResponse(TechnicalRegulationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

# === REFERENCE ===
class ReferenceBase(BaseModel):
    number: str
    title_uz: str
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    link: Optional[str] = None

class ReferenceCreate(ReferenceBase):
    pass

class ReferenceUpdate(BaseModel):
    number: Optional[str] = None
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    link: Optional[str] = None

class ReferenceResponse(ReferenceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True