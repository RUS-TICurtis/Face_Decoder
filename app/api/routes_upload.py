from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_service import save_upload_file
from app.utils.image_utils import validate_image
from app.schemas.face import ImageUploadResponse, ImageDimensions

router = APIRouter(prefix="", tags=["Upload"])

@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """
    Ingest a facial or emotional subject image into the storage filing system.
    Validates file headers, creates a secure identifier, and records dimension metadata.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a valid filename.")

    # Validate image data
    if not validate_image(file.file):
        raise HTTPException(status_code=400, detail="Invalid image file or unsupported image binary.")

    # Reset file pointer after validation
    file.file.seek(0)

    file_id, stored_filename, file_path, size_bytes, (width, height), img_format = save_upload_file(file)

    return ImageUploadResponse(
        file_id=file_id,
        original_filename=file.filename,
        stored_filename=stored_filename,
        file_path=str(file_path),
        format=img_format,
        dimensions=ImageDimensions(width=width, height=height),
        size_bytes=size_bytes,
        status="uploaded successfully"
    )