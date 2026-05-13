from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.schemas.club import ClubResponse, ApplicationFormResponse

router = APIRouter(prefix="/clubs", tags=["clubs"])


@router.get("/{club_id}", response_model=ClubResponse)
def get_club(club_id: str, db: Session = Depends(get_db)):
    """동아리 상세 조회 (비회원 포함)."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get("/{club_id}/form", response_model=ApplicationFormResponse)
def get_club_form(club_id: str, db: Session = Depends(get_db)):
    """동아리 신청 폼(질문 목록) 조회."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
