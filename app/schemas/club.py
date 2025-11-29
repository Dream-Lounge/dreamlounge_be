from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from app.models.enums import ClubType


class ClubBase(BaseModel):
    name: str
    club_type: ClubType  # ✅ type → club_type
    category: Optional[str] = None
    tag: Optional[str] = None
    description: Optional[str] = None
    custom_form: Optional[Dict[str, Any]] = None


class ClubCreate(ClubBase):
    pass


class ClubUpdate(BaseModel):
    name: Optional[str] = None
    club_type: Optional[ClubType] = None  # ✅ type → club_type
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