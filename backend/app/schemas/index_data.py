# schemas/index_data.py

from pydantic import BaseModel
from datetime import date


class IndexDataCreate(BaseModel):
    code: str
    date: date
    value: float


class IndexDataRead(IndexDataCreate):
    id: int

    class Config:
        orm_mode = True
