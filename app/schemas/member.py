from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MemberBase(BaseModel):
    name: str
    department: Optional[str] = None
    phone: Optional[str] = None


class MemberCreate(MemberBase):
    student_id: int
    password: str


class MemberUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class MemberResponse(MemberBase):
    student_id: int
    registered_at: datetime
    
    class Config:
        from_attributes = True