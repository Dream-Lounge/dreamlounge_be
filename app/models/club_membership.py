from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base
from app.models.enums import MembershipStatus


class ClubMembership(Base):
    __tablename__ = "club_membership"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="멤버십ID")
    student_id = Column(Integer, ForeignKey("member.student_id"), nullable=False, comment="학번")
    club_id = Column(Integer, ForeignKey("club.club_id"), nullable=False, comment="동아리ID")
    application_id = Column(Integer, ForeignKey("application.id"), comment="신청서ID")
    status = Column(Enum(MembershipStatus), default=MembershipStatus.ACTIVE, comment="상태(활동중/탈퇴)")
    joined_at = Column(DateTime, default=datetime.utcnow, comment="가입일시")
    left_at = Column(DateTime, nullable=True, comment="탈퇴일시")
    
    # Relationships
    # member = relationship("Member", back_populates="club_memberships")
    # club = relationship("Club", back_populates="club_memberships")
    # application = relationship("Application", back_populates="club_membership")