from sqlalchemy.orm import Session
from src.models.notification import Notification


def send_application_result(db: Session, user_id: str, club_name: str, status: str) -> None:
    """합격·불합격·보류 결과 알림 생성 + 이메일 발송."""
    raise NotImplementedError


def send_notice_to_members(db: Session, club_id: str, post_id: str) -> None:
    """공지 게시글 등록 시 동아리 부원 전체에게 알림 생성."""
    raise NotImplementedError
