from sqlalchemy import Column, String, DateTime, CheckConstraint, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database import Base
from .user import RoleEnum

class UserAdmin(Base):
    __tablename__ = "user_admins"
    __table_args__ = (
        # 이 테이블은 반드시 '관리자'만
        CheckConstraint("role = '관리자'", name="ck_user_admins_role"),
    )

    student_id = Column(String(20), ForeignKey("users.student_id", ondelete="CASCADE"), primary_key=True)

    # 관리자 비밀번호 (해시 저장)
    password = Column(String(255), nullable=False)

    # 역할 고정값
    role = Column(String(10), nullable=False, default=RoleEnum.ADMIN.value)

    # 가입일
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="admin", uselist=False)
