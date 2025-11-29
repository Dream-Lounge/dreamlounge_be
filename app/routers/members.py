from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberResponse, MemberLogin
from app.utils.password import hash_password, verify_password
from app.core.logging_config import get_logger

router = APIRouter(prefix="/members", tags=["Members"])
logger = get_logger(__name__)


@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member(member_data: MemberCreate, db: Session = Depends(get_db)):
    """회원가입"""
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
    
    # 3. Member 객체 생성
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


@router.post("/login")
def login(login_data: MemberLogin, db: Session = Depends(get_db)):
    """로그인"""
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
    
    # 3. 로그인 성공
    logger.info(f"Login successful: student_id={login_data.student_id}")
    return {
        "message": "로그인 성공",
        "student_id": member.student_id,
        "name": member.name
    }