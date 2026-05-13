import json
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    RESEND_API_KEY: str = ""
    RESEND_FROM_EMAIL: str = "noreply@dreamlounge.dev"

    FRONTEND_URL: str = "http://localhost:3000"
    ALLOWED_ORIGINS: str = '["http://localhost:3000"]'

    EMAIL_VERIFICATION_EXPIRY_MINUTES: int = 30
    CJU_EMAIL_DOMAIN: str = "cju.ac.kr"

    def get_allowed_origins(self) -> List[str]:
        return json.loads(self.ALLOWED_ORIGINS)

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
