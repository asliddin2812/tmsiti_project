from pydantic import BaseModel
from typing import Optional, List, Generic, TypeVar
from datetime import datetime

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

class FileUploadResponse(BaseModel):
    filename: str
    url: str
    size: int