# app/core/logging_config.py
import logging
import sys
from typing import Any

# 로그 포맷 정의
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(log_level: str = "INFO") -> None:
    """
    애플리케이션 로깅 설정
    
    Args:
        log_level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # 로그 레벨 변환
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # 루트 로거 설정
    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # SQLAlchemy 로거 설정 (쿼리 로그)
    # 개발: DEBUG, 운영: WARNING
    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    if log_level.upper() == "DEBUG":
        sqlalchemy_logger.setLevel(logging.INFO)  # SQL 쿼리 출력
    else:
        sqlalchemy_logger.setLevel(logging.WARNING)  # 운영에서는 경고만


def get_logger(name: str) -> logging.Logger:
    """
    특정 모듈의 로거 반환
    
    Args:
        name: 로거 이름 (보통 __name__ 사용)
    
    Returns:
        Logger 인스턴스
    """
    return logging.getLogger(name)