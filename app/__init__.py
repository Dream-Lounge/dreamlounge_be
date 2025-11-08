# app/__init__.py
# 패키지 초기화: Base만 노출하고, models를 로드해서 메타데이터에 등록
from .database import Base  # ✅ .db가 아니라 .database 를 사용
import app.models  # noqa: F401  # 모델 모듈들을 로드해서 Base.metadata에 반영
