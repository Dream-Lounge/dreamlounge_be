import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
import logging

# .env 파일 로드
load_dotenv()

# 기본 로거 사용 (logging_config 초기화 전)
logger = logging.getLogger(__name__)

# ========================================
# 데이터베이스 설정
# ========================================
DB_USERNAME = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "dreamlounge_db")

# 비밀번호 URL 인코딩 (특수문자 처리)
encoded_password = quote_plus(DB_PASSWORD) if DB_PASSWORD else ""

# 데이터베이스 URL 생성
if encoded_password:
    DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# ========================================
# 환경 설정
# ========================================
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # development, production
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # DEBUG, INFO, WARNING, ERROR


# ========================================
# JWT 인증 설정
# ========================================
SECRET_KEY = os.getenv(
    "SECRET_KEY", 
    "your-secret-key-change-this-in-production-must-be-at-least-32-characters-long"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# 운영 환경에서 기본 SECRET_KEY 사용 시 경고
if ENVIRONMENT == "production" and SECRET_KEY == "your-secret-key-change-this-in-production-must-be-at-least-32-characters-long":
    logger.warning("⚠️ WARNING: Using default SECRET_KEY in production! Set SECRET_KEY in .env file!")


# ========================================
# 설정 검증 및 로깅
# ========================================
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


def log_jwt_config():
    """JWT 설정 로깅 (main.py에서 호출)"""
    if ENVIRONMENT == "development":
        logger.info(f"JWT Algorithm: {ALGORITHM}")
        logger.info(f"Token Expire Minutes: {ACCESS_TOKEN_EXPIRE_MINUTES}")
        # SECRET_KEY는 보안상 로그에 출력하지 않음
        logger.info(f"SECRET_KEY: {'*' * min(len(SECRET_KEY), 32)}...")
    else:
        logger.info("JWT authentication configured")


def validate_config():
    """설정 검증 (선택적으로 main.py에서 호출)"""
    errors = []
    
    # SECRET_KEY 검증
    if len(SECRET_KEY) < 32:
        errors.append("SECRET_KEY must be at least 32 characters long")
    
    # 데이터베이스 이름 검증
    if not DB_NAME:
        errors.append("DB_NAME is required")
    
    # 토큰 만료 시간 검증
    if ACCESS_TOKEN_EXPIRE_MINUTES < 1:
        errors.append("ACCESS_TOKEN_EXPIRE_MINUTES must be at least 1")
    
    if errors:
        error_msg = "Configuration errors:\n" + "\n".join(f"  - {err}" for err in errors)
        if ENVIRONMENT == "production":
            raise ValueError(error_msg)
        else:
            logger.warning(error_msg)
    
    return len(errors) == 0