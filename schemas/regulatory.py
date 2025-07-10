from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# SHNQ
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

class ShnqResponse(BaseModel):
    id: int
    subsystem: str
    group: str
    code: str
    title_uz: str
    title_ru: Optional[str]
    title_en: Optional[str]
    link: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# STANDARDS
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

class StandardResponse(BaseModel):
    id: int
    code: str
    title_uz: str
    title_ru: Optional[str]
    title_en: Optional[str]
    description_uz: str
    description_ru: Optional[str]
    description_en: Optional[str]
    link: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# BUILDING REGULATION
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

class BuildingRegulationResponse(BaseModel):
    id: int
    number: str
    code: str
    title_uz: str
    title_ru: Optional[str]
    title_en: Optional[str]
    link: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# SMETA RESURS NORM
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

class SmetaResursNormResponse(BaseModel):
    id: int
    srn_code: str
    srn_title_uz: str
    srn_title_ru: Optional[str]
    srn_title_en: Optional[str]
    main_shnq_code: Optional[str]
    main_shnq_title_uz: Optional[str]
    main_shnq_title_ru: Optional[str]
    main_shnq_title_en: Optional[str]
    additional_shnqs: Optional[str]
    file: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# TECHNICAL REGULATIONS
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

class TechnicalRegulationResponse(BaseModel):
    id: int
    code: str
    title_uz: str
    title_ru: Optional[str]
    title_en: Optional[str]
    description_uz: Optional[str]
    description_ru: Optional[str]
    description_en: Optional[str]
    link: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# REFERENCE
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

class ReferenceResponse(BaseModel):
    id: int
    number: str
    title_uz: str
    title_ru: Optional[str]
    title_en: Optional[str]
    link: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True