# app/routers/applications.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app.database import get_db
from app.models.application import Application
from app.models.member import Member
from app.models.enums import UserType, ApplicationStatus

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("/member", status_code=status.HTTP_201_CREATED)
def create_member_application(
    club_id: int,
    content: dict = None,
    current_user_id: int = None,  # 로그인한 사용자 (인증에서 주입)
    db: Session = Depends(get_db)
):
    """회원 신청 (같은 동아리에 한 번만 가능)"""
    
    # 1. 로그인 확인
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인이 필요합니다."
        )
    
    # 2. 회원 정보 조회
    member = db.query(Member).filter(Member.student_id == current_user_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="회원 정보를 찾을 수 없습니다."
        )
    
    # 3. ✅ 사전 중복 체크 (DB 레벨 제약 조건 이전에 확인)
    existing_application = db.query(Application).filter(
        Application.club_id == club_id,
        Application.student_id == member.student_id,
        Application.user_type == UserType.MEMBER
    ).first()
    
    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 해당 동아리에 신청하셨습니다."
        )
    
    # 4. 신청서 생성
    new_app = Application(
        club_id=club_id,
        user_type=UserType.MEMBER,
        student_id=member.student_id,
        content=content,
        status=ApplicationStatus.SUBMITTED,
        submitted_time=datetime.utcnow()
    )
    
    try:
        db.add(new_app)
        db.commit()
        db.refresh(new_app)
        
        return {
            "message": "신청서가 제출되었습니다.",
            "application_id": new_app.id,
            "applicant": {
                "student_id": member.student_id,
                "name": member.name,
                "department": member.department,
                "phone": member.phone
            }
        }
        
    except IntegrityError as e:
        db.rollback()
        
        # ✅ 데이터베이스별 고유 키 위반 에러 코드 확인
        error_code = None
        
        # MySQL의 경우 (에러 코드 1062: Duplicate entry)
        if hasattr(e.orig, 'args') and len(e.orig.args) > 0:
            error_code = e.orig.args[0]
            if error_code == 1062:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="이미 해당 동아리에 신청하셨습니다."
                )
        
        # PostgreSQL의 경우 (에러 코드 23505: unique_violation)
        if hasattr(e.orig, 'pgcode') and e.orig.pgcode == '23505':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 해당 동아리에 신청하셨습니다."
            )
        
        # 기타 IntegrityError (외래 키 위반 등)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="데이터 무결성 오류가 발생했습니다."
        )
    
    except Exception as e:
        db.rollback()
        # 예상치 못한 에러
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="신청서 제출 중 오류가 발생했습니다."
        )