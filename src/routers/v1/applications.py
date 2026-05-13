from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.core.dependencies import get_current_user
from src.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ApplicationListItem,
)

router = APIRouter(tags=["applications"])


@router.post("/applications", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(
    body: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """신청서 임시저장(is_draft=true) 또는 제출(is_draft=false)."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.patch("/applications/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: str,
    body: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """임시저장 신청서 수정 또는 최종 제출."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get("/me/applications/drafts", response_model=list[ApplicationListItem])
def get_draft_applications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """임시저장함 목록 조회."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get("/me/applications/drafts/{application_id}", response_model=ApplicationResponse)
def get_draft_application(
    application_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """임시저장 신청서 상세 조회 (수정 가능)."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get("/me/applications/submitted", response_model=list[ApplicationListItem])
def get_submitted_applications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """제출한 신청서 목록 + 상태 조회."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get("/me/applications/submitted/{application_id}", response_model=ApplicationResponse)
def get_submitted_application(
    application_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """제출한 신청서 상세 조회 (읽기 전용)."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
