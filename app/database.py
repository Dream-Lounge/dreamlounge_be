# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

# (A) .env 로드를 "uv --env-file" 없이도 안전하게 하려면 주석 해제
try:
    from dotenv import load_dotenv  # uv add python-dotenv
    load_dotenv()
except Exception:
    pass  # python-dotenv가 없어도 uv --env-file 로 실행하면 OK

DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "dreamlounge_db")

# (B) 기본값이 남아있으면 즉시 오류를 내서 문제를 빨리 알림
if DB_USER == "user":
    raise RuntimeError(
        "[DB CONFIG] DB_USER가 기본값('user')입니다. .env가 로드되지 않았거나 값이 잘못되었습니다."
    )

# (C) DSN 생성 (mysql-connector-python 사용)
url = URL.create(
    drivername="mysql+mysqlconnector",
    username=DB_USER,
    password=DB_PASS,   # URL.create가 안전 처리
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

# (D) 마스킹된 DSN 로그
masked = str(url)
if DB_PASS:
    masked = masked.replace(DB_PASS, "****")
print(f"[DB] URL: {masked}")

engine = create_engine(url, future=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()
