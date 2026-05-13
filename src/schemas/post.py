from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PostCreate(BaseModel):
    title: str
    content: str


class PostResponse(BaseModel):
    id: str
    club_id: str
    author_id: str
    post_type: str
    title: str
    content: str
    is_notice: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: str
    post_id: str
    author_id: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
