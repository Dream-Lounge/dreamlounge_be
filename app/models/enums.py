import enum


class ClubType(str, enum.Enum):
    DEPARTMENT = "학과"
    CENTRAL = "중앙"


class MembershipStatus(str, enum.Enum):
    ACTIVE = "활동중"
    WITHDRAWN = "탈퇴"


class UserType(str, enum.Enum):
    MEMBER = "회원"
    GUEST = "비회원"


class ApplicationStatus(str, enum.Enum):
    DRAFT = "임시저장"
    SUBMITTED = "제출됨"
    ACCEPTED = "합격"
    REJECTED = "불합격"