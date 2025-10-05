from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

# 역할 Enum 타입 미리 정의
UserRoleEnum = Enum('MEMBER', 'ADMIN', 'GUEST', name='user_role_enum')

class User(Base):
    """[user테이블(모든 사용자)]"""
    __tablename__ = "User"

    student_id = Column(String(20), primary_key=True, unique=True, index=True)
    name = Column(String(50), nullable=False)
    department = Column(String(100))
    phone = Column(String(20))
    role = Column(UserRoleEnum, nullable=False, default='GUEST') #잼미니는 기본값을 guest로 두래요. 근데 왜그럴까여,,

    #관계 설정 -> 이게 뭘까 / 왜 detail을 따로 둘까..?
    member_detail = relationship("UserMember", back_populates="User", uselist=False)
    admin_detail = relationship("UserAdmin", back_populates="User", uselist=False)
    guest_detail = relationship("UserGuest", back_populates="User", uselist=False)