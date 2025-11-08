from sqlalchemy import Column, String, DateTime, CheckConstraint, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database import Base
from .user import RoleEnum

class UserGuest(Base):
    __tablename__ = "user_guests"
    __table_args__ = (
        # 이 테이블은 반드시 '비회원'만
        CheckConstraint("role = '비회원'", name="ck_user_guests_role"),
    )

    student_id = Column(String(20), ForeignKey("users.student_id", ondelete="CASCADE"), primary_key=True)

    # 역할 고정값
    role = Column(String(10), nullable=False, default=RoleEnum.GUEST.value)

    # 동아리 신청서 제출 시간
    submitted_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="guest", uselist=False)
