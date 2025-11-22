from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base


class Member(Base):
    __tablename__ = "member"
    
    student_id = Column(Integer, primary_key=True, comment="학번(고유)")
    name = Column(String(50), nullable=False, comment="이름")
    department = Column(String(100), comment="학과")
    phone = Column(String(20), comment="전화번호")
    password = Column(String(255), nullable=False, comment="비밀번호")
    registered_at = Column(DateTime, default=datetime.utcnow, comment="가입일시")
    
    # Relationships
    club_managers = relationship("ClubManager", back_populates="member")
    applications = relationship("Application", back_populates="member")
    club_memberships = relationship("ClubMembership", back_populates="member")