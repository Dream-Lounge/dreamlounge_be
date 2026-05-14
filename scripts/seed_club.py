"""
테스트용 동아리 시드 스크립트.

실행: python -m scripts.seed_club
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.db.session import SessionLocal
from src.core.security import hash_password
from src.models.user import User, PrivacyConsent
from src.models.club import Club, ClubTag
from src.models.club_member import ClubMember
from src.models.application import ApplicationForm, FormQuestion


PRESIDENT_STUDENT_ID = "20200001"
PRESIDENT_EMAIL = "president@cju.ac.kr"
PRESIDENT_PASSWORD = "Test1234!"


def seed(db):
    # ── 1. 회장 계정 ──────────────────────────────────────────────
    president = db.query(User).filter(User.student_id == PRESIDENT_STUDENT_ID).first()
    if not president:
        president = User(
            student_id=PRESIDENT_STUDENT_ID,
            password_hash=hash_password(PRESIDENT_PASSWORD),
            name="홍길동",
            phone="010-1234-5678",
            department="컴퓨터공학과",
            email=PRESIDENT_EMAIL,
            email_verified=True,
        )
        db.add(president)
        db.flush()

        db.add(PrivacyConsent(
            user_id=president.id,
            required_agreed=True,
            optional_agreed=False,
        ))
        print(f"[+] 회장 계정 생성: {PRESIDENT_STUDENT_ID} / {PRESIDENT_PASSWORD}")
    else:
        print(f"[=] 회장 계정 기존 존재: {PRESIDENT_STUDENT_ID}")

    # ── 2. 동아리 ─────────────────────────────────────────────────
    club = db.query(Club).filter(Club.name == "드림코딩").first()
    if not club:
        from datetime import date
        club = Club(
            president_id=president.id,
            name="드림코딩",
            club_type="central",
            description=(
                "청주대학교 중앙 개발 동아리 드림코딩입니다.\n"
                "웹·앱 개발, 알고리즘 스터디, 해커톤 참여 등 다양한 활동을 합니다.\n"
                "학과 무관 누구든 열정 있는 분 환영합니다!"
            ),
            contact_email="dreamcoding@cju.ac.kr",
            contact_phone="010-0000-1234",
            open_chat_url="https://open.kakao.com/o/example",
            image_url=None,
            division="중앙동아리",
            field="IT/개발",
            atmosphere="열정적",
            activity_purpose="실력 향상 및 프로젝트 경험",
            activity_period="매주 수요일 저녁",
            recruit_start=date(2026, 3, 1),
            recruit_end=date(2026, 3, 31),
            is_recruiting=True,
        )
        db.add(club)
        db.flush()

        for key, value in [
            ("division", "중앙동아리"),
            ("field", "IT/개발"),
            ("atmosphere", "열정적"),
            ("activity_purpose", "프로젝트"),
            ("activity_period", "매주 수요일"),
        ]:
            db.add(ClubTag(club_id=club.id, tag_key=key, tag_value=value))

        print(f"[+] 동아리 생성: 드림코딩 (id={club.id})")
    else:
        print(f"[=] 동아리 기존 존재: 드림코딩 (id={club.id})")

    # ── 3. 회장을 부원으로 등록 ────────────────────────────────────
    membership = db.query(ClubMember).filter(
        ClubMember.club_id == club.id,
        ClubMember.user_id == president.id,
    ).first()
    if not membership:
        db.add(ClubMember(
            club_id=club.id,
            user_id=president.id,
            role="president",
            status="active",
        ))
        print("[+] 회장 부원 등록 완료")

    # ── 4. 신청 폼 + 질문 ─────────────────────────────────────────
    form = db.query(ApplicationForm).filter(
        ApplicationForm.club_id == club.id,
        ApplicationForm.is_active == True,
    ).first()
    if not form:
        form = ApplicationForm(
            club_id=club.id,
            title="드림코딩 2026 신입 부원 모집",
            is_active=True,
        )
        db.add(form)
        db.flush()

        questions = [
            FormQuestion(
                form_id=form.id,
                question_text="자기소개를 해주세요. (학번, 학과, 이름 포함)",
                question_type="text",
                is_required=True,
                order_index=0,
                options=None,
            ),
            FormQuestion(
                form_id=form.id,
                question_text="지원 동기를 적어주세요.",
                question_type="text",
                is_required=True,
                order_index=1,
                options=None,
            ),
            FormQuestion(
                form_id=form.id,
                question_text="관심 있는 분야를 선택해주세요.",
                question_type="choice",
                is_required=True,
                order_index=2,
                options=["웹 프론트엔드", "웹 백엔드", "앱(Android/iOS)", "AI/데이터", "기타"],
            ),
            FormQuestion(
                form_id=form.id,
                question_text="본인의 개발 경험 수준은 어느 정도인가요?",
                question_type="choice",
                is_required=True,
                order_index=3,
                options=["완전 처음", "기초 학습 중", "토이 프로젝트 경험", "실무/외부 프로젝트 경험"],
            ),
            FormQuestion(
                form_id=form.id,
                question_text="포트폴리오나 GitHub 링크가 있다면 적어주세요. (선택)",
                question_type="text",
                is_required=False,
                order_index=4,
                options=None,
            ),
        ]
        db.add_all(questions)
        print(f"[+] 신청 폼 생성: {form.title} (id={form.id})")
    else:
        print(f"[=] 신청 폼 기존 존재 (id={form.id})")

    db.commit()

    print("\n────────────────────────────────")
    print(f"동아리 ID  : {club.id}")
    print(f"신청 폼 ID : {form.id}")
    print(f"회장 학번  : {PRESIDENT_STUDENT_ID}")
    print(f"회장 비번  : {PRESIDENT_PASSWORD}")
    print("────────────────────────────────")
    print("테스트 API 예시:")
    print(f"  GET /api/v1/clubs/{club.id}")
    print(f"  GET /api/v1/clubs/{club.id}/form")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed(db)
    except Exception as e:
        db.rollback()
        print(f"[!] 오류 발생: {e}")
        raise
    finally:
        db.close()
