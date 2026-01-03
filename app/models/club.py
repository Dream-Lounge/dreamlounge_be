from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base
from app.models.enums import ClubType


class Club(Base):
    __tablename__ = "club"
    
    club_id = Column(Integer, primary_key=True, autoincrement=True, comment="동아리ID")
    name = Column(String(100), nullable=False, comment="동아리이름")
    club_type = Column(Enum(ClubType), nullable=False, comment="유형(학과/중앙)")  # ✅ type → club_type
    category = Column(String(50), comment="분야")
    tag = Column(String(255), comment="키워드")
    description = Column(Text, comment="동아리소개")
    custom_form = Column(JSON, comment="커스텀신청폼")
    created_at = Column(DateTime, default=datetime.utcnow, comment="등록일시")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="수정일시")
    
    # Relationships
    # club_managers = relationship("ClubManager", back_populates="club")
    # applications = relationship("Application", back_populates="club")
    # club_memberships = relationship("ClubMembership", back_populates="club")