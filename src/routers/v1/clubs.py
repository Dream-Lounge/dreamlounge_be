from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.schemas.club import ClubResponse, ApplicationFormResponse
from src.services import club_service

router = APIRouter(prefix="/clubs", tags=["clubs"])


@router.get("/{club_id}", response_model=ClubResponse)
def get_club(club_id: str, db: Session = Depends(get_db)):
    """동아리 상세 조회 (비회원 포함)."""
    club = club_service.get_club(db, club_id)
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="동아리를 찾을 수 없습니다.")
    return club


@router.get("/{club_id}/form", response_model=ApplicationFormResponse)
def get_club_form(club_id: str, db: Session = Depends(get_db)):
    """동아리 신청 폼(질문 목록) 조회."""
    form = club_service.get_active_form(db, club_id)
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="활성화된 신청 폼이 없습니다.",
        )
    return form
