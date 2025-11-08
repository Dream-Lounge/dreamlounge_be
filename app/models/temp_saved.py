from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, PrimaryKeyConstraint, Index, func
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class TempStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class TempSaved(Base):
    __tablename__ = "temp_saved"

    club_id = Column(Integer, ForeignKey("clubs.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(String(20), ForeignKey("users.student_id", ondelete="CASCADE"), nullable=False)

    content = Column(JSON, nullable=False)  # 임시 저장된 신청서 내용
    status = Column(Enum(TempStatus, name="tempsaved_status_enum"), nullable=False, server_default=TempStatus.SUBMITTED.value)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    saved_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("club_id", "student_id", name="pk_tempsaved_club_student"),  # 복합 PK
        Index("ix_tempsaved_status", "status"),
        Index("ix_tempsaved_saved_at", "saved_at"),
    )

    # 관계
    club = relationship("Club", back_populates="temp_saved_forms")
    user = relationship("User", lazy="joined")
