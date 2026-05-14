from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.core.dependencies import get_current_user
from src.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ApplicationListItem,
    ActiveClubItem,
)
from src.services import application_service

router = APIRouter(tags=["applications"])


@router.post("/applications", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(
    body: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """신청서 임시저장(is_draft=true) 또는 제출(is_draft=false)."""
    try:
        return application_service.create_application(db, current_user, body)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/applications/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: str,
    body: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """임시저장 신청서 수정 또는 최종 제출."""
    try:
        return application_service.update_application(db, current_user, application_id, body)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/me/applications/drafts", response_model=list[ApplicationListItem])
def get_draft_applications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """임시저장함 목록 조회."""
    return application_service.get_draft_applications(db, current_user)


@router.get("/me/applications/drafts/{application_id}", response_model=ApplicationResponse)
def get_draft_application(
    application_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """임시저장 신청서 상세 조회 (수정 가능)."""
    app = application_service.get_draft_application(db, current_user, application_id)
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="임시저장 신청서를 찾을 수 없습니다.")
    return app


@router.get("/me/applications/submitted", response_model=list[ApplicationListItem])
def get_submitted_applications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """제출한 신청서 목록 + 상태 조회."""
    return application_service.get_submitted_applications(db, current_user)


@router.get("/me/applications/submitted/{application_id}", response_model=ApplicationResponse)
def get_submitted_application(
    application_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """제출한 신청서 상세 조회 (읽기 전용)."""
    app = application_service.get_submitted_application(db, current_user, application_id)
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="제출한 신청서를 찾을 수 없습니다.")
    return app


@router.get("/me/clubs", response_model=list[ActiveClubItem])
def get_active_clubs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """활동중인(합격한) 동아리 목록 조회."""
    return application_service.get_active_clubs(db, current_user)
