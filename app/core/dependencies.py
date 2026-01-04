# app/core/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.member import Member
from app.core.security import decode_access_token
from app.core.logging_config import get_logger

logger = get_logger(__name__)

# HTTP Bearer 스키마 (Authorization: Bearer <token>)
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Member:
    """
    현재 인증된 사용자 반환
    
    토큰을 검증하고 해당 사용자를 DB에서 조회합니다.
    """
    token = credentials.credentials
    
    # 1. 토큰 디코딩
    payload = decode_access_token(token)
    if payload is None:
        logger.warning("Invalid or expired token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 인증 토큰입니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. student_id 추출
    student_id: Optional[int] = payload.get("sub")
    if student_id is None:
        logger.warning("Token missing 'sub' claim")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 인증 토큰입니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. DB에서 사용자 조회
    user = db.query(Member).filter(Member.student_id == student_id).first()
    if user is None:
        logger.warning(f"User not found for student_id: {student_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[Member]:
    """
    선택적 인증 (토큰이 없어도 됨)
    """
    if credentials is None:
        return None
    
    try:
        return get_current_user(credentials, db)
    except HTTPException:
        return None