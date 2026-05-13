from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
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
