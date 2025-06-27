# schemas/index_type.py

from pydantic import BaseModel
from typing import Optional


class IndexTypeCreate(BaseModel):
    code: str
    name: Optional[str] = None
    description: Optional[str] = None


class IndexTypeRead(IndexTypeCreate):
    id: int

    class Config:
        orm_mode = True
