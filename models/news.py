from sqlalchemy import Column, Integer, String, Text, DateTime, func
from core.database import Base

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title_uz = Column(String, nullable=False)
    title_ru = Column(String, nullable=False)
    title_en = Column(String, nullable=False)
    content_uz = Column(Text, nullable=False)
    content_ru = Column(Text, nullable=False)
    content_en = Column(Text, nullable=False)
    image = Column(String, nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AntiCorruption(Base):
    __tablename__ = "anti_corruption"
    id = Column(Integer, primary_key=True, index=True)
    title_uz = Column(String, nullable=False)
    title_ru = Column(String, nullable=False)
    title_en = Column(String, nullable=False)
    content_uz = Column(Text, nullable=False)
    content_ru = Column(Text, nullable=False)
    content_en = Column(Text, nullable=False)
    file = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
