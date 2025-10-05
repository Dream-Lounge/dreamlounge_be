from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
from .user_base import User, UserRoleEnum 

class UserMember(Base):
    """[user_member 테이블 (회원 사용자)]"""
    __tablename__ = "User_member"

    student_id = Column(String(20), ForeignKey("User.student_id"), primary_key=True)
    password = Column(String(255), nullable=False)
    role = Column(UserRoleEnum, nullable=False, default='MEMBER') 
    created_date = Column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="member_detail")
