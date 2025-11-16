# app/models/club.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship
from ..database import Base

class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, autoincrement=True)   # club_id
    name = Column(String(100), nullable=False, unique=True)
    club_type = Column(String(50), nullable=False)               # 🔁 renamed from `type`
    category = Column(String(50), nullable=True)
    tags = Column(JSON, nullable=True)                           # 키워드(리스트/맵)
    leader_id = Column(String(20), ForeignKey("users.student_id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    description = Column(Text, nullable=True)
    custom_form = Column(JSON, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 🔁 lazy 전략 조정: 기본 조회는 가볍게, 필요할 때 selectin 로딩
    leader = relationship("User", foreign_keys=[leader_id], lazy="selectin")

    submitted_forms = relationship("Submitted", back_populates="club", cascade="all, delete-orphan")
    temp_saved_forms = relationship("TempSaved", back_populates="club", cascade="all, delete-orphan")
