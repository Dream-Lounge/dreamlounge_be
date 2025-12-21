# app/models/application.py
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.enums import UserType, ApplicationStatus


class Application(Base):
    __tablename__ = "application"
    
    # PK
    id = Column(Integer, primary_key=True, autoincrement=True, comment="신청서ID")
    
    # 기본 정보
    club_id = Column(Integer, ForeignKey("club.club_id"), nullable=False, comment="동아리ID")
    user_type = Column(Enum(UserType), nullable=False, comment="사용자유형(회원/비회원)")
    
    # 회원 정보 (로그인 상태)
    student_id = Column(
        Integer, 
        ForeignKey("member.student_id"), 
        nullable=True,  # 비회원은 NULL
        comment="회원학번"
    )
    
    # 비회원 정보 (직접 입력)
    guest_student_id = Column(String(20), comment="비회원학번")
    guest_name = Column(String(50), comment="비회원이름")
    guest_department = Column(String(100), comment="비회원학과")
    guest_phone = Column(String(20), comment="비회원전화번호")
    
    # 신청 내용
    content = Column(JSON, comment="신청내용")
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.DRAFT, comment="상태")
    submitted_time = Column(DateTime, comment="제출일시")
    reviewed_at = Column(DateTime, comment="검토일시")
    comment = Column(String(500), comment="검토의견")
    
    # 관계
    club = relationship("Club", back_populates="applications")
    member = relationship("Member", back_populates="applications")
    club_membership = relationship("ClubMembership", back_populates="application", uselist=False)
    
    # ✅ 중복 방지: 회원은 같은 동아리에 한 번만 신청 가능
    __table_args__ = (
        UniqueConstraint('club_id', 'student_id', name='unique_club_member_application'),
    )