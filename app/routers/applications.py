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
    
    # 3. 신청서 생성
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
        
        # ✅ 중복 신청 에러 처리
        if "unique_club_member_application" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 해당 동아리에 신청하셨습니다."
            )
        
        # 기타 DB 에러
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="신청서 제출 중 오류가 발생했습니다."
        )