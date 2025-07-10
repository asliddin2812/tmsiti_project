from sqlalchemy import Column, Integer, String, Text, DateTime, func
from core.database import Base

class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    fio = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    category_uz = Column(String, nullable=True)
    category_ru = Column(String, nullable=True)
    category_en = Column(String, nullable=True)

    message_uz = Column(Text, nullable=True)
    message_ru = Column(Text, nullable=True)
    message_en = Column(Text, nullable=True)

    file = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
