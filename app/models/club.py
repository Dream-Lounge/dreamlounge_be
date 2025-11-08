# 임시 club 테이블입니다

from sqlalchemy import Column, Integer, String
from ..database import Base

class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)