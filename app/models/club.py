from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship
from ..database import Base

class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, autoincrement=True)  # club_id
    name = Column(String(100), nullable=False, unique=True)     # 동아리 이름
    type = Column(String(50), nullable=False)                   # 학과/중앙 등
    category = Column(String(50), nullable=True)                # 분과(체육, 미술 등)
    tags = Column(JSON, nullable=True)                          # 키워드(리스트/맵) -> JSON
    leader_id = Column(String(20), ForeignKey("users.student_id", ondelete="SET NULL"), nullable=True)  # 관리자 학번
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)             # 등록일
    description = Column(Text, nullable=True)                   # 소개글
    custom_form = Column(JSON, nullable=True)                   # 신청 폼 구조(JSON)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 역방향 관계(필요 시 사용)
    leader = relationship("User", foreign_keys=[leader_id], lazy="joined")
    submitted_forms = relationship("Submitted", back_populates="club", cascade="all, delete-orphan")
    temp_saved_forms = relationship("TempSaved", back_populates="club", cascade="all, delete-orphan")
