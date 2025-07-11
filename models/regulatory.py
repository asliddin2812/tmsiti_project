from sqlalchemy import Column, Integer, String, Text, DateTime, func
from core.database import Base

class Shnq(Base):
    __tablename__ = "shnq"
    id = Column(Integer, primary_key=True, index=True)
    subsystem = Column(String, nullable=False)
    group = Column(String, nullable=False)
    code = Column(String, nullable=False)
    title_uz = Column(String, nullable=False)
    title_ru = Column(String, nullable=True)
    title_en = Column(String, nullable=True)
    link = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Standard(Base):
    __tablename__ = "standards"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    title_uz = Column(String, nullable=False)
    title_ru = Column(String, nullable=True)
    title_en = Column(String, nullable=True)
    description_uz = Column(Text, nullable=False)
    description_ru = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    link = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BuildingRegulation(Base):
    __tablename__ = "building_regulations"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False)
    code = Column(String, nullable=False)
    title_uz = Column(String, nullable=False)
    title_ru = Column(String, nullable=True)
    title_en = Column(String, nullable=True)
    link = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SmetaResursNorm(Base):
    __tablename__ = "srn"
    id = Column(Integer, primary_key=True, index=True)
    srn_code = Column(String, nullable=False)
    srn_title_uz = Column(String, nullable=False)
    srn_title_ru = Column(String, nullable=True)
    srn_title_en = Column(String, nullable=True)
    main_shnq_code = Column(String, nullable=True)
    main_shnq_title_uz = Column(String, nullable=True)
    main_shnq_title_ru = Column(String, nullable=True)
    main_shnq_title_en = Column(String, nullable=True)
    additional_shnqs = Column(Text, nullable=True)
    file = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TechnicalRegulation(Base):
    __tablename__ = "technical_regulations"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    title_uz = Column(String, nullable=False)
    title_ru = Column(String, nullable=True)
    title_en = Column(String, nullable=True)
    description_uz = Column(Text, nullable=True)
    description_ru = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    link = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Reference(Base):
    __tablename__ = "reference"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False)
    title_uz = Column(String, nullable=False)
    title_ru = Column(String, nullable=True)
    title_en = Column(String, nullable=True)
    link = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())