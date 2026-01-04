from pydantic import BaseModel, Field, field_validator, model_validator
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
    password_confirm: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """비밀번호 강도 검증 (선택사항)"""
        return v
    
    @model_validator(mode='after')
    def check_passwords_match(self) -> 'MemberCreate':
        """비밀번호 확인 일치 검증"""
        if self.password != self.password_confirm:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return self


class MemberLogin(BaseModel):
    """로그인용 스키마"""
    student_id: int
    password: str


# ✅ 토큰 응답 스키마 추가
class TokenResponse(BaseModel):
    """로그인 성공 시 토큰 응답"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # 초 단위
    user: dict


class MemberUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    password_confirm: Optional[str] = None
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        """비밀번호 강도 검증"""
        return v
    
    @model_validator(mode='after')
    def check_passwords_match(self) -> 'MemberUpdate':
        """비밀번호 확인 일치 검증 (비밀번호 변경 시)"""
        if self.password is not None and self.password_confirm is not None:
            if self.password != self.password_confirm:
                raise ValueError('비밀번호가 일치하지 않습니다')
        elif self.password is not None and self.password_confirm is None:
            raise ValueError('비밀번호 확인을 입력해주세요')
        return self


class MemberResponse(MemberBase):
    student_id: int
    registered_at: datetime
    # ⚠️ password는 절대 포함하지 않음 (보안)
    
    class Config:
        from_attributes = True