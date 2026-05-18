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


<<<<<<< Updated upstream
def get_active_clubs(db: Session, user: User) -> list:
    """합격(passed) 상태이고 부원(active)으로 등록된 동아리 목록."""
    raise NotImplementedError
=======
# ── 관리자: 신청서 심사 ────────────────────────────────────────────────────────

def get_club_applications(db: Session, club_id: str) -> list[dict]:
    """동아리에 제출된 신청서 목록 (is_draft=False)."""
    apps = (
        db.query(Application)
        .join(ApplicationForm, Application.form_id == ApplicationForm.id)
        .filter(ApplicationForm.club_id == club_id, Application.is_draft == False)
        .order_by(Application.submitted_at.desc())
        .all()
    )
    return [
        {
            "id": a.id,
            "user_id": a.user_id,
            "user_name": a.user.name,
            "user_student_id": a.user.student_id,
            "status": a.status,
            "submitted_at": a.submitted_at,
        }
        for a in apps
    ]


def get_club_application(db: Session, club_id: str, application_id: str) -> dict | None:
    """동아리 신청서 상세 (관리자용)."""
    from sqlalchemy.orm import selectinload
    app = (
        db.query(Application)
        .options(selectinload(Application.answers), selectinload(Application.user))
        .join(ApplicationForm, Application.form_id == ApplicationForm.id)
        .filter(
            ApplicationForm.club_id == club_id,
            Application.id == application_id,
            Application.is_draft == False,
        )
        .first()
    )
    if not app:
        return None
    return {
        "id": app.id,
        "user_id": app.user_id,
        "user_name": app.user.name,
        "user_student_id": app.user.student_id,
        "status": app.status,
        "submitted_at": app.submitted_at,
        "answers": app.answers,
    }


def update_application_status(db: Session, club_id: str, application_id: str, new_status: str) -> Application:
    """심사 결과 업데이트. passed 시 ClubMember 자동 등록."""
    app = (
        db.query(Application)
        .join(ApplicationForm, Application.form_id == ApplicationForm.id)
        .filter(
            ApplicationForm.club_id == club_id,
            Application.id == application_id,
            Application.is_draft == False,
        )
        .first()
    )
    if not app:
        raise LookupError("신청서를 찾을 수 없습니다.")
    if app.status in ("passed", "failed"):
        raise ValueError("이미 최종 심사가 완료된 신청서입니다.")

    app.status = new_status

    if new_status == "passed":
        already = db.query(ClubMember).filter(
            ClubMember.club_id == club_id,
            ClubMember.user_id == app.user_id,
            ClubMember.status == "active",
        ).first()
        if not already:
            db.add(ClubMember(club_id=club_id, user_id=app.user_id, role="member", status="active"))

    db.commit()
    db.refresh(app)
    return app


def get_active_clubs(db: Session, user: User) -> list[dict]:
    memberships = (
        db.query(ClubMember)
        .join(Club, ClubMember.club_id == Club.id)
        .filter(ClubMember.user_id == user.id, ClubMember.status == "active")
        .all()
    )
    return [
        {
            "club_id": m.club_id,
            "club_name": m.club.name,
            "role": m.role,
            "joined_at": m.joined_at,
        }
        for m in memberships
    ]
>>>>>>> Stashed changes
