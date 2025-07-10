from typing import TypeVar, Generic, List
from pydantic import BaseModel
from sqlalchemy.orm import Query
from fastapi import HTTPException, status

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    page: int
    size: int
    pages: int
    items: List[T]

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True

def paginate(query: Query, page: int, size: int) -> PaginatedResponse:
    if page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Page >= 1 bo'lishi kerak")
    if size < 1 or size > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Size 1 dan 100 gacha bo'lishi kerak")

    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    pages = (total + size - 1) // size if total > 0 else 1

    return PaginatedResponse(
        total=total,
        page=page,
        size=size,
        pages=pages,
        items=items
    )
