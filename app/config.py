import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수 읽기
DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "club_management")

# 데이터베이스 URL 생성
DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 디버깅용: 비밀번호 마스킹하여 출력
if DB_PASSWORD:
    masked_url = DATABASE_URL.replace(DB_PASSWORD, "****")
    print(f"[DB] Connecting to: {masked_url}")
else:
    print(f"[DB] Connecting to: {DATABASE_URL}")