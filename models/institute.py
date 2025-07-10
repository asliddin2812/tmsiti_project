from sqlalchemy import Column, Integer, String, Text, DateTime, func
from core.database import Base

# ✅ Institut haqida
class About(Base):
    __tablename__ = "about"
    id = Column(Integer, primary_key=True, index=True)
    content_uz = Column(Text, nullable=False)
    content_ru = Column(Text, nullable=False)
    content_en = Column(Text, nullable=False)
    pdf_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# ✅ Rahbariyat
class Management(Base):
    __tablename__ = "management"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    position_uz = Column(String, nullable=False)
    position_ru = Column(String, nullable=False)
    position_en = Column(String, nullable=False)
    profile_image = Column(String, nullable=True)
    reception_days = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    specialization_uz = Column(String, nullable=True)
    specialization_ru = Column(String, nullable=True)
    specialization_en = Column(String, nullable=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# ✅ Tuzilma
class Structure(Base):
    __tablename__ = "structure"
    id = Column(Integer, primary_key=True, index=True)
    title_uz = Column(String, nullable=False)
    title_ru = Column(String, nullable=False)
    title_en = Column(String, nullable=False)
    pdf_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# ✅ Tarkibiy bo'limlar
class StructuralDivision(Base):
    __tablename__ = "structural_divisions"
    id = Column(Integer, primary_key=True, index=True)
    title_uz = Column(String, nullable=False)
    title_ru = Column(String, nullable=False)
    title_en = Column(String, nullable=False)
    head_full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    profile_image = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# ✅ Vakansiyalar
class Vacancy(Base):
    __tablename__ = "vacancies"
    id = Column(Integer, primary_key=True, index=True)
    title_uz = Column(String, nullable=False)
    title_ru = Column(String, nullable=False)
    title_en = Column(String, nullable=False)
    description_uz = Column(Text, nullable=False)
    description_ru = Column(Text, nullable=False)
    description_en = Column(Text, nullable=False)
    requirements_uz = Column(Text, nullable=False)
    requirements_ru = Column(Text, nullable=False)
    requirements_en = Column(Text, nullable=False)
    deadline = Column(DateTime, nullable=True)
    contact_email = Column(String, nullable=False)
    attachment = Column(String, nullable=True)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
