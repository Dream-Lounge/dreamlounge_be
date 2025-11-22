from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from app.models.enums import UserType, ApplicationStatus


class ApplicationBase(BaseModel):
    club_id: int
    user_type: UserType
    content: Optional[Dict[str, Any]] = None


class ApplicationCreate(ApplicationBase):
    student_id: Optional[int] = None
    guest_name: Optional[str] = None
    guest_phone: Optional[str] = None


class ApplicationUpdate(BaseModel):
    content: Optional[Dict[str, Any]] = None
    status: Optional[ApplicationStatus] = None
    comment: Optional[str] = None


class ApplicationResponse(ApplicationBase):
    id: int
    student_id: Optional[int]
    guest_name: Optional[str]
    guest_phone: Optional[str]
    status: ApplicationStatus
    submitted_time: Optional[datetime]
    reviewed_at: Optional[datetime]
    comment: Optional[str]
    
    class Config:
        from_attributes = True