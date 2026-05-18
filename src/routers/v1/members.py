from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
<<<<<<< Updated upstream
from src.db.session import get_db
from src.core.dependencies import get_current_user
from src.schemas.application import ActiveClubItem

router = APIRouter(tags=["me"])


@router.get("/me/clubs", response_model=list[ActiveClubItem])
def get_active_clubs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """합격하여 활동 중인 동아리 목록 조회."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
=======

from src.db.session import get_db
from src.core.dependencies import require_club_president
from src.schemas.member import MemberResponse
from src.services import member_service

router = APIRouter(prefix="/clubs", tags=["members"])


@router.get("/{club_id}/members", response_model=list[MemberResponse])
def list_members(
    club_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_club_president),
):
    """동아리 회원 명단 조회 (회장 전용)."""
    return member_service.list_members(db, club_id)


@router.patch("/{club_id}/members/{user_id}/withdraw", status_code=status.HTTP_204_NO_CONTENT)
def withdraw_member(
    club_id: str,
    user_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_club_president),
):
    """부원 탈퇴 처리 (회장 전용)."""
    try:
        member_service.withdraw_member(db, club_id, user_id)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{club_id}/members/{user_id}/role", status_code=status.HTTP_204_NO_CONTENT)
def transfer_role(
    club_id: str,
    user_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_club_president),
):
    """권한 이전 — 해당 부원이 회장이 되고 기존 회장은 일반 부원으로 변경됩니다 (회장 전용)."""
    try:
        member_service.transfer_role(db, club_id, current_user.id, user_id)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
>>>>>>> Stashed changes
