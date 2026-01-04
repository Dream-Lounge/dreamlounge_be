# app/routers/members.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.models.member import Member
from app.schemas.member import (
    MemberCreate, MemberResponse, MemberLogin, TokenResponse
)
from app.utils.password import hash_password, verify_password
from app.core.logging_config import get_logger
from app.core.security import create_access_token
from app.core.dependencies import get_current_user
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/members", tags=["Members"])
logger = get_logger(__name__)


@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member(member_data: MemberCreate, db: Session = Depends(get_db)):
    """
    회원가입
    
    - **student_id**: 학번 (8자리)
    - **name**: 이름
    - **department**: 학과
    - **phone**: 전화번호 (010-1234-5678)
    - **password**: 비밀번호 (8자 이상, 영문+숫자)
    - **password_confirm**: 비밀번호 확인
    """
    logger.info(f"Creating new member: student_id={member_data.student_id}")
    
    # 1. 중복 확인
    existing_member = db.query(Member).filter(
        Member.student_id == member_data.student_id
    ).first()
    
    if existing_member:
        logger.warning(f"Duplicate student_id attempted: {member_data.student_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 존재하는 학번입니다"
        )
    
    # 2. 비밀번호 해싱
    hashed_password = hash_password(member_data.password)
    
    # 3. Member 객체 생성 (password_confirm은 제외)
    db_member = Member(
        student_id=member_data.student_id,
        name=member_data.name,
        department=member_data.department,
        phone=member_data.phone,
        password=hashed_password
    )
    
    # 4. DB에 저장
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    
    logger.info(f"Member created successfully: student_id={member_data.student_id}")
    return db_member


@router.post("/login", response_model=TokenResponse)
def login(login_data: MemberLogin, db: Session = Depends(get_db)):
    """
    로그인 - JWT 토큰 발급
    
    - **student_id**: 학번
    - **password**: 비밀번호
    
    성공 시 access_token을 반환합니다.
    이후 API 요청 시 헤더에 `Authorization: Bearer <token>`을 포함하세요.
    """
    logger.info(f"Login attempt: student_id={login_data.student_id}")
    
    # 1. 사용자 조회
    member = db.query(Member).filter(
        Member.student_id == login_data.student_id
    ).first()
    
    if not member:
        logger.warning(f"Login failed - user not found: student_id={login_data.student_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="학번 또는 비밀번호가 올바르지 않습니다"
        )
    
    # 2. 비밀번호 검증
    if not verify_password(login_data.password, member.password):
        logger.warning(f"Login failed - wrong password: student_id={login_data.student_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="학번 또는 비밀번호가 올바르지 않습니다"
        )
    
    # 3. JWT 토큰 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(member.student_id)},  # subject: 사용자 식별자
        expires_delta=access_token_expires
    )
    
    # 4. 로그인 성공 응답
    logger.info(f"Login successful: student_id={login_data.student_id}")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # 초 단위로 변환
        "user": {
            "student_id": member.student_id,
            "name": member.name,
            "department": member.department,
            "phone": member.phone
        }
    }


@router.get("/me", response_model=MemberResponse)
def get_current_member(current_user: Member = Depends(get_current_user)):
    """
    현재 로그인한 사용자 정보 조회
    
    **인증 필요**: Authorization 헤더에 Bearer 토큰 필요
    """
    logger.info(f"Fetching current user info: student_id={current_user.student_id}")
    return current_user


@router.get("/check/{student_id}")
def check_student_id_exists(student_id: int, db: Session = Depends(get_db)):
    """학번 중복 확인 (실시간 검증용)"""
    existing = db.query(Member).filter(
        Member.student_id == student_id
    ).first()
    
    return {
        "exists": existing is not None,
        "student_id": student_id
    }