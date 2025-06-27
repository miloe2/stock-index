from sqlalchemy import Column, Integer, String, Float, Date, Double
from .config import Base


class IndexTypes(Base):
    __tablename__ = "index_types"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)  # "VIX", "FGI"
    name = Column(String)  # '공포탐욕지수'
    description = Column(String)  # '설명'


class IndexData(Base):
    __tablename__ = "index_data"

    id = Column(Integer, primary_key=True, index=True)
    index_type_id = Column(String, index=True)  # "VIX", "FGI"
    date = Column(Date)
    value = Column(Float)
    created_at = Column(Date)


class IndexScore(Base):
    __tablename__ = "index_score"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    score = Column(Float)
    explanation = Column(String)
    created_at = Column(Date)
