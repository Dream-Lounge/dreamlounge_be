from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.enums import UserType, ApplicationStatus


class Application(Base):
    __tablename__ = "application"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="신청서ID")
    club_id = Column(Integer, ForeignKey("club.club_id"), nullable=False, comment="동아리ID")
    student_id = Column(Integer, ForeignKey("member.student_id"), nullable=True, comment="학번(NULL가능)")
    guest_name = Column(String(50), comment="비회원이름")
    guest_phone = Column(String(20), comment="비회원전화번호")
    user_type = Column(Enum(UserType), nullable=False, comment="사용자유형(회원/비회원)")
    content = Column(JSON, comment="신청내용")
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.DRAFT, comment="상태(임시저장/제출됨/합격/불합격)")
    submitted_time = Column(DateTime, comment="제출일시")
    reviewed_at = Column(DateTime, comment="검토일시")
    comment = Column(String(500), comment="검토의견")
    
    # Relationships
    club = relationship("Club", back_populates="applications")
    member = relationship("Member", back_populates="applications")
    club_membership = relationship("ClubMembership", back_populates="application", uselist=False)