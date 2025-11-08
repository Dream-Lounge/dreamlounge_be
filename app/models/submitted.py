from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Text, PrimaryKeyConstraint, Index, func
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship
from ..database import Base
from .user import RoleEnum
import enum

class SubmissionStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class Submitted(Base):
    __tablename__ = "submitted"

    club_id = Column(Integer, ForeignKey("clubs.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(String(20), ForeignKey("users.student_id", ondelete="CASCADE"), nullable=False)

    # 회원/비회원/관리자 스냅샷 — FK 대신 Enum으로 고정값 보관
    role = Column(Enum(RoleEnum, name="role_enum"), nullable=True)

    # 신청서 내용(JSON)
    content = Column(JSON, nullable=False)

    status = Column(Enum(SubmissionStatus, name="submission_status_enum"), nullable=False, server_default=SubmissionStatus.SUBMITTED.value)

    submitted_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    admin_comment = Column(Text, nullable=True)  # 합격여부 및 관리자 메시지
    reviewed_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint("club_id", "student_id", name="pk_submitted_club_student"),  # 복합 PK
        Index("ix_submitted_status", "status"),
        Index("ix_submitted_submitted_time", "submitted_time"),
    )

    # 관계
    club = relationship("Club", back_populates="submitted_forms")
    user = relationship("User", lazy="joined")
