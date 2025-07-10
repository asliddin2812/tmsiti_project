from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from core.database import Base

class ManagementSystem(Base):
    __tablename__ = "management_systems"

    id = Column(Integer, primary_key=True, index=True)

    title_uz = Column(String, nullable=False)
    title_ru = Column(String, nullable=False)
    title_en = Column(String, nullable=False)

    description_uz = Column(Text, nullable=False)
    description_ru = Column(Text, nullable=False)
    description_en = Column(Text, nullable=False)

    pdf = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
