import os
import uuid
import shutil
from pathlib import Path
from typing import Tuple, Optional
from PIL import Image
from fastapi import UploadFile, HTTPException

from app.core.config import settings

def ensure_storage_directories() -> None:
    """Ensure all configured storage directories exist."""
    settings.RAW_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    settings.PROCESSED_FACES_DIR.mkdir(parents=True, exist_ok=True)
    settings.EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
    settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    settings.CACHE_DIR.mkdir(parents=True, exist_ok=True)

def sanitize_filename(filename: str) -> str:
    """Sanitize original filename to prevent path traversal."""
    return Path(filename).name.replace(" ", "_")

def save_upload_file(upload_file: UploadFile) -> Tuple[str, str, Path, int, Tuple[int, int], str]:
    """
    Saves an uploaded image into the structured raw_images storage with a unique UUID.
    
    Returns:
        (file_id, stored_filename, full_file_path, file_size, (width, height), image_format)
    """
    ensure_storage_directories()
    
    clean_name = sanitize_filename(upload_file.filename or "unnamed_image.jpg")
    ext = clean_name.split(".")[-1].lower() if "." in clean_name else "jpg"
    
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Allowed formats: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    file_id = str(uuid.uuid4())
    stored_filename = f"{file_id}_{clean_name}"
    destination_path = settings.RAW_IMAGES_DIR / stored_filename
    
    with open(destination_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    file_size = destination_path.stat().st_size
    
    if file_size > settings.MAX_FILE_SIZE_BYTES:
        destination_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE_BYTES // (1024 * 1024)}MB"
        )
    
    # Read format and dimensions safely
    try:
        with Image.open(destination_path) as img:
            dimensions = (img.width, img.height)
            img_format = img.format or ext.upper()
    except Exception as e:
        destination_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail=f"Failed to inspect image file: {str(e)}")
    
    return file_id, stored_filename, destination_path, file_size, dimensions, img_format

def resolve_file_path(file_id_or_name: str, is_processed: bool = False) -> Optional[Path]:
    """
    Find an image in storage by its UUID prefix or exact filename.
    Searches RAW_IMAGES_DIR by default, or PROCESSED_FACES_DIR if is_processed=True.
    """
    search_dir = settings.PROCESSED_FACES_DIR if is_processed else settings.RAW_IMAGES_DIR
    if not search_dir.exists():
        return None
    for file in search_dir.iterdir():
        if file.is_file() and not file.name.startswith("."):
            if file.name.startswith(file_id_or_name) or file.name == file_id_or_name:
                return file
    return None