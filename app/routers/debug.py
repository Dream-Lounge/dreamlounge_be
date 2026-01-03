# app/routers/debug.py
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path

router = APIRouter(prefix="/debug", tags=["Debug"])

# 정적 파일 경로
FORM_DIR = Path(__file__).parent.parent.parent / "form"


@router.get("/register-form", response_class=HTMLResponse)
def show_register_form():
    """회원가입 폼 HTML 반환"""
    form_file = FORM_DIR / "register.html"
    if not form_file.exists():
        return HTMLResponse(
            content="<h1>회원가입 폼을 찾을 수 없습니다.</h1>",
            status_code=404
        )
    return FileResponse(form_file)


@router.get("/login-form", response_class=HTMLResponse)
def show_login_form():
    """로그인 폼 HTML 반환"""
    form_file = FORM_DIR / "login.html"
    if not form_file.exists():
        return HTMLResponse(
            content="<h1>로그인 폼을 찾을 수 없습니다.</h1>",
            status_code=404
        )
    return FileResponse(form_file)


@router.get("/form", response_class=HTMLResponse)
def show_test_form():
    """테스트 폼 HTML 반환 (기존 index.html)"""
    form_file = FORM_DIR / "index.html"
    if not form_file.exists():
        return HTMLResponse(
            content="<h1>폼 파일을 찾을 수 없습니다.</h1>",
            status_code=404
        )
    return FileResponse(form_file)