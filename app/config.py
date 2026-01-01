import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
import logging

# .env 파일 로드
load_dotenv()

# 기본 로거 사용 (logging_config 초기화 전)
logger = logging.getLogger(__name__)

# 환경 변수 읽기
DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "dreamlounge_db")

# 환경 설정 (개발/운영 구분)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # development, production
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # DEBUG, INFO, WARNING, ERROR

# 비밀번호 URL 인코딩 (특수문자 처리)
encoded_password = quote_plus(DB_PASSWORD) if DB_PASSWORD else ""

# 데이터베이스 URL 생성
if encoded_password:
    DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 디버깅용: 비밀번호 마스킹하여 로그 출력 (개발 환경에서만)
# 로깅은 main.py에서 초기화된 후에 동작
def log_database_config():
    """데이터베이스 설정 로깅 (main.py에서 호출)"""
    if ENVIRONMENT == "development":
        if DB_PASSWORD:
            masked_url = DATABASE_URL.replace(encoded_password, "****")
            logger.info(f"Database URL: {masked_url}")
        else:
            logger.info(f"Database URL: {DATABASE_URL}")
    else:
        # 운영 환경에서는 간단한 연결 성공 메시지만
        logger.info(f"Database connection configured for: {DB_NAME}")