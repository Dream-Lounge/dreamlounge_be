# app/models/test_application.py
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from app.models.base import Base


class TestApplication(Base):
    __tablename__ = "test_applications"

    # ✅ student_id를 Primary Key로 변경
    student_id = Column(String(20), primary_key=True, comment="학번")
    
    department = Column(String(100), nullable=False, comment="학과")
    name = Column(String(50), nullable=False, comment="이름")
    email = Column(String(100), nullable=False, comment="이메일")
    phone = Column(String(20), nullable=False, comment="전화번호")
    
    created_at = Column(DateTime, default=datetime.utcnow, comment="등록일시")