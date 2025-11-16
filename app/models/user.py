# app/models/user.py
from sqlalchemy import Column, String, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class RoleEnum(str, enum.Enum):
    MEMBER = "회원"
    GUEST = "비회원"
    ADMIN  = "관리자"

class User(Base):
    __tablename__ = "users"

    student_id = Column(String(20), primary_key=True)
    name       = Column(String(50), nullable=False)
    department = Column(String(100))
    phone      = Column(String(20))
    role       = Column(Enum(RoleEnum, name="role_enum"), nullable=True)
    club_id    = Column(Integer, ForeignKey("clubs.id", ondelete="SET NULL"))

    member = relationship("UserMember", back_populates="user", uselist=False, cascade="all, delete-orphan")
    guest  = relationship("UserGuest",  back_populates="user", uselist=False, cascade="all, delete-orphan")
    admin  = relationship("UserAdmin",  back_populates="user", uselist=False, cascade="all, delete-orphan")
