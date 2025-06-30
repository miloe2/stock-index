from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.db.database import Base


class IndexTypes(Base):
    __tablename__ = "index_types"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)  # "VIX", "FGI"
    name = Column(String)
    description = Column(String)

    index_data = relationship("IndexData", back_populates="index_type")


class IndexData(Base):
    __tablename__ = "index_data"

    id = Column(Integer, primary_key=True, index=True)
    index_type_id = Column(Integer, ForeignKey("index_types.id"), nullable=False)
    date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)
    # created_at = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    index_type = relationship("IndexTypes", back_populates="index_data")

    __table_args__ = (
        UniqueConstraint("index_type_id", "date", name="uix_index_type_date"),
    )


class IndexScore(Base):
    __tablename__ = "index_score"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    score = Column(Float)
    explanation = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
