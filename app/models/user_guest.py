from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
from .user_base import User, UserRoleEnum

class UserGuest(Base):
    """[user_guest 테이블(비회원 사용자)]"""
    __tablename__ = "User_guest"

    student_id = Column(String(20), ForeignKey("User.student_id"), primary_key=True)
    password = Column(String(255), nullable=False)
    role = Column(UserRoleEnum, nullable=False, default='GUEST') #잼미니는 기본값을 guest로 두래요. 근데 왜그럴까여,,
    created_date = Column(DateTime, default=datetime.now())
    
    user = relationship("User", back_populates="member_detail")