from sqlalchemy.orm import Session
from src.models.application import Application
from src.models.user import User
from src.schemas.application import ApplicationCreate, ApplicationUpdate


def create_application(db: Session, user: User, data: ApplicationCreate) -> Application:
    """신청서 생성. is_draft=False면 submitted_at 설정, status='submitted'."""
    raise NotImplementedError


def update_application(
    db: Session, user: User, application_id: str, data: ApplicationUpdate
) -> Application:
    """임시저장 신청서 수정. is_draft=False로 변경 시 최종 제출 처리."""
    raise NotImplementedError


def get_draft_applications(db: Session, user: User) -> list[Application]:
    """사용자의 임시저장 신청서 목록 (is_draft=True)."""
    raise NotImplementedError


def get_draft_application(db: Session, user: User, application_id: str) -> Application | None:
    """임시저장 신청서 상세 + answers 조회. 본인 소유 확인."""
    raise NotImplementedError


def get_submitted_applications(db: Session, user: User) -> list[Application]:
    """사용자의 제출 완료 신청서 목록 (is_draft=False)."""
    raise NotImplementedError


def get_submitted_application(db: Session, user: User, application_id: str) -> Application | None:
    """제출 신청서 상세 조회 (읽기 전용). 본인 소유 확인."""
    raise NotImplementedError


def get_active_clubs(db: Session, user: User) -> list:
    """합격(passed) 상태이고 부원(active)으로 등록된 동아리 목록."""
    raise NotImplementedError
