from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class ClubTagResponse(BaseModel):
    tag_key: str
    tag_value: str

    model_config = {"from_attributes": True}


class ClubResponse(BaseModel):
    id: str
    name: str
    club_type: Optional[str]
    description: Optional[str]
    contact_email: Optional[str]
    contact_phone: Optional[str]
    open_chat_url: Optional[str]
    image_url: Optional[str]
    division: Optional[str]
    field: Optional[str]
    atmosphere: Optional[str]
    activity_purpose: Optional[str]
    activity_period: Optional[str]
    recruit_start: Optional[date]
    recruit_end: Optional[date]
    is_recruiting: bool
    tags: List[ClubTagResponse] = []

    model_config = {"from_attributes": True}


class FormQuestionResponse(BaseModel):
    id: str
    question_text: str
    question_type: str
    is_required: bool
    order_index: int
    options: Optional[list] = None

    model_config = {"from_attributes": True}


class ApplicationFormResponse(BaseModel):
    id: str
    club_id: str
    title: str
    is_active: bool
    questions: List[FormQuestionResponse] = []

    model_config = {"from_attributes": True}
