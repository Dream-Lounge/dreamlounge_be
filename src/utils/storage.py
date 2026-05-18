import uuid
from fastapi import UploadFile

from src.core.config import settings
from src.utils.supabase_client import get_supabase_client

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


async def upload_club_image(file: UploadFile) -> str:
    """이미지 파일을 Supabase Storage에 업로드하고 퍼블릭 URL을 반환한다."""
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError("지원하지 않는 파일 형식입니다. jpg, png, webp, gif만 허용됩니다.")

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise ValueError("파일 크기는 5MB 이하여야 합니다.")

    ext = file.filename.rsplit(".", 1)[-1].lower() if file.filename and "." in file.filename else "jpg"
    path = f"clubs/{uuid.uuid4()}.{ext}"

    client = get_supabase_client()
    client.storage.from_(settings.SUPABASE_STORAGE_BUCKET).upload(
        path=path,
        file=contents,
        file_options={"content-type": file.content_type},
    )

    return client.storage.from_(settings.SUPABASE_STORAGE_BUCKET).get_public_url(path)
