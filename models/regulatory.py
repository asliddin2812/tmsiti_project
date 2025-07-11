from sqlalchemy import Column, Integer, String, Text, DateTime, func
from core.database import Base

class Shnq(Base):
    __tablename__ = "shnq"
    id = Column(Integer, primary_key=True, index=True)
    subsystem = Column(String(50), nullable=False)
    group = Column(String(20), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    title_uz = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=True)
    title_en = Column(String(255), nullable=True)
    link = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Standard(Base):
    __tablename__ = "standards"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False)
    title_uz = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=True)
    title_en = Column(String(255), nullable=True)
    description_uz = Column(Text, nullable=False)
    description_ru = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    link = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BuildingRegulation(Base):
    __tablename__ = "building_regulations"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    title_uz = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=True)
    title_en = Column(String(255), nullable=True)
    link = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SmetaResursNorm(Base):
    __tablename__ = "srn"
    id = Column(Integer, primary_key=True, index=True)
    srn_code = Column(String(20), unique=True, nullable=False)
    srn_title_uz = Column(String(255), nullable=False)
    srn_title_ru = Column(String(255), nullable=True)
    srn_title_en = Column(String(255), nullable=True)
    main_shnq_code = Column(String(20), nullable=True)
    main_shnq_title_uz = Column(String(255), nullable=True)
    main_shnq_title_ru = Column(String(255), nullable=True)
    main_shnq_title_en = Column(String(255), nullable=True)
    additional_shnqs = Column(Text, nullable=True)
    file = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TechnicalRegulation(Base):
    __tablename__ = "technical_regulations"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False)
    title_uz = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=True)
    title_en = Column(String(255), nullable=True)
    description_uz = Column(Text, nullable=True)
    description_ru = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    link = Column(String(500), nullable=True)
    file = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Reference(Base):
    __tablename__ = "reference"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), nullable=False)
    title_uz = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=True)
    title_en = Column(String(255), nullable=True)
    link = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())