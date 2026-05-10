import os
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# 1. 환경 설정 로드
load_dotenv()

app = FastAPI(
    title="DreamLounge API",
    description="청주대 동아리 서비스 - 이메일 인증 + 프로필 통합 관리",
    version="1.1.0"
)

# CORS 설정: 프론트엔드(5173)와의 통신을 허용합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Supabase 설정
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# --- [3. 데이터 모델(Schemas) 정의] ---

class UserSignup(BaseModel):
    email: str
    password: str

class VerifyOTP(BaseModel):
    email: str
    token: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserProfileUpdate(BaseModel):
    user_id: str
    name: str
    student_id: str
    phone: str       
    department: str

# --- [4. API 엔드포인트] ---

@app.get("/")
async def root():
    return {"message": "DreamLounge 서버가 정상 작동 중입니다!"}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client
import os

# --- [1. 데이터 모델 정의] ---
class UserSignup(BaseModel):
    email: EmailStr
    password: str

class VerifyOTP(BaseModel):
    email: str
    token: str

class UserLogin(BaseModel):
    email: str
    password: str

# image_8bfffa.png의 DB 구조를 그대로 반영한 모델입니다.
class ProfileData(BaseModel):
    user_id: str
    name: str
    student_id: str
    department: str
    phone: str # 필수 필드!

# --- [2. 백엔드 엔드포인트] ---

@app.post("/auth/signup", tags=["Auth"], summary="1. 회원가입 (메일 발송)")
async def signup(data: UserSignup):
    """청주대학교 메일로 OTP 인증 번호를 발송합니다."""
    if not data.email.endswith("@cju.ac.kr"):
        raise HTTPException(status_code=400, detail="청주대학교 이메일(@cju.ac.kr)만 사용 가능합니다.")

    try:
        # Supabase에 유저 생성 요청 (이때 메일이 자동 발송됩니다)
        response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password,
        })
        return {"message": "인증 메일이 발송되었습니다.", "user": response.user}
    except Exception as e:
        print(f"🔥 회원가입 에러: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/verify-otp", tags=["Auth"], summary="2. OTP 인증")
async def verify_otp(data: VerifyOTP):
    """메일로 받은 8자리 번호를 검증합니다."""
    try:
        # 1. Supabase OTP 검증 실행
        response = supabase.auth.verify_otp({
            "email": data.email,
            "token": data.token.strip(), # 혹시 모를 공백 제거
            "type": "signup"
        })
        
        # 2. 인증 성공 시 유저의 UUID 반환
        # response 객체 내부에 user 정보가 있는지 확인 후 반환합니다.
        if response.user:
            return {"status": "success", "user_id": response.user.id}
        else:
            raise Exception("유저 정보를 찾을 수 없습니다.")

    except Exception as e:
        # 터미널에 실제 Supabase가 뱉는 에러 메시지를 출력하여 원인을 파악합니다.
        # 예: "AuthApiError: Email link is invalid or has expired"
        print(f"🔥 OTP 인증 실패 상세 원인: {str(e)}")
        
        # 프론트엔드에는 사용자 친화적인 메시지를 보냅니다.
        raise HTTPException(
            status_code=400, 
            detail="인증 번호가 올바르지 않거나 시간이 만료되었습니다. 가장 최근에 받은 메일의 번호를 입력해주세요."
        )
@app.post("/auth/profile", tags=["Auth"], summary="3. 프로필 정보 저장")
async def create_profile(data: ProfileData):
    """회원가입 완료 후 유저의 상세 정보를 DB에 저장합니다."""
    try:
        # image_8bfffa.png의 모든 NOT NULL 제약조건을 충족시킵니다.
        profile_res = supabase.table("profiles").insert({
            "id": data.user_id,
            "name": data.name,
            "student_id": data.student_id,
            "department": data.department,
            "phone": data.phone # 전화번호 누락 방지!
        }).execute()
        
        return {"message": "프로필 저장 성공", "data": profile_res.data}
    except Exception as e:
        print(f"🔥 프로필 저장 에러: {str(e)}")
        raise HTTPException(status_code=400, detail="프로필 정보를 저장하는 중 오류가 발생했습니다.")

@app.post("/auth/login", tags=["Auth"], summary="4. 로그인")
async def login(data: UserLogin):
    """로그인 처리 및 프로필 상세 정보를 반환합니다."""
    login_email = data.email
    if "@" not in login_email:
        login_email = f"{login_email}@cju.ac.kr"
        
    try:
        # 1. Supabase 인증
        auth_res = supabase.auth.sign_in_with_password({
            "email": login_email,
            "password": data.password,
        })
        
        user_id = auth_res.user.id
        
        # 2. profiles 테이블에서 정보 가져오기
        profile_res = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        
        # 3. 만약 프로필이 없다면(회원가입 도중 이탈 등) 예외 처리
        if not profile_res.data:
            return {
                "message": "로그인 성공 (프로필 정보 없음)",
                "access_token": auth_res.session.access_token,
                "user": auth_res.user,
                "profile": None
            }
            
        return {
            "message": "로그인 성공",
            "access_token": auth_res.session.access_token,
            "user": auth_res.user,
            "profile": profile_res.data 
        }
    except Exception as e:
        print(f"🔥 로그인 에러: {str(e)}")
        raise HTTPException(status_code=400, detail="아이디 또는 비밀번호를 확인해주세요.")
@app.post("/auth/profile", tags=["Auth"], summary="4. 프로필 저장")
@app.post("/auth/profile", tags=["Auth"])
async def create_profile(data: UserProfileUpdate):
    """이름, 학번(아이디), 전화번호, 학과 정보를 DB에 저장합니다."""
    try:
        response = supabase.table("profiles").insert({
            "id": data.user_id,
            "name": data.name,
            "student_id": data.student_id,
            "phone": data.phone,     
            "department": data.department
        }).execute()
        return {"message": "프로필 저장 성공", "data": response.data}
    except Exception as e:
        print(f"🔥 프로필 저장 에러 원인: {str(e)}") # 터미널 확인용
        raise HTTPException(status_code=400, detail=f"프로필 저장 실패: {str(e)}")
@app.get("/auth/profile/{user_id}", tags=["Auth"])
async def get_profile(user_id: str):
    """유저 ID로 프로필 정보를 조회합니다."""
    try:
        response = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=404, detail="프로필을 찾을 수 없습니다.")