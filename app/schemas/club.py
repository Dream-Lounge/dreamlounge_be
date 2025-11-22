from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from app.models.enums import ClubType


class ClubBase(BaseModel):
    name: str
    type: ClubType
    category: Optional[str] = None
    tag: Optional[str] = None
    description: Optional[str] = None
    custom_form: Optional[Dict[str, Any]] = None


class ClubCreate(ClubBase):
    pass


class ClubUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[ClubType] = None
    category: Optional[str] = None
    tag: Optional[str] = None
    description: Optional[str] = None
    custom_form: Optional[Dict[str, Any]] = None


class ClubResponse(ClubBase):
    club_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True