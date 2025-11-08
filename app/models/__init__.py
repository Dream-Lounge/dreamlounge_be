# app/models/__init__.py
# 모델들을 임포트해서 Base.metadata에 모두 등록
from .club import Club           # noqa: F401
from .user import User, RoleEnum # noqa: F401
from .user_member import UserMember  # noqa: F401
from .user_guest import UserGuest    # noqa: F401
from .user_admin import UserAdmin    # noqa: F401
