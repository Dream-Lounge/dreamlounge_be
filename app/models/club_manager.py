from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base


class ClubManager(Base):
    __tablename__ = "club_manager"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="관리자ID")
    student_id = Column(Integer, ForeignKey("member.student_id"), nullable=False, comment="학번")
    club_id = Column(Integer, ForeignKey("club.club_id"), nullable=False, comment="동아리ID")
    assigned_at = Column(DateTime, default=datetime.utcnow, comment="배정일시")
    
    # Relationships
    member = relationship("Member", back_populates="club_managers")
    club = relationship("Club", back_populates="club_managers")