from sqlalchemy import Column, String, Enum, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class RoleEnum(str, enum.Enum):
    MEMBER = "회원"
    GUEST = "비회원"
    ADMIN = "관리자"

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("student_id", name="uq_users_student_id"),
    )

    # 학번 로그인 ID (PK & UNIQUE)
    student_id = Column(String(20), primary_key=True)
    name = Column(String(50), nullable=False)
    department = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)

    # 전체 사용자 역할: 회원/비회원/관리자
    role = Column(Enum(RoleEnum, name="role_enum"), nullable=False)

    # 동아리 소속 (없을 수 있음)
    club_id = Column(Integer, ForeignKey("clubs.id", ondelete="SET NULL"), nullable=True)

    # 1:1 서브타입 매핑
    member = relationship("UserMember", back_populates="user", uselist=False, cascade="all, delete-orphan")
    guest = relationship("UserGuest", back_populates="user", uselist=False, cascade="all, delete-orphan")
    admin = relationship("UserAdmin", back_populates="user", uselist=False, cascade="all, delete-orphan")
