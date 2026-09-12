import io
from typing import BinaryIO
from PIL import Image

def validate_image(file_obj: BinaryIO) -> bool:
    """
    Validate that the stream is a readable, non-corrupt image.
    Preserves the initial stream position after inspection.
    """
    try:
        pos = file_obj.tell() if hasattr(file_obj, "tell") else 0
        img = Image.open(file_obj)
        img.verify()
        if hasattr(file_obj, "seek"):
            file_obj.seek(pos)
        return True
    except Exception:
        return False