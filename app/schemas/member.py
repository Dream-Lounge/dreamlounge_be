from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


class MemberBase(BaseModel):
    name: str
    department: Optional[str] = None
    phone: Optional[str] = None


class MemberCreate(BaseModel):
    student_id: int
    name: str
    department: Optional[str] = None
    phone: Optional[str] = None
    password: str = Field(..., min_length=8, description="최소 8자 이상")
    
    @validator('password')
    def validate_password(cls, v):
        """비밀번호 강도 검증 (선택사항)"""
        if len(v) < 8:
            raise ValueError('비밀번호는 최소 8자 이상이어야 합니다')
        # 추가 검증 규칙 가능
        # if not any(char.isdigit() for char in v):
        #     raise ValueError('비밀번호에 최소 1개의 숫자가 포함되어야 합니다')
        return v


class MemberLogin(BaseModel):
    """로그인용 스키마"""
    student_id: int
    password: str


class MemberUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    
    @validator('password')
    def validate_password(cls, v):
        if v and len(v) < 8:
            raise ValueError('비밀번호는 최소 8자 이상이어야 합니다')
        return v


class MemberResponse(MemberBase):
    student_id: int
    registered_at: datetime
    # ⚠️ password는 절대 포함하지 않음 (보안)
    
    class Config:
        from_attributes = True