from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.enums import MembershipStatus


class ClubMembershipBase(BaseModel):
    student_id: int
    club_id: int
    application_id: Optional[int] = None


class ClubMembershipCreate(ClubMembershipBase):
    pass


class ClubMembershipUpdate(BaseModel):
    status: Optional[MembershipStatus] = None
    left_at: Optional[datetime] = None


class ClubMembershipResponse(ClubMembershipBase):
    id: int
    status: MembershipStatus
    joined_at: datetime
    left_at: Optional[datetime]
    
    class Config:
        from_attributes = True