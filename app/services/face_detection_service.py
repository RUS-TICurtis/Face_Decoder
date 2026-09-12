import os
import urllib.request
from pathlib import Path
from typing import List, Optional, Tuple
import cv2
import numpy as np

from app.core.config import settings
from app.schemas.face import (
    FaceBoundingBox,
    LandmarkPoint,
    FacialLandmarks,
    DetectedFace,
    FaceAnalysisResponse,
    ImageDimensions,
)

YUNET_MODEL_URL = "https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"
MODELS_DIR = settings.CACHE_DIR / "models"
MODEL_PATH = MODELS_DIR / "face_detection_yunet_2023mar.onnx"

class FaceDetectionService:
    """
    Production-grade Face Detection & Landmark Extraction Service powered by OpenCV YuNet.
    Extracts bounding boxes, 5 key landmarks (eyes, nose, mouth corners), and crops faces.
    """

    def __init__(self):
        self._ensure_model_available()
        self._detector: Optional[cv2.FaceDetectorYN] = None

    def _ensure_model_available(self) -> None:
        """Download YuNet model if not already cached locally."""
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        if not MODEL_PATH.exists() or MODEL_PATH.stat().st_size < 10000:
            print(f"Downloading YuNet face detection model to {MODEL_PATH}...")
            urllib.request.urlretrieve(YUNET_MODEL_URL, MODEL_PATH)

    def _get_detector(self, width: int, height: int, score_threshold: float = 0.6) -> cv2.FaceDetectorYN:
        """Create or update FaceDetectorYN instance for current image resolution."""
        self._ensure_model_available()
        return cv2.FaceDetectorYN_create(
            str(MODEL_PATH),
            "",
            (width, height),
            score_threshold=score_threshold,
            nms_threshold=0.3,
            top_k=5000,
        )

    def detect_and_crop(
        self,
        image_path: Path,
        file_id: str,
        padding_ratio: float = 0.15,
        score_threshold: float = 0.6
    ) -> FaceAnalysisResponse:
        """
        Detect faces in the given image, extract coordinates and 5 landmarks,
        and save cropped face chips into storage/processed_faces/.
        """
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found at path: {image_path}")

        # Read image
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Failed to read image binary at: {image_path}")

        h, w = img.shape[:2]
        detector = self._get_detector(w, h, score_threshold=score_threshold)
        
        # Detect faces
        _, faces = detector.detect(img)

        detected_faces: List[DetectedFace] = []

        if faces is not None:
            settings.PROCESSED_FACES_DIR.mkdir(parents=True, exist_ok=True)

            for idx, raw_face in enumerate(faces):
                # Bounding box coordinates
                bx, by, bw, bh = raw_face[0:4]
                conf = float(raw_face[14])

                # Landmarks: right_eye, left_eye, nose_tip, mouth_right, mouth_left
                landmarks = FacialLandmarks(
                    right_eye=LandmarkPoint(x=float(raw_face[4]), y=float(raw_face[5])),
                    left_eye=LandmarkPoint(x=float(raw_face[6]), y=float(raw_face[7])),
                    nose_tip=LandmarkPoint(x=float(raw_face[8]), y=float(raw_face[9])),
                    mouth_right=LandmarkPoint(x=float(raw_face[10]), y=float(raw_face[11])),
                    mouth_left=LandmarkPoint(x=float(raw_face[12]), y=float(raw_face[13])),
                )

                bbox = FaceBoundingBox(
                    x=int(max(0, bx)),
                    y=int(max(0, by)),
                    width=int(bw),
                    height=int(bh),
                    confidence=round(conf, 4),
                )

                # Compute padded crop boundary
                pad_w = int(bw * padding_ratio)
                pad_h = int(bh * padding_ratio)

                crop_x1 = max(0, int(bx - pad_w))
                crop_y1 = max(0, int(by - pad_h))
                crop_x2 = min(w, int(bx + bw + pad_w))
                crop_y2 = min(h, int(by + bh + pad_h))

                face_chip = img[crop_y1:crop_y2, crop_x1:crop_x2]

                crop_filename = f"{file_id}_face_{idx}.jpg"
                crop_path = settings.PROCESSED_FACES_DIR / crop_filename

                # Save cropped face chip
                cv2.imwrite(str(crop_path), face_chip)

                face_obj = DetectedFace(
                    face_id=f"{file_id}_face_{idx}",
                    index=idx,
                    bbox=bbox,
                    landmarks=landmarks,
                    confidence=round(conf, 4),
                    crop_filename=crop_filename,
                    crop_path=str(crop_path),
                )
                detected_faces.append(face_obj)

        return FaceAnalysisResponse(
            file_id=file_id,
            image_dimensions=ImageDimensions(width=w, height=h),
            total_faces=len(detected_faces),
            faces=detected_faces,
        )

face_detection_service = FaceDetectionService()
