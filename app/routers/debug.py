from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path

router = APIRouter(prefix="/debug", tags=["Debug"])

FORM_DIR = Path(__file__).parent.parent.parent / "form"

@router.get("/register-form", response_class=HTMLResponse)
def register_form():
    """회원가입 폼"""
    return FileResponse(FORM_DIR / "register.html")

@router.get("/login-form", response_class=HTMLResponse)
def login_form():
    """로그인 폼"""
    return FileResponse(FORM_DIR / "login.html")

# ✅ 추가: 테스트 페이지 라우트
@router.get("/test-page", response_class=HTMLResponse)
def test_page():
    """JWT 테스트 페이지"""
    return FileResponse(FORM_DIR / "test-page.html")