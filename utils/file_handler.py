import os
import uuid
from fastapi import UploadFile, HTTPException, status
from core.config import UPLOAD_DIR, MAX_FILE_SIZE

ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".svg"]
ALLOWED_DOCUMENT_EXTENSIONS = [".pdf", ".doc", ".docx", ".xlsx", ".xls"]
ALLOWED_ARCHIVE_EXTENSIONS = [".zip", ".rar"]

os.makedirs(UPLOAD_DIR, exist_ok=True)

def validate_file(file: UploadFile):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS + ALLOWED_DOCUMENT_EXTENSIONS + ALLOWED_ARCHIVE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Fayl turi ruxsat etilmagan: {ext}"
        )

def get_unique_filename(original_filename: str) -> str:
    ext = os.path.splitext(original_filename)[1]
    return f"{uuid.uuid4().hex}{ext}"

async def save_upload_file(file: UploadFile, folder: str = "") -> str:
    validate_file(file)
    folder_path = os.path.join(UPLOAD_DIR, folder)
    os.makedirs(folder_path, exist_ok=True)
    filename = get_unique_filename(file.filename)
    file_path = os.path.join(folder_path, filename)

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Fayl hajmi ruxsat etilgan limitdan oshdi")

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    return os.path.join(folder, filename)

def delete_file(path: str):
    full_path = os.path.join(UPLOAD_DIR, path)
    if os.path.exists(full_path):
        os.remove(full_path)
