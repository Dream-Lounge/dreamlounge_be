from sqlalchemy import Column, String, DateTime, CheckConstraint, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database import Base
from .user import RoleEnum

class UserMember(Base):
    __tablename__ = "user_members"
    __table_args__ = (
        # 이 테이블은 반드시 '회원'만
        CheckConstraint("role = '회원'", name="ck_user_members_role"),
    )

    # users.student_id 를 FK로 갖는 1:1
    student_id = Column(String(20), ForeignKey("users.student_id", ondelete="CASCADE"), primary_key=True)

    # 로그인 비밀번호 (해시 저장 권장: bcrypt/argon2 등)
    password = Column(String(255), nullable=False)

    # 역할 고정값 (FK는 부적절하므로 CHECK로 강제)
    role = Column(String(10), nullable=False, default=RoleEnum.MEMBER.value)

    # 가입일
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="member", uselist=False)
